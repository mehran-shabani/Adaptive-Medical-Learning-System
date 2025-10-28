import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/api/dashboard_api_service.dart';
import '../../core/models/mastery_model.dart';

/// Dashboard state provider
final dashboardProvider =
    StateNotifierProvider<DashboardNotifier, DashboardState>(
        (ref) => DashboardNotifier());

/// Dashboard state
class DashboardState {
  DashboardState({
    this.masteries = const [],
    this.isLoading = false,
    this.errorMessage,
  });
  final List<MasteryModel> masteries;
  final bool isLoading;
  final String? errorMessage;

  DashboardState copyWith({
    List<MasteryModel>? masteries,
    bool? isLoading,
    String? errorMessage,
  }) =>
      DashboardState(
        masteries: masteries ?? this.masteries,
        isLoading: isLoading ?? this.isLoading,
        errorMessage: errorMessage ?? this.errorMessage,
      );
}

/// Dashboard notifier
class DashboardNotifier extends StateNotifier<DashboardState> {
  DashboardNotifier() : super(DashboardState());
  final DashboardApiService _dashboardService = DashboardApiService();

  /// Load user mastery data
  Future<void> loadMastery() async {
    state = state.copyWith(isLoading: true, errorMessage: null);

    try {
      final masteryDataList = await _dashboardService.getUserMastery();

      final topics =
          masteryDataList.map((item) => MasteryModel.fromJson(item)).toList();

      state = state.copyWith(
        masteries: topics,
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
}
