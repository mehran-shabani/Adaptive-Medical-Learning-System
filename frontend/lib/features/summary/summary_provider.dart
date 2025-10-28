import 'package:adaptivemed_mobile/core/api/content_api_service.dart';
import 'package:adaptivemed_mobile/core/models/summary_model.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Summary state provider
final summaryProvider = StateNotifierProvider<SummaryNotifier, SummaryState>(
    (ref) => SummaryNotifier(),);

/// Summary state
class SummaryState {
  SummaryState({
    this.summary,
    this.isLoading = false,
    this.errorMessage,
  });
  final SummaryModel? summary;
  final bool isLoading;
  final String? errorMessage;

  SummaryState copyWith({
    SummaryModel? summary,
    bool? isLoading,
    String? errorMessage,
  }) =>
      SummaryState(
        summary: summary ?? this.summary,
        isLoading: isLoading ?? this.isLoading,
        errorMessage: errorMessage ?? this.errorMessage,
      );
}

/// Summary notifier
class SummaryNotifier extends StateNotifier<SummaryState> {
  SummaryNotifier() : super(SummaryState());
  final ContentApiService _contentService = ContentApiService();

  /// Load topic summary with citations
  Future<void> loadSummary({required int topicId}) async {
    state = state.copyWith(isLoading: true);

    try {
      final data = await _contentService.getTopicSummary(topicId);
      final summary = SummaryModel.fromJson(data);

      state = state.copyWith(
        summary: summary,
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
