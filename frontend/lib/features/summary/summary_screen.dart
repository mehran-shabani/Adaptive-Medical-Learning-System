import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'summary_provider.dart';
import '../../widgets/keypoint_card.dart';

/// Summary screen showing topic content with citations
///
/// Displays:
/// - Key clinical points
/// - High-yield traps and tips
/// - Source citations for transparency
class SummaryScreen extends ConsumerStatefulWidget {
  const SummaryScreen({
    super.key,
    required this.topicId,
  });
  final int topicId;

  @override
  ConsumerState<SummaryScreen> createState() => _SummaryScreenState();
}

class _SummaryScreenState extends ConsumerState<SummaryScreen> {
  @override
  void initState() {
    super.initState();
    // Load summary on screen init
    Future.microtask(() {
      // TODO: Load topic summary
      // ref.read(summaryProvider.notifier).loadSummary(topicId: widget.topicId);
    });
  }

  @override
  Widget build(BuildContext context) {
    // TODO: Watch summary provider state
    // final summaryState = ref.watch(summaryProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('خلاصه مطالب'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Topic title
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'مدیریت کتواسیدوز دیابتی (DKA)', // TODO: Use actual topic name
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),

          // Key points section
          Text(
            'نکات کلیدی',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 8),
          // TODO: Map through actual key points
          const KeypointCard(
            title: 'نکته ۱',
            content: 'هدف اصلی درمان DKA اصلاح کم‌آبی و اسیدوز است',
          ),
          const KeypointCard(
            title: 'نکته ۲',
            content:
                'شروع انسولین قبل از احیای مایع در کودکان می‌تواند خطر ادم مغزی را افزایش دهد',
          ),
          const KeypointCard(
            title: 'نکته ۳',
            content: 'مونیتورینگ دقیق الکترولیت‌ها ضروری است',
          ),

          const SizedBox(height: 24),

          // High-yield traps section
          Text(
            'دام‌های تستی (High-Yield)',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 8),
          Card(
            color: Colors.orange[50],
            child: const Padding(
              padding: EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.warning, color: Colors.orange),
                      SizedBox(width: 8),
                      Text(
                        'دام رایج',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                  SizedBox(height: 8),
                  Text(
                    'بیکربنات وریدی معمولاً در DKA کودکان توصیه نمی‌شود مگر در موارد خاص',
                  ),
                ],
              ),
            ),
          ),

          const SizedBox(height: 24),

          // Citations section
          Text(
            'منابع و استنادات',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 8),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // TODO: Map through actual citations
                  _buildCitation('Harrison 21e p.304-305'),
                  const Divider(),
                  _buildCitation('Cecil 27e p.1121'),
                ],
              ),
            ),
          ),

          const SizedBox(height: 24),

          // Start quiz button
          ElevatedButton.icon(
            onPressed: () {
              // TODO: Navigate to quiz for this topic
              // Navigator.of(context).push(
              //   MaterialPageRoute(
              //     builder: (context) => QuizScreen(topicId: widget.topicId),
              //   ),
              // );
            },
            icon: const Icon(Icons.quiz),
            label: const Text('شروع تست این موضوع'),
          ),
        ],
      ),
    );
  }

  Widget _buildCitation(String reference) => Row(
        children: [
          const Icon(Icons.book, size: 16),
          const SizedBox(width: 8),
          Text(reference),
        ],
      );
}
