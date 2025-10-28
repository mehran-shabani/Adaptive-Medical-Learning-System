import 'dart:convert';
import 'package:http/http.dart' as http;
import '../storage/secure_storage.dart';

/// Authentication API service
/// 
/// Handles OTP login flow and JWT token management.
class AuthApiService {
  // TODO: Update with actual backend URL
  static const String baseUrl = 'http://localhost:8000/api/v1/auth';
  
  final SecureStorageService _storage = SecureStorageService();
  
  /// Request OTP for phone number
  /// 
  /// POST /auth/login-otp
  /// Request: { "phone_number": "+98912xxxxxxx" }
  /// Response: { "status": "otp_sent" }
  Future<Map<String, dynamic>> loginWithOTP(String phoneNumber) async {
    final response = await http.post(
      Uri.parse('$baseUrl/login-otp'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'phone_number': phoneNumber}),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body) as Map<String, dynamic>;
    } else {
      throw Exception('Failed to send OTP: ${response.body}');
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
    final response = await http.post(
      Uri.parse('$baseUrl/verify-otp'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'phone_number': phoneNumber,
        'otp_code': otpCode,
      }),
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      
      // Save authentication data securely
      await _storage.saveAccessToken(data['access_token']);
      await _storage.saveUserId(data['user_id']);
      await _storage.saveUserRole(data['role']);
      
      return data;
    } else {
      throw Exception('Failed to verify OTP: ${response.body}');
    }
  }
  
  /// Logout and clear stored tokens
  Future<void> logout() async {
    await _storage.clearAuthData();
  }
}
