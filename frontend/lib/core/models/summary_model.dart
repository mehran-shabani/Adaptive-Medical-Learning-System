/// Topic summary model with citations
class SummaryModel {
  final String topic;
  final List<String> keyPoints;
  final List<String> highYieldTraps;
  final List<CitationModel> citations;
  
  SummaryModel({
    required this.topic,
    required this.keyPoints,
    required this.highYieldTraps,
    required this.citations,
  });
  
  factory SummaryModel.fromJson(Map<String, dynamic> json) {
    return SummaryModel(
      topic: json['topic_name'] as String,
      keyPoints: (json['key_points'] as List).cast<String>(),
      highYieldTraps: (json['high_yield_traps'] as List?)
              ?.map((trap) => trap['description'] as String)
              .toList() ??
          [],
      citations: (json['citations'] as List?)
              ?.map((citation) => CitationModel.fromJson(citation as Map<String, dynamic>))
              .toList() ??
          [],
    );
  }
}

/// Citation model
class CitationModel {
  final String sourceReference;
  final int chunkId;
  
  CitationModel({
    required this.sourceReference,
    required this.chunkId,
  });
  
  factory CitationModel.fromJson(Map<String, dynamic> json) {
    return CitationModel(
      sourceReference: json['source_reference'] as String,
      chunkId: json['chunk_id'] as int,
    );
  }
}
