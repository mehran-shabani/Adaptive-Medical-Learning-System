/// Study plan model
class StudyPlanModel {
  final int durationMinutes;
  final List<StudyBlockModel> blocks;
  
  StudyPlanModel({
    required this.durationMinutes,
    required this.blocks,
  });
  
  factory StudyPlanModel.fromJson(Map<String, dynamic> json) {
    return StudyPlanModel(
      durationMinutes: json['duration_minutes'] as int,
      blocks: (json['blocks'] as List)
          .map((block) => StudyBlockModel.fromJson(block as Map<String, dynamic>))
          .toList(),
    );
  }
}

/// Individual study block within a plan
class StudyBlockModel {
  final int topicId;
  final String topic;
  final int durationMinutes;
  final String reviewMaterial;
  final String priority;
  final String reason;
  final double currentMastery;
  
  StudyBlockModel({
    required this.topicId,
    required this.topic,
    required this.durationMinutes,
    required this.reviewMaterial,
    required this.priority,
    required this.reason,
    required this.currentMastery,
  });
  
  factory StudyBlockModel.fromJson(Map<String, dynamic> json) {
    return StudyBlockModel(
      topicId: json['topic_id'] as int,
      topic: json['topic'] as String,
      durationMinutes: json['duration_minutes'] as int,
      reviewMaterial: json['review_material'] as String? ?? '',
      priority: json['priority'] as String,
      reason: json['reason'] as String? ?? '',
      currentMastery: (json['current_mastery'] as num?)?.toDouble() ?? 0.0,
    );
  }
}
