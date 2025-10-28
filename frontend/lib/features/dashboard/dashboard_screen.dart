import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../widgets/mastery_card.dart';
import 'dashboard_provider.dart';

/// Dashboard screen showing user mastery across topics
///
/// Displays:
/// - Overall mastery percentage
/// - Mastery breakdown by body system
/// - Progress indicators
/// - Quick navigation to study plan and quiz
class DashboardScreen extends ConsumerStatefulWidget {
  const DashboardScreen({super.key});

  @override
  ConsumerState<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends ConsumerState<DashboardScreen> {
  @override
  void initState() {
    super.initState();
    // Load mastery data on screen init
    Future.microtask(() {
      // TODO: Load user mastery
      // ref.read(dashboardProvider.notifier).loadMastery();
    });
  }

  @override
  Widget build(BuildContext context) {
    // TODO: Watch dashboard provider state
    // final dashboardState = ref.watch(dashboardProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('داشبورد'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              // TODO: Implement logout
              // ref.read(authProvider.notifier).logout();
              // Navigate to login
            },
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          // TODO: Refresh mastery data
          // await ref.read(dashboardProvider.notifier).loadMastery();
        },
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // Overall mastery card
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'میزان تسلط کلی',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 16),
                    // TODO: Display actual mastery percentage
                    LinearProgressIndicator(
                      value: 0.65,
                      minHeight: 8,
                      backgroundColor: Colors.grey[200],
                    ),
                    const SizedBox(height: 8),
                    const Text('۶۵٪'),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // System breakdown section
            Text(
              'تسلط بر اساس سیستم‌های بدن',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 8),

            // TODO: Map through actual mastery data
            // Example mastery cards
            const MasteryCard(
              systemName: 'قلب و عروق',
              masteryScore: 0.72,
              lastReviewedDaysAgo: 3,
            ),
            const MasteryCard(
              systemName: 'کلیه و الکترولیت',
              masteryScore: 0.45,
              lastReviewedDaysAgo: 7,
            ),
            const MasteryCard(
              systemName: 'غدد',
              masteryScore: 0.88,
              lastReviewedDaysAgo: 1,
            ),

            const SizedBox(height: 24),

            // Action buttons
            ElevatedButton.icon(
              onPressed: () {
                // TODO: Navigate to study plan screen
                // Navigator.of(context).push(
                //   MaterialPageRoute(
                //     builder: (context) => const StudyPlanScreen(),
                //   ),
                // );
              },
              icon: const Icon(Icons.school),
              label: const Text('برنامه مطالعه امروز'),
            ),
            const SizedBox(height: 12),
            OutlinedButton.icon(
              onPressed: () {
                // TODO: Navigate to quiz screen
              },
              icon: const Icon(Icons.quiz),
              label: const Text('شروع تست'),
            ),
          ],
        ),
      ),
    );
  }
}
