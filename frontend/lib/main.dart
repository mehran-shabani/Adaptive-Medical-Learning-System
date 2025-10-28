import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/theme/app_theme.dart';
import 'features/auth/login_screen.dart';

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
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AdaptiveMed',
      debugShowCheckedModeBanner: false,
      
      // RTL Support for Persian
      locale: const Locale('fa', 'IR'),
      
      // Material 3 with custom theme
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.light,
      
      // Start with Login screen
      home: const LoginScreen(),
      
      // TODO: Add proper routing with named routes
      // routes: {
      //   '/login': (context) => const LoginScreen(),
      //   '/dashboard': (context) => const DashboardScreen(),
      //   '/study-plan': (context) => const StudyPlanScreen(),
      //   '/quiz': (context) => const QuizScreen(),
      //   '/summary': (context) => const SummaryScreen(),
      // },
    );
  }
}
