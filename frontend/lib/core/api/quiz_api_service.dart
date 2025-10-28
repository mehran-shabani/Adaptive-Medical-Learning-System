import 'dart:convert';
import 'package:http/http.dart' as http;
import '../storage/secure_storage.dart';

/// Quiz API service
/// 
/// Handles quiz generation and answer submission.
class QuizApiService {
  // TODO: Update with actual backend URL
  static const String baseUrl = 'http://localhost:8000/api/v1/quiz';
  
  final SecureStorageService _storage = SecureStorageService();
  
  /// Generate quiz questions for a topic
  /// 
  /// GET /quiz/generate?topic_id=...&limit=5
  /// Headers: Authorization: Bearer <JWT>
  /// Response: [ { "question_id": 771, "stem": "...", "options": [...] } ]
  Future<List<dynamic>> generateQuiz({
    required int topicId,
    int limit = 5,
    String? difficulty,
  }) async {
    final token = await _storage.getAccessToken();
    
    if (token == null) {
      throw Exception('No authentication token found');
    }
    
    final queryParams = {
      'topic_id': topicId.toString(),
      'limit': limit.toString(),
      if (difficulty != null) 'difficulty': difficulty,
    };
    
    final uri = Uri.parse('$baseUrl/generate')
        .replace(queryParameters: queryParams);
    
    final response = await http.get(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(utf8.decode(response.bodyBytes)) as List<dynamic>;
    } else if (response.statusCode == 401) {
      throw Exception('Authentication failed. Please login again.');
    } else {
      throw Exception('Failed to generate quiz: ${response.body}');
    }
  }
  
  /// Submit quiz answer
  /// 
  /// POST /quiz/answer
  /// Headers: Authorization: Bearer <JWT>
  /// Body: {
  ///   "user_id": 1,
  ///   "question_id": 42,
  ///   "chosen_option": "B",
  ///   "response_time_sec": 45.5
  /// }
  /// Response: { "correct": true, "explanation": "...", "updated_mastery": {...} }
  Future<Map<String, dynamic>> submitAnswer({
    required int userId,
    required int questionId,
    required String chosenOption,
    required double responseTimeSec,
  }) async {
    final token = await _storage.getAccessToken();
    
    if (token == null) {
      throw Exception('No authentication token found');
    }
    
    final response = await http.post(
      Uri.parse('$baseUrl/answer'),
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
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
    } else if (response.statusCode == 401) {
      throw Exception('Authentication failed. Please login again.');
    } else {
      throw Exception('Failed to submit answer: ${response.body}');
    }
  }
}
