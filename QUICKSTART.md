# Quick Start Guide - Adaptive Medical Learning System

راهنمای سریع برای راه‌اندازی و اجرای پروژه

## پیش‌نیازها

### Backend
- Docker و Docker Compose
- یا Python 3.11+ (برای اجرای بدون Docker)

### Frontend
- Flutter SDK 3.0+ 
- Dart 3.0+
- Android Studio / Xcode (برای اجرا روی emulator/simulator)

## راه‌اندازی سریع Backend

### روش 1: استفاده از Docker (توصیه می‌شود)

```bash
# 1. رفتن به پوشه backend
cd backend

# 2. کپی کردن فایل env.example
cp env.example .env

# یا در Windows:
copy env.example .env

# 3. ویرایش فایل .env و تنظیم موارد زیر:
# - JWT_SECRET_KEY: یک کلید امنیتی تصادفی (با openssl rand -hex 32)
# - OPENAI_API_KEY: کلید API از platform.openai.com (اختیاری برای تست اولیه)

# 4. راه‌اندازی با Docker Compose
cd ..
docker-compose up -d

# 5. بررسی وضعیت سرویس‌ها
docker-compose ps

# 6. مشاهده لاگ‌ها
docker-compose logs -f api
```

Backend روی `http://localhost:8000` در دسترس خواهد بود.
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### روش 2: اجرای Local (بدون Docker)

```bash
# 1. رفتن به پوشه backend
cd backend

# 2. ایجاد virtual environment
python -m venv venv

# فعال‌سازی در Linux/Mac:
source venv/bin/activate

# فعال‌سازی در Windows:
venv\Scripts\activate

# 3. نصب dependencies
pip install -r requirements.txt

# 4. تنظیم متغیرهای محیطی
cp env.example .env
# ویرایش .env و تنظیم DATABASE_URL به PostgreSQL محلی

# 5. اجرای migrations (نیاز به PostgreSQL با pgvector)
# ابتدا PostgreSQL را نصب و راه‌اندازی کنید
python scripts/init_db.py

# 6. اجرای سرور
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## راه‌اندازی Frontend (Flutter)

### مرحله 1: نصب Dependencies

```bash
# رفتن به پوشه frontend
cd frontend

# دریافت packages
flutter pub get
```

### مرحله 2: تنظیم Base URL (اختیاری)

اگر Backend روی کامپیوتر دیگری یا IP خاصی اجرا می‌شود:

```dart
// در فایل lib/core/config/api_config.dart
// می‌توانید custom base URL تنظیم کنید
```

### مرحله 3: اجرای Frontend

```bash
# برای Web
flutter run -d chrome

# برای Android Emulator
flutter run

# برای iOS Simulator (فقط روی macOS)
flutter run -d ios
```

## تست سریع

### تست Backend

```bash
# تست health endpoint
curl http://localhost:8000/health

# یا با مرورگر:
# باز کردن http://localhost:8000/docs
```

### تست Login Flow

1. اپلیکیشن Flutter را باز کنید
2. در صفحه login، شماره موبایل وارد کنید (مثلاً `09123456789`)
3. روی "ارسال کد تایید" کلیک کنید
4. در حالت Development، کد OTP در لاگ Backend نمایش داده می‌شود
5. کد را وارد کرده و روی "تایید کد" کلیک کنید
6. به Dashboard منتقل خواهید شد

## مشکلات رایج

### Backend

**خطا: OpenAI API Key مشخص نشده**
- در فایل `.env` مقدار `OPENAI_API_KEY` را تنظیم کنید
- برای تست اولیه می‌توانید یک کلید dummy استفاده کنید

**خطا: Database connection failed**
- مطمئن شوید PostgreSQL با pgvector extension نصب است
- یا از Docker Compose استفاده کنید که همه چیز را خودکار راه‌اندازی می‌کند

### Frontend

**خطا: Connection refused / No internet**
- مطمئن شوید Backend در حال اجراست
- برای Android Emulator از `http://10.0.2.2:8000` استفاده کنید
- برای iOS Simulator از `http://localhost:8000` استفاده کنید
- برای دستگاه واقعی از IP لوکال کامپیوتر استفاده کنید (مثلاً `http://192.168.1.100:8000`)

**تغییر Base URL برای دستگاه واقعی:**

```dart
// در lib/core/config/api_config.dart
// قبل از استفاده از app:
ApiConfig.setCustomBaseUrl('http://192.168.1.100:8000');
```

## دستورات مفید

### Docker Commands

```bash
# مشاهده لاگ‌های API
docker-compose logs -f api

# Restart کردن سرویس‌ها
docker-compose restart

# متوقف کردن همه سرویس‌ها
docker-compose down

# پاک کردن volumes (حذف داده‌های database)
docker-compose down -v

# Rebuild کردن images
docker-compose build --no-cache
```

### Flutter Commands

```bash
# پاک کردن cache
flutter clean

# دریافت مجدد packages
flutter pub get

# اجرا با hot reload
flutter run

# Build برای release
flutter build apk  # Android
flutter build ios  # iOS
flutter build web  # Web
```

## مراحل بعدی

1. **ایجاد Topics**: از API Docs (`/docs`) برای ایجاد topics استفاده کنید
2. **Upload PDF**: محتوای آموزشی PDF را آپلود کنید
3. **Generate Quiz**: تست‌های خودکار برای topics ایجاد کنید
4. **Study Plan**: برنامه مطالعه شخصی‌سازی شده دریافت کنید

## منابع بیشتر

- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)
- [API Documentation](http://localhost:8000/docs)
- [Project Structure](backend/PROJECT_STRUCTURE.md)

## پشتیبانی

برای گزارش مشکلات یا سوالات، یک Issue در GitHub ایجاد کنید.

