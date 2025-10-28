import 'package:adaptivemed_mobile/widgets/plan_block_card.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Study plan screen showing recommended study blocks
///
/// Displays 120-minute personalized study plan with:
/// - Topics prioritized by spaced repetition
/// - Time allocation for each topic
/// - Priority level (HIGH/MEDIUM/LOW)
/// - Reasoning for inclusion
class StudyPlanScreen extends ConsumerStatefulWidget {
  const StudyPlanScreen({super.key});

  @override
  ConsumerState<StudyPlanScreen> createState() => _StudyPlanScreenState();
}

class _StudyPlanScreenState extends ConsumerState<StudyPlanScreen> {
  @override
  void initState() {
    super.initState();
    // Load study plan on screen init
    Future.microtask(() {
      // TODO: Load study plan
      // ref.read(studyPlanProvider.notifier).loadPlan(userId: 1);
    });
  }

  @override
  Widget build(BuildContext context) {
    // TODO: Watch study plan provider state
    // final planState = ref.watch(studyPlanProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('برنامه مطالعه'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              // TODO: Regenerate plan
              // ref.read(studyPlanProvider.notifier).loadPlan(userId: 1);
            },
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Plan header
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'برنامه مطالعه ۱۲۰ دقیقه',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'این برنامه بر اساس میزان تسلط و زمان مرور قبلی شما طراحی شده است.',
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),

          // Study blocks
          // TODO: Map through actual plan blocks
          const PlanBlockCard(
            topic: 'مدیریت کتواسیدوز دیابتی (DKA)',
            priority: 'HIGH',
            durationMinutes: 30,
            currentMastery: 0.45,
            reason: 'تسلط پایین + مدت زمان طولانی از آخرین مرور',
          ),
          const PlanBlockCard(
            topic: 'نارسایی حاد کلیوی (AKI)',
            priority: 'MEDIUM',
            durationMinutes: 30,
            currentMastery: 0.65,
            reason: 'نیاز به مرور دوره‌ای',
          ),
          const PlanBlockCard(
            topic: 'شوک سپتیک و هیپوولمی',
            priority: 'HIGH',
            durationMinutes: 25,
            currentMastery: 0.38,
            reason: 'تسلط پایین',
          ),

          const SizedBox(height: 24),

          // Start studying button
          ElevatedButton.icon(
            onPressed: () {
              // TODO: Start first study block
              // Navigate to summary screen for first topic
            },
            icon: const Icon(Icons.play_arrow),
            label: const Text('شروع مطالعه'),
          ),
        ],
      ),
    );
  }
}
