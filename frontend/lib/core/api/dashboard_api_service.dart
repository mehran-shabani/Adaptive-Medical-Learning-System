import 'dart:convert';
import 'dart:io';

import '../storage/secure_storage.dart';
import 'package:http/http.dart' as http;

import 'package:adaptivemed_mobile/core/config/api_config.dart';

/// Dashboard API service
///
/// Fetches mastery data and user progress for dashboard.
class DashboardApiService {
  final SecureStorageService _storage = SecureStorageService();

  /// Get user's mastery across all topics
  ///
  /// GET /mastery/user/{user_id}
  Future<List<Map<String, dynamic>>> getUserMastery() async {
    try {
      final token = await _storage.getAccessToken();
      final userId = await _storage.getUserId();

      if (token == null || userId == null) {
        throw Exception('No authentication token found. Please login again.');
      }

      final response = await http.get(
        Uri.parse('${ApiConfig.masteryByUser}/$userId'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
      ).timeout(ApiConfig.requestTimeout);

      if (response.statusCode == 200) {
        final data =
            jsonDecode(utf8.decode(response.bodyBytes)) as List<dynamic>;
        return data.cast<Map<String, dynamic>>();
      } else if (response.statusCode == 401) {
        throw Exception('Authentication failed. Please login again.');
      } else {
        throw Exception('Failed to load mastery data');
      }
    } on SocketException {
      throw Exception('No internet connection. Please check your network.');
    } on http.ClientException {
      throw Exception('Connection error. Please try again.');
    } catch (e) {
      throw Exception('Failed to load mastery data: ${e.toString()}');
    }
  }

  /// Get weak topics that need more study
  ///
  /// GET /mastery/user/{user_id}/weak-topics
  Future<List<Map<String, dynamic>>> getWeakTopics() async {
    try {
      final token = await _storage.getAccessToken();
      final userId = await _storage.getUserId();

      if (token == null || userId == null) {
        throw Exception('No authentication token found. Please login again.');
      }

      final response = await http.get(
        Uri.parse(ApiConfig.masteryWeakTopics(userId)),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
      ).timeout(ApiConfig.requestTimeout);

      if (response.statusCode == 200) {
        final data =
            jsonDecode(utf8.decode(response.bodyBytes)) as List<dynamic>;
        return data.cast<Map<String, dynamic>>();
      } else if (response.statusCode == 401) {
        throw Exception('Authentication failed. Please login again.');
      } else {
        throw Exception('Failed to load weak topics');
      }
    } on SocketException {
      throw Exception('No internet connection. Please check your network.');
    } on http.ClientException {
      throw Exception('Connection error. Please try again.');
    } catch (e) {
      throw Exception('Failed to load weak topics: ${e.toString()}');
    }
  }
}
