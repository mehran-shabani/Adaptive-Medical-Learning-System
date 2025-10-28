import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/api/auth_api_service.dart';

/// Auth state provider
/// 
/// Manages authentication state and user session.
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier();
});

/// Authentication state
class AuthState {
  final bool isAuthenticated;
  final int? userId;
  final String? userRole;
  final bool isLoading;
  final String? errorMessage;
  
  AuthState({
    this.isAuthenticated = false,
    this.userId,
    this.userRole,
    this.isLoading = false,
    this.errorMessage,
  });
  
  AuthState copyWith({
    bool? isAuthenticated,
    int? userId,
    String? userRole,
    bool? isLoading,
    String? errorMessage,
  }) {
    return AuthState(
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      userId: userId ?? this.userId,
      userRole: userRole ?? this.userRole,
      isLoading: isLoading ?? this.isLoading,
      errorMessage: errorMessage ?? this.errorMessage,
    );
  }
}

/// Authentication notifier
class AuthNotifier extends StateNotifier<AuthState> {
  final AuthApiService _authService = AuthApiService();
  
  AuthNotifier() : super(AuthState());
  
  /// Request OTP for phone number
  Future<void> requestOTP(String phoneNumber) async {
    state = state.copyWith(isLoading: true, errorMessage: null);
    
    try {
      await _authService.loginWithOTP(phoneNumber);
      state = state.copyWith(isLoading: false);
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: e.toString(),
      );
      rethrow;
    }
  }
  
  /// Verify OTP and authenticate user
  Future<void> verifyOTP(String phoneNumber, String otpCode) async {
    state = state.copyWith(isLoading: true, errorMessage: null);
    
    try {
      final result = await _authService.verifyOTP(phoneNumber, otpCode);
      
      state = state.copyWith(
        isAuthenticated: true,
        userId: result['user_id'] as int,
        userRole: result['role'] as String,
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: e.toString(),
      );
      rethrow;
    }
  }
  
  /// Logout user
  Future<void> logout() async {
    await _authService.logout();
    state = AuthState();
  }
}
