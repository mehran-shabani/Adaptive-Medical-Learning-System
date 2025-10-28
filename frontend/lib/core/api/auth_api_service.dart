import 'dart:convert';
import 'dart:io';

import 'package:adaptivemed_mobile/core/config/api_config.dart';
import 'package:adaptivemed_mobile/core/storage/secure_storage.dart';
import 'package:http/http.dart' as http;

/// Authentication API service
///
/// Handles OTP login flow and JWT token management.
class AuthApiService {
  final SecureStorageService _storage = SecureStorageService();

  /// Request OTP for phone number
  ///
  /// POST /auth/login-otp
  /// Request: { "phone_number": "+98912xxxxxxx" }
  /// Response: { "status": "otp_sent" }
  Future<Map<String, dynamic>> loginWithOTP(String phoneNumber) async {
    try {
      final response = await http
          .post(
            Uri.parse(ApiConfig.authLoginOtp),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({'phone_number': phoneNumber}),
          )
          .timeout(ApiConfig.requestTimeout);

      if (response.statusCode == 200) {
        return jsonDecode(utf8.decode(response.bodyBytes))
            as Map<String, dynamic>;
      } else if (response.statusCode == 400) {
        final error = jsonDecode(utf8.decode(response.bodyBytes));
        throw Exception(error['detail'] ?? 'Invalid phone number');
      } else {
        throw Exception('Failed to send OTP: ${response.statusCode}');
      }
    } on SocketException {
      throw Exception('No internet connection. Please check your network.');
    } on http.ClientException {
      throw Exception('Connection error. Please try again.');
    } catch (e) {
      throw Exception('Failed to send OTP: ${e.toString()}');
    }
  }

  /// Verify OTP and get JWT token
  ///
  /// POST /auth/verify-otp
  /// Request: { "phone_number": "+98912xxxxxxx", "otp_code": "1234" }
  /// Response: { "access_token": "<JWT>", "user_id": 42, "role": "student" }
  Future<Map<String, dynamic>> verifyOTP(
    String phoneNumber,
    String otpCode,
  ) async {
    try {
      final response = await http
          .post(
            Uri.parse(ApiConfig.authVerifyOtp),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'phone_number': phoneNumber,
              'otp_code': otpCode,
            }),
          )
          .timeout(ApiConfig.requestTimeout);

      if (response.statusCode == 200) {
        final data =
            jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;

        // Save authentication data securely
        await _storage.saveAccessToken(data['access_token'] as String);
        await _storage.saveUserId(data['user_id'] as int);
        await _storage.saveUserRole(data['role'] as String);

        return data;
      } else if (response.statusCode == 400) {
        final error = jsonDecode(utf8.decode(response.bodyBytes));
        throw Exception(error['detail'] ?? 'Invalid OTP code');
      } else if (response.statusCode == 401) {
        throw Exception('Invalid or expired OTP code');
      } else {
        throw Exception('Failed to verify OTP: ${response.statusCode}');
      }
    } on SocketException {
      throw Exception('No internet connection. Please check your network.');
    } on http.ClientException {
      throw Exception('Connection error. Please try again.');
    } catch (e) {
      throw Exception('Failed to verify OTP: ${e.toString()}');
    }
  }

  /// Logout and clear stored tokens
  Future<void> logout() async {
    await _storage.clearAuthData();
  }
}
