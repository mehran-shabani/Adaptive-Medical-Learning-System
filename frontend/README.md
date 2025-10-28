# AdaptiveMed Mobile (Flutter)

Adaptive Learning Platform for Iranian Medical Students - Mobile Client

## Overview

This is the Flutter (Web/Mobile) frontend for AdaptiveMed, providing a personalized learning experience for Iranian medical students preparing for board exams.

### Features

- 🔐 **OTP Authentication** - Secure login with phone number and OTP
- 📊 **Dashboard** - Visual mastery tracking across body systems
- 📚 **Smart Study Plans** - AI-generated 120-minute study plans using spaced repetition
- ❓ **MCQ Practice** - Clinical vignette-style questions with immediate feedback
- 📖 **Content Summaries** - Key points, high-yield traps, and source citations
- 🌙 **RTL Support** - Full Persian language and right-to-left layout
- 🎨 **Material 3 Design** - Modern, professional medical-themed UI

## Project Structure

```
lib/
├── main.dart                    # App entry point
├── core/
│   ├── api/                     # API service layer
│   │   ├── auth_api_service.dart
│   │   ├── dashboard_api_service.dart
│   │   ├── plan_api_service.dart
│   │   ├── quiz_api_service.dart
│   │   └── content_api_service.dart
│   ├── storage/
│   │   └── secure_storage.dart  # JWT token storage
│   ├── models/                  # Data models
│   │   ├── mastery_model.dart
│   │   ├── study_plan_model.dart
│   │   ├── quiz_question_model.dart
│   │   └── summary_model.dart
│   └── theme/
│       └── app_theme.dart       # Material 3 theme
├── features/
│   ├── auth/                    # Authentication
│   │   ├── login_screen.dart
│   │   └── auth_provider.dart
│   ├── dashboard/               # Mastery dashboard
│   │   ├── dashboard_screen.dart
│   │   └── dashboard_provider.dart
│   ├── study_plan/              # Study plan
│   │   ├── study_plan_screen.dart
│   │   └── study_plan_provider.dart
│   ├── quiz/                    # Quiz/MCQ
│   │   ├── quiz_screen.dart
│   │   └── quiz_provider.dart
│   └── summary/                 # Content summaries
│       ├── summary_screen.dart
│       └── summary_provider.dart
└── widgets/                     # Reusable widgets
    ├── mastery_card.dart
    ├── plan_block_card.dart
    ├── quiz_option_tile.dart
    └── keypoint_card.dart
```

## Tech Stack

- **Framework**: Flutter 3.0+
- **State Management**: Riverpod 2.4+
- **HTTP Client**: Dio 5.3+ / http 1.1+
- **Secure Storage**: flutter_secure_storage 9.0+
- **Persian Date**: shamsi_date 1.0+
- **Material Design**: Material 3

## Getting Started

### Prerequisites

- Flutter SDK 3.0 or higher
- Dart 3.0 or higher
- Android Studio / VS Code with Flutter extension
- Backend API running (see backend/README.md)

### Installation

1. Clone the repository:
```bash
cd frontend
```

2. Install dependencies:
```bash
flutter pub get
```

3. Update API base URL in service files:
```dart
// In each *_api_service.dart file, update:
static const String baseUrl = 'http://your-backend-url/api/v1';
```

4. Run the app:
```bash
# Web
flutter run -d chrome

# Android
flutter run -d android

# iOS
flutter run -d ios
```

## Architecture

### State Management (Riverpod)

Each feature has its own provider for state management:

- `authProvider` - Authentication state (login, logout, user session)
- `dashboardProvider` - Mastery data for dashboard
- `studyPlanProvider` - Personalized study plans
- `quizProvider` - Quiz questions and answers
- `summaryProvider` - Topic summaries with citations

### API Integration

All API calls go through service classes in `core/api/`:

- Authentication with JWT tokens (stored securely)
- Automatic token refresh on 401 errors
- UTF-8 encoding for Persian text

### RTL Support

The app is fully RTL-aware:

- Material 3 automatic RTL layout
- Persian fonts (ready for custom fonts)
- Right-to-left text direction
- Persian date formatting

## API Contract

### Authentication Flow

1. **Request OTP**:
```dart
POST /auth/login-otp
{
  "phone_number": "+98912xxxxxxx"
}
```

2. **Verify OTP**:
```dart
POST /auth/verify-otp
{
  "phone_number": "+98912xxxxxxx",
  "otp_code": "123456"
}
Response: {
  "access_token": "<JWT>",
  "user_id": 42,
  "role": "student"
}
```

### Protected Endpoints

All endpoints except auth require `Authorization: Bearer <JWT>` header:

- `GET /mastery/{user_id}` - Get mastery dashboard
- `GET /recommender/{user_id}/plan` - Get study plan
- `GET /quiz/generate?topic_id=5&limit=5` - Generate quiz
- `POST /quiz/answer` - Submit answer
- `GET /content/topic/{topic_id}/summary` - Get summary

## Development

### Running Tests

```bash
flutter test
```

### Building for Production

```bash
# Android APK
flutter build apk --release

# iOS IPA
flutter build ios --release

# Web
flutter build web --release
```

### Adding Persian Fonts

1. Download Vazir or IRANSans fonts
2. Add to `assets/fonts/`
3. Update `pubspec.yaml`:
```yaml
fonts:
  - family: Vazir
    fonts:
      - asset: fonts/Vazir-Regular.ttf
      - asset: fonts/Vazir-Bold.ttf
        weight: 700
```
4. Update theme in `app_theme.dart`:
```dart
textTheme: ThemeData.light().textTheme.apply(
  fontFamily: 'Vazir',
),
```

## TODO for Production

- [ ] Implement actual API integration (currently skeleton code)
- [ ] Add error handling and retry logic
- [ ] Implement offline support with local caching
- [ ] Add analytics tracking
- [ ] Implement push notifications for study reminders
- [ ] Add dark mode toggle
- [ ] Implement user profile management
- [ ] Add social sharing features
- [ ] Localization support (if needed for English)
- [ ] Performance optimization
- [ ] Accessibility improvements

## Screenshots

(Add screenshots here after UI is complete)

## License

This project is part of the AdaptiveMed platform. See LICENSE file for details.

## Support

For issues or questions, contact the development team.

---

**Version**: 0.1.0  
**Status**: Development (Skeleton Implementation)  
**Last Updated**: 2025-10-28
