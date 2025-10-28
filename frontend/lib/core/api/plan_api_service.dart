import 'dart:convert';
import 'dart:io';

import 'package:adaptivemed_mobile/core/config/api_config.dart';
import 'package:adaptivemed_mobile/core/storage/secure_storage.dart';
import 'package:http/http.dart' as http;

/// Study Plan API service
///
/// Fetches personalized study plans based on spaced repetition.
class PlanApiService {
  final SecureStorageService _storage = SecureStorageService();

  /// Get personalized study plan
  ///
  /// POST /recommender/study-plan
  /// Headers: Authorization: Bearer <JWT>
  /// Body: { "user_id": 1, "duration_minutes": 120, "include_quiz": true }
  /// Response: { "duration_minutes": 120, "blocks": [...], "total_topics": 3 }
  Future<Map<String, dynamic>> getStudyPlan({
    int durationMinutes = 120,
    bool includeQuiz = true,
    List<int>? focusTopics,
  }) async {
    try {
      final token = await _storage.getAccessToken();
      final userId = await _storage.getUserId();

      if (token == null || userId == null) {
        throw Exception('No authentication token found. Please login again.');
      }

      final response = await http
          .post(
            Uri.parse(ApiConfig.recommenderStudyPlan),
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer $token',
            },
            body: jsonEncode({
              'user_id': userId,
              'duration_minutes': durationMinutes,
              'include_quiz': includeQuiz,
              if (focusTopics != null) 'focus_topics': focusTopics,
            }),
          )
          .timeout(ApiConfig.requestTimeout);

      if (response.statusCode == 200) {
        return jsonDecode(utf8.decode(response.bodyBytes))
            as Map<String, dynamic>;
      } else if (response.statusCode == 401) {
        throw Exception('Authentication failed. Please login again.');
      } else if (response.statusCode == 404) {
        throw Exception('User not found');
      } else {
        final error = jsonDecode(utf8.decode(response.bodyBytes));
        throw Exception(error['detail'] ?? 'Failed to load study plan');
      }
    } on SocketException {
      throw Exception('No internet connection. Please check your network.');
    } on http.ClientException {
      throw Exception('Connection error. Please try again.');
    } catch (e) {
      throw Exception('Failed to load study plan: ${e.toString()}');
    }
  }
}
