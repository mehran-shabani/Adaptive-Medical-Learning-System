import 'dart:convert';
import 'package:http/http.dart' as http;
import '../storage/secure_storage.dart';

/// Study Plan API service
/// 
/// Fetches personalized study plans based on spaced repetition.
class PlanApiService {
  // TODO: Update with actual backend URL
  static const String baseUrl = 'http://localhost:8000/api/v1';
  
  final SecureStorageService _storage = SecureStorageService();
  
  /// Get personalized study plan
  /// 
  /// GET /recommender/{user_id}/plan?duration_minutes=120
  /// Headers: Authorization: Bearer <JWT>
  /// Response: { "duration_minutes": 120, "blocks": [...] }
  Future<Map<String, dynamic>> getStudyPlan(
    int userId, {
    int durationMinutes = 120,
    bool includeQuiz = true,
  }) async {
    final token = await _storage.getAccessToken();
    
    if (token == null) {
      throw Exception('No authentication token found');
    }
    
    final queryParams = {
      'duration_minutes': durationMinutes.toString(),
      'include_quiz': includeQuiz.toString(),
    };
    
    final uri = Uri.parse('$baseUrl/recommender/$userId/plan')
        .replace(queryParameters: queryParams);
    
    final response = await http.get(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
    } else if (response.statusCode == 401) {
      throw Exception('Authentication failed. Please login again.');
    } else {
      throw Exception('Failed to load study plan: ${response.body}');
    }
  }
}
