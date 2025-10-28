# Adaptive Learning Platform for Medical Students

[![CI](https://github.com/your-org/your-repo/workflows/CI/badge.svg)](https://github.com/your-org/your-repo/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This repository contains an **Adaptive Learning System** designed specifically for medical students. The platform intelligently analyzes learning materials, generates personalized quizzes, tracks mastery levels, and recommends optimized study paths.

### Architecture

The project consists of two main modules:

1. **Backend** (`backend/`): FastAPI-based REST API (Python 3.11+)
   - Content ingestion & processing pipeline
   - PDF parsing and chunking
   - Vector embeddings (pgvector)
   - Quiz generation with LLM integration
   - Mastery tracking and analytics
   - Personalized learning path recommendations

2. **Frontend** (`frontend/`): Flutter application (Android & Web)
   - Cross-platform mobile and web support
   - Interactive quiz interface
   - Real-time mastery visualization
   - Study plan management
   - Dashboard with learning analytics

## Adaptive Learning Pipeline

```
PDF Upload → Content Ingestion → Chunking → Embedding → Vector Store
                                                              ↓
Student Profile ← Recommender ← Mastery Tracker ← Quiz Engine
```

1. **Content Ingestion**: Parse and structure PDF materials
2. **Semantic Chunking**: Break content into meaningful segments
3. **Embedding**: Generate vector representations for semantic search
4. **Quiz Generation**: Create adaptive questions based on learning objectives
5. **Mastery Assessment**: Track student understanding per topic
6. **Personalized Recommendations**: Suggest next study materials based on performance

## Versioning & Release Automation

This project uses **Semantic Versioning** with automated release management:

- **Version Format**: `MAJOR.MINOR.PATCH`
- **Special Patch Increment**: Patches increment by `0.01` (e.g., `1.0.01`, `1.0.02`, ..., `1.0.99`, then `1.1.0`)
- **Automation**: Every merge to `main` triggers automatic version bump, tagging, and GitHub Release creation
- **Current Version**: Tracked in [`VERSION`](./VERSION) file at repository root

### Release Artifacts

Each GitHub Release includes:
- 📝 Auto-generated changelog from commits
- 📱 Android APK (`app-release.apk`)
- 🐳 Backend Docker image digest
- 📦 Release notes with all changes since last version

See [`.github/workflows/release.yml`](.github/workflows/release.yml) for implementation details.

## CI/CD Pipeline

### Continuous Integration (`ci.yml`)

Runs on every PR and push to feature branches:
- ✅ Backend linting (Ruff/Flake8)
- ✅ Backend tests with pytest (minimum 85% coverage required)
- ✅ Frontend analysis (`flutter analyze`)
- ✅ Frontend widget/unit tests

### Release Automation (`release.yml`)

Triggers on merge to `main`:
1. Bump version in `VERSION` file
2. Create Git tag (`v1.0.XX`)
3. Generate changelog from commits
4. Build Android APK
5. Build & tag Docker image
6. Create GitHub Release with all artifacts

### Dependency Management

- **Dependabot**: Weekly automated dependency updates for Python (`pip`) and Flutter (`pub`)
- **Security**: Automatic vulnerability scanning and PR creation

## Getting Started

### Prerequisites

- **Backend**: Docker & Docker Compose, or Python 3.11+
- **Frontend**: Flutter SDK 3.0+, Dart 3.0+
- **Database**: PostgreSQL with pgvector extension (included in Docker setup)

### Quick Start with Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/your-org/your-repo.git
cd your-repo

# 2. Configure Backend environment
cd backend
cp env.example .env

# 3. Edit .env file and set:
#   - JWT_SECRET_KEY (generate with: openssl rand -hex 32)
#   - OPENAI_API_KEY (optional for initial testing, required for LLM features)

# 4. Start services
cd ..
docker-compose up -d

# 5. Verify services are running
docker-compose ps

# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Health Check: http://localhost:8000/health
```

### Frontend Setup

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
flutter pub get

# 3. Run the app
flutter run  # For mobile emulator
flutter run -d chrome  # For web

# Note: For Android emulator, API will be accessible at http://10.0.2.2:8000
# For iOS simulator: http://localhost:8000
# For physical device: Use your computer's local IP (e.g., http://192.168.1.100:8000)
```

For detailed setup instructions, see [QUICKSTART.md](./QUICKSTART.md)

### Local Development (Without Docker)

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure .env file
cp env.example .env
# Edit .env with your PostgreSQL connection details

# Initialize database
python scripts/init_db.py

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

Same as above - Flutter setup is independent of backend deployment method.

## Recent Bug Fixes & Improvements

### Backend
- ✅ Fixed Python version in Dockerfile (3.14 → 3.11)
- ✅ Fixed import order in content/router.py  
- ✅ Added comprehensive error handling for OpenAI API
- ✅ Improved CORS configuration for Flutter development
- ✅ Simplified Docker setup (removed optional Celery services for development)
- ✅ Created env.example with comprehensive configuration guide

### Frontend
- ✅ Implemented centralized API configuration (ApiConfig)
- ✅ Added proper error handling to all API services
- ✅ Activated login flow with OTP authentication
- ✅ Implemented named routes and navigation
- ✅ Completed all provider implementations (Dashboard, Quiz, Study Plan)
- ✅ Improved network error messages in Persian

## Security & Data Privacy

⚠️ **Important**: This platform handles sensitive student learning data and potentially copyrighted educational materials.

- Student profiles and mastery data are confidential
- PDF source materials may be subject to copyright restrictions
- **Do NOT** publish proprietary content in public releases
- JWT tokens are securely stored using flutter_secure_storage

See [SECURITY.md](./SECURITY.md) for vulnerability reporting procedures.

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](./CONTRIBUTING.md) before submitting PRs.

### Branch Naming Convention

- `feature/<short-description>`: New features
- `fix/<bug-description>`: Bug fixes
- `infra/<infrastructure-change>`: DevOps/infrastructure updates
- `docs/<documentation-change>`: Documentation only

### Code Quality Standards

- All code must pass CI checks (lint, tests, coverage)
- Minimum 85% test coverage for backend changes
- All PRs require at least one approval
- Commits should follow [Conventional Commits](https://www.conventionalcommits.org/)

## Project Status & Roadmap

### ✅ Completed (v1.0)
- [x] Core backend API with FastAPI
- [x] Content ingestion pipeline
- [x] Quiz generation and mastery tracking
- [x] Flutter mobile app (Android)
- [x] CI/CD automation
- [x] Docker containerization

### 🚧 In Progress
- [ ] Flutter web deployment automation
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

### 📋 Planned
- [ ] iOS support
- [ ] Offline mode for mobile app
- [ ] Collaborative study groups
- [ ] Integration with medical curriculum standards

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

**TODO**: Review copyright restrictions for embedded PDF content and educational materials before public distribution.

## Acknowledgments

Built with ❤️ for medical students worldwide.

## Support

For questions, issues, or feature requests, please [open an issue](https://github.com/your-org/your-repo/issues) using our templates.

---

**Last Updated**: 2025-10-28  
**Current Version**: See [`VERSION`](./VERSION)
