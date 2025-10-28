import 'dart:convert';
import 'package:http/http.dart' as http;
import '../storage/secure_storage.dart';

/// Dashboard/Mastery API service
/// 
/// Fetches user mastery data for dashboard display.
class DashboardApiService {
  // TODO: Update with actual backend URL
  static const String baseUrl = 'http://localhost:8000/api/v1';
  
  final SecureStorageService _storage = SecureStorageService();
  
  /// Get user mastery dashboard
  /// 
  /// GET /user/{id}/mastery
  /// Headers: Authorization: Bearer <JWT>
  /// Response: { "user_id": 42, "topics": [...] }
  Future<Map<String, dynamic>> getUserMastery(int userId) async {
    final token = await _storage.getAccessToken();
    
    if (token == null) {
      throw Exception('No authentication token found');
    }
    
    final response = await http.get(
      Uri.parse('$baseUrl/mastery/$userId'),
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
      throw Exception('Failed to load mastery data: ${response.body}');
    }
  }
}
