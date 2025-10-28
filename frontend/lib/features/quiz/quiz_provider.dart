import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/api/quiz_api_service.dart';
import '../../core/models/quiz_question_model.dart';

/// Quiz state provider
final quizProvider = StateNotifierProvider<QuizNotifier, QuizState>((ref) {
  return QuizNotifier();
});

/// Quiz state
class QuizState {
  final List<QuizQuestionModel> questions;
  final int currentQuestionIndex;
  final bool isLoading;
  final String? errorMessage;
  final Map<String, dynamic>? lastAnswerResult;
  
  QuizState({
    this.questions = const [],
    this.currentQuestionIndex = 0,
    this.isLoading = false,
    this.errorMessage,
    this.lastAnswerResult,
  });
  
  QuizState copyWith({
    List<QuizQuestionModel>? questions,
    int? currentQuestionIndex,
    bool? isLoading,
    String? errorMessage,
    Map<String, dynamic>? lastAnswerResult,
  }) {
    return QuizState(
      questions: questions ?? this.questions,
      currentQuestionIndex: currentQuestionIndex ?? this.currentQuestionIndex,
      isLoading: isLoading ?? this.isLoading,
      errorMessage: errorMessage ?? this.errorMessage,
      lastAnswerResult: lastAnswerResult ?? this.lastAnswerResult,
    );
  }
}

/// Quiz notifier
class QuizNotifier extends StateNotifier<QuizState> {
  final QuizApiService _quizService = QuizApiService();
  
  QuizNotifier() : super(QuizState());
  
  /// Load quiz questions for topic
  Future<void> loadQuiz({
    required int topicId,
    int limit = 5,
  }) async {
    state = state.copyWith(isLoading: true, errorMessage: null);
    
    try {
      final data = await _quizService.generateQuiz(
        topicId: topicId,
        limit: limit,
      );
      
      final questions = data
          .map((q) => QuizQuestionModel.fromJson(q as Map<String, dynamic>))
          .toList();
      
      state = state.copyWith(
        questions: questions,
        currentQuestionIndex: 0,
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: e.toString(),
      );
    }
  }
  
  /// Submit answer for current question
  Future<void> submitAnswer({
    required int userId,
    required int questionId,
    required String chosenOption,
    required double responseTimeSec,
  }) async {
    try {
      final result = await _quizService.submitAnswer(
        userId: userId,
        questionId: questionId,
        chosenOption: chosenOption,
        responseTimeSec: responseTimeSec,
      );
      
      state = state.copyWith(lastAnswerResult: result);
    } catch (e) {
      state = state.copyWith(errorMessage: e.toString());
    }
  }
  
  /// Move to next question
  void nextQuestion() {
    if (state.currentQuestionIndex < state.questions.length - 1) {
      state = state.copyWith(
        currentQuestionIndex: state.currentQuestionIndex + 1,
        lastAnswerResult: null,
      );
    }
  }
}
