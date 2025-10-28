# Release Workflow Fixes - Summary

## تغییرات اعمال‌شده (Applied Changes)

### 1. رفع خطای Unstaged Changes (Fixed Unstaged Changes Error)
**مشکل قبلی:**
```
error: cannot pull with rebase: You have unstaged changes.
error: Please commit or stash them.
```

**علت:** فایل VERSION قبل از `git pull` تغییر می‌کرد و باعث ایجاد unstaged changes می‌شد.

**راه‌حل:** ترتیب مراحل در workflow اصلاح شد:

#### ترتیب قبلی (اشتباه):
1. Checkout code
2. Setup Python
3. Get current version
4. Determine bump type
5. **Bump version** ← فایل VERSION تغییر می‌کند
6. Git config
7. **Git pull** ← خطا! فایل VERSION تغییر کرده است

#### ترتیب جدید (صحیح):
1. Checkout code
2. Setup Python
3. **Configure Git** ← تنظیمات git
4. **Pull latest changes** ← قبل از تغییر هر فایلی
5. Get current version
6. Determine bump type
7. **Bump version** ← حالا امن است
8. Get latest tag
9. Generate changelog
10. Commit version bump
11. **Create and push Git tag** ← ایجاد و push tag در یک مرحله

---

## 2. سیستم نسخه‌گذاری خودکار (Auto-Versioning System)

### ورژن اولیه: `1.0.0`
- فایل VERSION در حال حاضر روی `1.0.0` تنظیم شده است
- این ورژن اولیه پروژه خواهد بود

### سیستم افزایش نسخه (Version Increment):

#### برای تغییرات کوچک (Patch):
```
1.0.0  → 1.0.01  (اولین تغییر)
1.0.01 → 1.0.02  (دومین تغییر)
1.0.02 → 1.0.03  (سومین تغییر)
...
1.0.98 → 1.0.99  (نود و نهمین تغییر)
1.0.99 → 1.1.0   (صدمین تغییر - rollover)
```

**هر push به main**: ورژن به صورت خودکار +0.01 افزایش می‌یابد

#### برای تغییرات بزرگ‌تر:

**Minor Version** (افزایش ویژگی):
```
1.0.15 → 1.1.0
```
تشخیص خودکار با commit message های `feat:` یا `feature:`

**Major Version** (تغییرات breaking):
```
1.5.23 → 2.0.0
```
تشخیص خودکار با commit message های `BREAKING CHANGE` یا `major:`

---

## 3. توالی رویدادها در Release Action

### هنگام push به main:
1. ✅ **CI checks** اجرا می‌شود (linting, tests)
2. ✅ **Auto-tag**: ورژن جدید محاسبه و تگ ایجاد می‌شود
3. ✅ **Build Backend**: Docker image ساخته می‌شود
4. ✅ **Build Android**: APK ساخته می‌شود
5. ✅ **Create Release**: GitHub Release با changelog و artifacts

### اجرای دستی (Manual Dispatch):
می‌توانید نوع bump را انتخاب کنید:
- `patch`: +0.01 (پیش‌فرض)
- `minor`: +0.1.0 (ویژگی جدید)
- `major`: +1.0.0 (breaking change)

---

## 4. تست عملکرد (Testing)

### تست افزایش نسخه:
```bash
# از 1.0.0 شروع می‌شود
$ python3 .github/scripts/bump_version.py patch
Current version: 1.0.0
Bumped patch version: 1.0.0 -> 1.0.01
1.0.01

# تست‌های متوالی:
$ for i in {1..5}; do python3 .github/scripts/bump_version.py patch; done
1.0.01
1.0.02
1.0.03
1.0.04
1.0.05
```

---

## 5. فایل‌های تغییریافته

### `.github/workflows/release.yml`
- ✅ جابه‌جایی `git config` و `git pull` قبل از bump
- ✅ حذف `git pull` مجدد در مرحله commit
- ✅ ادغام مراحل tag creation و push

### `.github/scripts/bump_version.py`
- ✅ منطق افزایش 0.01 برای patch
- ✅ فرمت‌بندی صحیح (01, 02, ..., 99)
- ✅ Rollover به minor version در 99

### `VERSION`
- ✅ تنظیم شده روی `1.0.0` (ورژن اولیه)

---

## 6. مثال‌های استفاده

### Commit با auto-patch:
```bash
git add .
git commit -m "fix: resolve login issue"
git push origin main
# → Version: 1.0.0 → 1.0.01
```

### Commit با feature (minor):
```bash
git commit -m "feat: add dark mode support"
git push origin main
# → Version: 1.0.15 → 1.1.0
```

### Manual release با انتخاب bump type:
```bash
# در GitHub Actions:
# Workflow dispatch → Release → انتخاب bump_type (patch/minor/major)
```

---

## نتیجه‌گیری

✅ **مشکل unstaged changes**: حل شد  
✅ **Auto-tagging**: قبل از build ها اجرا می‌شود  
✅ **ورژن اولیه**: 1.0.0  
✅ **افزایش خودکار**: هر تغییر +0.01  
✅ **Changelog**: خودکار از commit messages  
✅ **Artifacts**: Backend Docker + Android APK  

**وضعیت نهایی:** Release workflow آماده استفاده است! 🎉
