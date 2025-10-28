import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/api/dashboard_api_service.dart';
import '../../core/models/mastery_model.dart';

/// Dashboard state provider
final dashboardProvider = StateNotifierProvider<DashboardNotifier, DashboardState>((ref) {
  return DashboardNotifier();
});

/// Dashboard state
class DashboardState {
  final List<MasteryModel> masteries;
  final bool isLoading;
  final String? errorMessage;
  
  DashboardState({
    this.masteries = const [],
    this.isLoading = false,
    this.errorMessage,
  });
  
  DashboardState copyWith({
    List<MasteryModel>? masteries,
    bool? isLoading,
    String? errorMessage,
  }) {
    return DashboardState(
      masteries: masteries ?? this.masteries,
      isLoading: isLoading ?? this.isLoading,
      errorMessage: errorMessage ?? this.errorMessage,
    );
  }
}

/// Dashboard notifier
class DashboardNotifier extends StateNotifier<DashboardState> {
  final DashboardApiService _dashboardService = DashboardApiService();
  
  DashboardNotifier() : super(DashboardState());
  
  /// Load user mastery data
  Future<void> loadMastery(int userId) async {
    state = state.copyWith(isLoading: true, errorMessage: null);
    
    try {
      final data = await _dashboardService.getUserMastery(userId);
      final topics = (data['topics'] as List?)
              ?.map((topic) => MasteryModel.fromJson(topic as Map<String, dynamic>))
              .toList() ??
          [];
      
      state = state.copyWith(
        masteries: topics,
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: e.toString(),
      );
    }
  }
}
