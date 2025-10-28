import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/api/plan_api_service.dart';
import '../../core/models/study_plan_model.dart';

/// Study plan state provider
final studyPlanProvider =
    StateNotifierProvider<StudyPlanNotifier, StudyPlanState>(
        (ref) => StudyPlanNotifier());

/// Study plan state
class StudyPlanState {
  StudyPlanState({
    this.plan,
    this.isLoading = false,
    this.errorMessage,
  });
  final StudyPlanModel? plan;
  final bool isLoading;
  final String? errorMessage;

  StudyPlanState copyWith({
    StudyPlanModel? plan,
    bool? isLoading,
    String? errorMessage,
  }) =>
      StudyPlanState(
        plan: plan ?? this.plan,
        isLoading: isLoading ?? this.isLoading,
        errorMessage: errorMessage ?? this.errorMessage,
      );
}

/// Study plan notifier
class StudyPlanNotifier extends StateNotifier<StudyPlanState> {
  StudyPlanNotifier() : super(StudyPlanState());
  final PlanApiService _planService = PlanApiService();

  /// Load study plan for user
  Future<void> loadPlan({
    int durationMinutes = 120,
    bool includeQuiz = true,
  }) async {
    state = state.copyWith(isLoading: true, errorMessage: null);

    try {
      final data = await _planService.getStudyPlan(
        durationMinutes: durationMinutes,
        includeQuiz: includeQuiz,
      );

      final plan = StudyPlanModel.fromJson(data);

      state = state.copyWith(
        plan: plan,
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
