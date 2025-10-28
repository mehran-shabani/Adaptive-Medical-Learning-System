import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/api/content_api_service.dart';
import '../../core/models/summary_model.dart';

/// Summary state provider
final summaryProvider = StateNotifierProvider<SummaryNotifier, SummaryState>((ref) {
  return SummaryNotifier();
});

/// Summary state
class SummaryState {
  final SummaryModel? summary;
  final bool isLoading;
  final String? errorMessage;
  
  SummaryState({
    this.summary,
    this.isLoading = false,
    this.errorMessage,
  });
  
  SummaryState copyWith({
    SummaryModel? summary,
    bool? isLoading,
    String? errorMessage,
  }) {
    return SummaryState(
      summary: summary ?? this.summary,
      isLoading: isLoading ?? this.isLoading,
      errorMessage: errorMessage ?? this.errorMessage,
    );
  }
}

/// Summary notifier
class SummaryNotifier extends StateNotifier<SummaryState> {
  final ContentApiService _contentService = ContentApiService();
  
  SummaryNotifier() : super(SummaryState());
  
  /// Load topic summary with citations
  Future<void> loadSummary({required int topicId}) async {
    state = state.copyWith(isLoading: true, errorMessage: null);
    
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
