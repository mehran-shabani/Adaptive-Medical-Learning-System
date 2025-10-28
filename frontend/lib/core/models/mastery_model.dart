/// Mastery model for user proficiency tracking
class MasteryModel {
  final int topicId;
  final String topicName;
  final String systemName;
  final double masteryScore;
  final String? lastReviewedAt;
  
  MasteryModel({
    required this.topicId,
    required this.topicName,
    required this.systemName,
    required this.masteryScore,
    this.lastReviewedAt,
  });
  
  factory MasteryModel.fromJson(Map<String, dynamic> json) {
    return MasteryModel(
      topicId: json['topic_id'] as int,
      topicName: json['topic_name'] as String,
      systemName: json['system_name'] as String,
      masteryScore: (json['mastery_score'] as num).toDouble(),
      lastReviewedAt: json['last_reviewed_at'] as String?,
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'topic_id': topicId,
      'topic_name': topicName,
      'system_name': systemName,
      'mastery_score': masteryScore,
      'last_reviewed_at': lastReviewedAt,
    };
  }
}
