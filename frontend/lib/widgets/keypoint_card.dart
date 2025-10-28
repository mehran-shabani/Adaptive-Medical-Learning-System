import 'package:flutter/material.dart';

/// Widget for displaying a key point in topic summary
class KeypointCard extends StatelessWidget {
  final String title;
  final String content;
  
  const KeypointCard({
    super.key,
    required this.title,
    required this.content,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Bullet point
            Container(
              margin: const EdgeInsets.only(top: 4),
              width: 8,
              height: 8,
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.primary,
                shape: BoxShape.circle,
              ),
            ),
            const SizedBox(width: 12),
            
            // Content
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (title.isNotEmpty) ...[
                    Text(
                      title,
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 4),
                  ],
                  Text(content),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
