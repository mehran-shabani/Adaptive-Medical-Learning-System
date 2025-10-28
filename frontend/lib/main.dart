import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/theme/app_theme.dart';
import 'features/auth/login_screen.dart';
import 'features/dashboard/dashboard_screen.dart';
import 'features/study_plan/study_plan_screen.dart';
import 'features/quiz/quiz_screen.dart';
import 'features/summary/summary_screen.dart';

/// Main entry point for AdaptiveMed Flutter application
///
/// This app provides adaptive learning for Iranian medical students
/// preparing for board exams.
void main() {
  runApp(
    const ProviderScope(
      child: AdaptiveMedApp(),
    ),
  );
}

class AdaptiveMedApp extends StatelessWidget {
  const AdaptiveMedApp({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'AdaptiveMed',
        debugShowCheckedModeBanner: false,

        // RTL Support for Persian
        locale: const Locale('fa', 'IR'),

        // Material 3 with custom theme
        theme: AppTheme.lightTheme,
        darkTheme: AppTheme.darkTheme,
        themeMode: ThemeMode.light,

        // Start with Login screen
        initialRoute: '/login',

        // Named routes
        routes: {
          '/login': (context) => const LoginScreen(),
          '/dashboard': (context) => const DashboardScreen(),
          '/study-plan': (context) => const StudyPlanScreen(),
        },

        // Route generator for routes with parameters (quiz and summary need topicId)
        onGenerateRoute: (settings) {
          if (settings.name == '/quiz') {
            final args = settings.arguments as Map<String, dynamic>?;
            final topicId = args?['topicId'] as int? ?? 1;
            return MaterialPageRoute(
              builder: (context) => QuizScreen(topicId: topicId),
              settings: settings,
            );
          }
          if (settings.name == '/summary') {
            final args = settings.arguments as Map<String, dynamic>?;
            final topicId = args?['topicId'] as int? ?? 1;
            return MaterialPageRoute(
              builder: (context) => SummaryScreen(topicId: topicId),
              settings: settings,
            );
          }
          return null;
        },
      );
}
