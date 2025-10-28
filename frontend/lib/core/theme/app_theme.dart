import 'package:flutter/material.dart';

/// Application theme configuration
///
/// Provides Material 3 theme with RTL support and medical-themed colors.
/// Uses professional, calming colors suitable for medical education.
class AppTheme {
  // Medical theme colors
  static const Color primaryBlue = Color(0xFF1976D2); // Professional blue
  static const Color accentGreen = Color(0xFF4CAF50); // Medical green
  static const Color errorRed = Color(0xFFD32F2F); // Alert red
  static const Color warningOrange = Color(0xFFFF9800); // Warning orange
  static const Color backgroundLight = Color(0xFFFAFAFA); // Light background
  static const Color surfaceWhite = Color(0xFFFFFFFF); // Card surface
  static const Color textPrimary = Color(0xFF212121); // Primary text
  static const Color textSecondary = Color(0xFF757575); // Secondary text

  /// Light theme configuration
  static ThemeData get lightTheme => ThemeData(
        useMaterial3: true,

        // Color scheme
        colorScheme: ColorScheme.fromSeed(
          seedColor: primaryBlue,
          primary: primaryBlue,
          secondary: accentGreen,
          error: errorRed,
          background: backgroundLight,
          surface: surfaceWhite,
        ),

        // App bar theme
        appBarTheme: const AppBarTheme(
          centerTitle: true,
          elevation: 0,
          backgroundColor: primaryBlue,
          foregroundColor: Colors.white,
        ),

        // Card theme
        cardTheme: CardThemeData(
          elevation: 2,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        ),

        // Button themes
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
        ),

        // Text theme (ready for Persian fonts)
        textTheme: const TextTheme(
          displayLarge: TextStyle(
            fontSize: 32,
            fontWeight: FontWeight.bold,
            color: textPrimary,
          ),
          displayMedium: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: textPrimary,
          ),
          titleLarge: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.w600,
            color: textPrimary,
          ),
          bodyLarge: TextStyle(
            fontSize: 16,
            color: textPrimary,
          ),
          bodyMedium: TextStyle(
            fontSize: 14,
            color: textSecondary,
          ),
        ),

        // Input decoration theme
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.grey[50],
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(8),
            borderSide: BorderSide.none,
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(8),
            borderSide: BorderSide(color: Colors.grey[300]!),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(8),
            borderSide: const BorderSide(color: primaryBlue, width: 2),
          ),
          errorBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(8),
            borderSide: const BorderSide(color: errorRed),
          ),
          contentPadding:
              const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        ),
      );

  /// Dark theme configuration (for future use)
  static ThemeData get darkTheme => ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: primaryBlue,
          brightness: Brightness.dark,
        ),
      );
}
