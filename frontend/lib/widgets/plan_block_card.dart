import 'package:flutter/material.dart';

/// Widget for displaying a study plan block
class PlanBlockCard extends StatelessWidget {
  const PlanBlockCard({
    required this.topic,
    required this.priority,
    required this.durationMinutes,
    required this.currentMastery,
    required this.reason,
    super.key,
  });
  final String topic;
  final String priority;
  final int durationMinutes;
  final double currentMastery;
  final String reason;

  @override
  Widget build(BuildContext context) => Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Topic title with priority badge
              Row(
                children: [
                  Expanded(
                    child: Text(
                      topic,
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                  ),
                  _buildPriorityBadge(),
                ],
              ),
              const SizedBox(height: 12),

              // Duration and mastery info
              Row(
                children: [
                  const Icon(Icons.schedule, size: 16),
                  const SizedBox(width: 4),
                  Text('$durationMinutes دقیقه'),
                  const SizedBox(width: 16),
                  const Icon(Icons.bar_chart, size: 16),
                  const SizedBox(width: 4),
                  Text('تسلط: ${(currentMastery * 100).toInt()}٪'),
                ],
              ),
              const SizedBox(height: 8),

              // Reason for inclusion
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.blue[50],
                  borderRadius: BorderRadius.circular(4),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.info_outline, size: 16),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        reason,
                        style: const TextStyle(fontSize: 12),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      );

  Widget _buildPriorityBadge() {
    Color color;
    String text;

    switch (priority.toUpperCase()) {
      case 'HIGH':
        color = Colors.red;
        text = 'اولویت بالا';
        break;
      case 'MEDIUM':
        color = Colors.orange;
        text = 'اولویت متوسط';
        break;
      case 'LOW':
        color = Colors.green;
        text = 'اولویت پایین';
        break;
      default:
        color = Colors.grey;
        text = priority;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.2),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Text(
        text,
        style: TextStyle(
          color: color,
          fontWeight: FontWeight.bold,
          fontSize: 12,
        ),
      ),
    );
  }
}
