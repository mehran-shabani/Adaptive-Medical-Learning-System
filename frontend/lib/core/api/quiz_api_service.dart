import 'dart:convert';
import 'dart:io';

import 'package:adaptivemed_mobile/core/config/api_config.dart';
import 'package:adaptivemed_mobile/core/storage/secure_storage.dart';
import 'package:http/http.dart' as http;

/// Quiz API service
///
/// Handles quiz generation and answer submission.
class QuizApiService {
  final SecureStorageService _storage = SecureStorageService();

  /// Generate quiz questions for a topic
  ///
  /// POST /quiz/generate
  /// Headers: Authorization: Bearer <JWT>
  /// Body: { "topic_id": 1, "count": 5, "difficulty": "medium" }
  /// Response: [ { "id": 771, "stem": "...", "options": [...] } ]
  Future<List<dynamic>> generateQuiz({
    required int topicId,
    int count = 5,
    String? difficulty,
  }) async {
    try {
      final token = await _storage.getAccessToken();

      if (token == null) {
        throw Exception('No authentication token found. Please login again.');
      }

      final response = await http
          .post(
            Uri.parse(ApiConfig.quizGenerate),
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer $token',
            },
            body: jsonEncode({
              'topic_id': topicId,
              'count': count,
              if (difficulty != null) 'difficulty': difficulty,
            }),
          )
          .timeout(ApiConfig.requestTimeout);

      if (response.statusCode == 200) {
        final data =
            jsonDecode(utf8.decode(response.bodyBytes)) as List<dynamic>;
        return data;
      } else if (response.statusCode == 401) {
        throw Exception('Authentication failed. Please login again.');
      } else if (response.statusCode == 404) {
        throw Exception('Topic not found');
      } else {
        final error = jsonDecode(utf8.decode(response.bodyBytes));
        throw Exception(error['detail'] ?? 'Failed to generate quiz');
      }
    } on SocketException {
      throw Exception('No internet connection. Please check your network.');
    } on http.ClientException {
      throw Exception('Connection error. Please try again.');
    } catch (e) {
      throw Exception('Failed to generate quiz: ${e.toString()}');
    }
  }

  /// Submit quiz answer
  ///
  /// POST /quiz/submit-answer
  /// Headers: Authorization: Bearer <JWT>
  /// Body: {
  ///   "user_id": 1,
  ///   "question_id": 42,
  ///   "chosen_option": "B",
  ///   "response_time_sec": 45.5
  /// }
  /// Response:
  /// { "correct": true, "explanation": "...", "new_mastery_score": 0.75 }
  Future<Map<String, dynamic>> submitAnswer({
    required int userId,
    required int questionId,
    required String chosenOption,
    required double responseTimeSec,
  }) async {
    try {
      final token = await _storage.getAccessToken();

      if (token == null) {
        throw Exception('No authentication token found. Please login again.');
      }

      final response = await http
          .post(
            Uri.parse(ApiConfig.quizSubmitAnswer),
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer $token',
            },
            body: jsonEncode({
              'user_id': userId,
              'question_id': questionId,
              'chosen_option': chosenOption,
              'response_time_sec': responseTimeSec,
            }),
          )
          .timeout(ApiConfig.requestTimeout);

      if (response.statusCode == 200) {
        return jsonDecode(utf8.decode(response.bodyBytes))
            as Map<String, dynamic>;
      } else if (response.statusCode == 401) {
        throw Exception('Authentication failed. Please login again.');
      } else if (response.statusCode == 404) {
        throw Exception('Question not found');
      } else {
        final error = jsonDecode(utf8.decode(response.bodyBytes));
        throw Exception(error['detail'] ?? 'Failed to submit answer');
      }
    } on SocketException {
      throw Exception('No internet connection. Please check your network.');
    } on http.ClientException {
      throw Exception('Connection error. Please try again.');
    } catch (e) {
      throw Exception('Failed to submit answer: ${e.toString()}');
    }
  }
}
