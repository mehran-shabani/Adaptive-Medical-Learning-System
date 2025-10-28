/// Topic summary model with citations
class SummaryModel {
  SummaryModel({
    required this.topic,
    required this.keyPoints,
    required this.highYieldTraps,
    required this.citations,
  });

  factory SummaryModel.fromJson(Map<String, dynamic> json) => SummaryModel(
      topic: json['topic_name'] as String,
      keyPoints: (json['key_points'] as List).cast<String>(),
      highYieldTraps: (json['high_yield_traps'] as List?)
              ?.map((trap) => trap['description'] as String)
              .toList() ??
          [],
      citations: (json['citations'] as List?)
              ?.map((citation) =>
                  CitationModel.fromJson(citation as Map<String, dynamic>),)
              .toList() ??
          [],
    );
  final String topic;
  final List<String> keyPoints;
  final List<String> highYieldTraps;
  final List<CitationModel> citations;
}

/// Citation model
class CitationModel {
  CitationModel({
    required this.sourceReference,
    required this.chunkId,
  });

  factory CitationModel.fromJson(Map<String, dynamic> json) => CitationModel(
      sourceReference: json['source_reference'] as String,
      chunkId: json['chunk_id'] as int,
    );
  final String sourceReference;
  final int chunkId;
}
