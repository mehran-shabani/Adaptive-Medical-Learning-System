import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// Secure storage wrapper for sensitive data like JWT tokens
///
/// Uses flutter_secure_storage for encrypted storage on device.
class SecureStorageService {
  static const _storage = FlutterSecureStorage();

  // Storage keys
  static const String _keyAccessToken = 'access_token';
  static const String _keyUserId = 'user_id';
  static const String _keyUserRole = 'user_role';

  /// Save JWT access token securely
  Future<void> saveAccessToken(String token) async {
    await _storage.write(key: _keyAccessToken, value: token);
  }

  /// Retrieve JWT access token
  Future<String?> getAccessToken() async =>
      await _storage.read(key: _keyAccessToken);

  /// Save user ID
  Future<void> saveUserId(int userId) async {
    await _storage.write(key: _keyUserId, value: userId.toString());
  }

  /// Retrieve user ID
  Future<int?> getUserId() async {
    final userIdStr = await _storage.read(key: _keyUserId);
    return userIdStr != null ? int.tryParse(userIdStr) : null;
  }

  /// Save user role
  Future<void> saveUserRole(String role) async {
    await _storage.write(key: _keyUserRole, value: role);
  }

  /// Retrieve user role
  Future<String?> getUserRole() async => await _storage.read(key: _keyUserRole);

  /// Check if user is authenticated (has valid token)
  Future<bool> isAuthenticated() async {
    final token = await getAccessToken();
    return token != null && token.isNotEmpty;
  }

  /// Clear all authentication data (logout)
  Future<void> clearAuthData() async {
    await _storage.delete(key: _keyAccessToken);
    await _storage.delete(key: _keyUserId);
    await _storage.delete(key: _keyUserRole);
  }

  /// Clear all stored data
  Future<void> clearAll() async {
    await _storage.deleteAll();
  }
}
