import 'package:flutter/material.dart';

/// Widget for displaying mastery progress for a body system
class MasteryCard extends StatelessWidget {
  const MasteryCard({
    super.key,
    required this.systemName,
    required this.masteryScore,
    this.lastReviewedDaysAgo,
  });
  final String systemName;
  final double masteryScore;
  final int? lastReviewedDaysAgo;

  @override
  Widget build(BuildContext context) => Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // System name
              Text(
                systemName,
                style: Theme.of(context).textTheme.titleMedium,
              ),
              const SizedBox(height: 12),

              // Progress bar
              LinearProgressIndicator(
                value: masteryScore,
                minHeight: 6,
                backgroundColor: Colors.grey[200],
                color: _getColorForScore(masteryScore),
              ),
              const SizedBox(height: 8),

              // Score percentage and last reviewed
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    '${(masteryScore * 100).toInt()}٪',
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  if (lastReviewedDaysAgo != null)
                    Text(
                      'آخرین مرور: $lastReviewedDaysAgo روز پیش',
                      style: Theme.of(context).textTheme.bodySmall,
                    ),
                ],
              ),
            ],
          ),
        ),
      );

  Color _getColorForScore(double score) {
    if (score >= 0.7) return Colors.green;
    if (score >= 0.5) return Colors.orange;
    return Colors.red;
  }
}
