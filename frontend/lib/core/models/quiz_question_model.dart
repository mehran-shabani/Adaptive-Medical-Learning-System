/// Quiz question model
class QuizQuestionModel {
  final int questionId;
  final String stem;
  final List<QuizOption> options;
  
  QuizQuestionModel({
    required this.questionId,
    required this.stem,
    required this.options,
  });
  
  factory QuizQuestionModel.fromJson(Map<String, dynamic> json) {
    return QuizQuestionModel(
      questionId: json['id'] as int,
      stem: json['stem'] as String,
      options: (json['options'] as List)
          .map((opt) => QuizOption.fromJson(opt as Map<String, dynamic>))
          .toList(),
    );
  }
}

/// Quiz option model
class QuizOption {
  final String label;
  final String text;
  
  QuizOption({
    required this.label,
    required this.text,
  });
  
  factory QuizOption.fromJson(Map<String, dynamic> json) {
    return QuizOption(
      label: json['label'] as String,
      text: json['text'] as String,
    );
  }
}
