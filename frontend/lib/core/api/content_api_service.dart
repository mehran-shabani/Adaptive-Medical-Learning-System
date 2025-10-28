import 'dart:convert';
import 'package:http/http.dart' as http;
import '../storage/secure_storage.dart';

/// Content API service
/// 
/// Fetches topic summaries with citations.
class ContentApiService {
  // TODO: Update with actual backend URL
  static const String baseUrl = 'http://localhost:8000/api/v1/content';
  
  final SecureStorageService _storage = SecureStorageService();
  
  /// Get topic summary with key points and citations
  /// 
  /// GET /content/topic/{topic_id}/summary
  /// Headers: Authorization: Bearer <JWT>
  /// Response: {
  ///   "topic": "DKA Management",
  ///   "key_points": ["..."],
  ///   "high_yield_traps": ["..."],
  ///   "citations": [
  ///     {"source_reference": "Harrison 21e p.304-305", "chunk_id": 182}
  ///   ]
  /// }
  Future<Map<String, dynamic>> getTopicSummary(int topicId) async {
    final token = await _storage.getAccessToken();
    
    if (token == null) {
      throw Exception('No authentication token found');
    }
    
    final response = await http.get(
      Uri.parse('$baseUrl/topics/$topicId/summary'),
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
      throw Exception('Failed to load topic summary: ${response.body}');
    }
  }
}
