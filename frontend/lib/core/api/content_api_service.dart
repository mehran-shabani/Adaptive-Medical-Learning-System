import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../storage/secure_storage.dart';
import '../config/api_config.dart';

/// Content API service
///
/// Fetches topic summaries with citations.
class ContentApiService {
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
    try {
      final token = await _storage.getAccessToken();

      if (token == null) {
        throw Exception('No authentication token found. Please login again.');
      }

      final response = await http.get(
        Uri.parse(ApiConfig.contentTopicSummary(topicId)),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
      ).timeout(ApiConfig.requestTimeout);

      if (response.statusCode == 200) {
        return jsonDecode(utf8.decode(response.bodyBytes))
            as Map<String, dynamic>;
      } else if (response.statusCode == 401) {
        throw Exception('Authentication failed. Please login again.');
      } else if (response.statusCode == 404) {
        throw Exception('Topic not found');
      } else {
        final error = jsonDecode(utf8.decode(response.bodyBytes));
        throw Exception(error['detail'] ?? 'Failed to load topic summary');
      }
    } on SocketException {
      throw Exception('No internet connection. Please check your network.');
    } on http.ClientException {
      throw Exception('Connection error. Please try again.');
    } catch (e) {
      throw Exception('Failed to load topic summary: ${e.toString()}');
    }
  }

  /// Get list of all topics
  Future<List<Map<String, dynamic>>> getTopics() async {
    try {
      final token = await _storage.getAccessToken();

      if (token == null) {
        throw Exception('No authentication token found. Please login again.');
      }

      final response = await http.get(
        Uri.parse(ApiConfig.contentTopics),
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
        throw Exception('Failed to load topics');
      }
    } on SocketException {
      throw Exception('No internet connection. Please check your network.');
    } on http.ClientException {
      throw Exception('Connection error. Please try again.');
    } catch (e) {
      throw Exception('Failed to load topics: ${e.toString()}');
    }
  }
}
