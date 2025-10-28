# Adaptive Medical Learning System - Backend

An intelligent, personalized learning platform for medical students that adapts to their knowledge gaps and learning patterns.

## Overview

This FastAPI-based backend provides:

- **Adaptive Learning**: Personalized study recommendations based on mastery levels
- **Content Management**: PDF ingestion with intelligent chunking and vector embeddings
- **Quiz Generation**: AI-powered multiple-choice questions from medical content
- **Mastery Tracking**: Real-time tracking of student proficiency across medical topics
- **Smart Recommendations**: 2-hour study plans leveraging spaced repetition

## Architecture

The system consists of the following modules:

- **Auth**: OTP-based authentication with JWT tokens
- **Users**: Student profile management (academic level, target specialty)
- **Content**: PDF ingestion, text extraction, chunking, and embedding generation
- **Quiz**: MCQ generation and answer tracking
- **Mastery**: Student proficiency tracking per topic
- **Recommender**: Adaptive study plan generation engine

## Tech Stack

- **Framework**: FastAPI 0.109+
- **Database**: PostgreSQL with pgvector for embeddings
- **ORM**: SQLAlchemy 2.0+ with Alembic migrations
- **Task Queue**: Celery + Redis for async processing
- **AI Integration**: OpenAI API (GPT-4o-mini, text-embedding-3-small)
- **PDF Processing**: PyMuPDF, pdfminer.six

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 14+ with pgvector extension
- Redis 7+

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (copy `.env.example` to `.env`):
```bash
cp .env.example .env
```

5. Configure your `.env` file with:
- Database connection string
- JWT secret key
- OpenAI API key
- Redis connection string

6. Run database migrations:
```bash
alembic upgrade head
```

7. Start the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Setup

```bash
docker-compose up -d
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Key Endpoints

### Authentication
- `POST /auth/login-otp` - Request OTP
- `POST /auth/verify-otp` - Verify OTP and get JWT

### Content Management
- `POST /content/upload-pdf` - Upload medical content PDF
- `GET /content/topic/{topic_id}/summary` - Get topic summary

### Quiz
- `GET /quiz/generate` - Generate quiz questions
- `POST /quiz/answer` - Submit quiz answer

### Student Progress
- `GET /user/{user_id}/mastery` - Get mastery dashboard
- `GET /user/{user_id}/plan` - Get personalized 2-hour study plan

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black app/
flake8 app/
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── db.py                   # Database session management
│   ├── auth/                   # Authentication module
│   ├── users/                  # User management module
│   ├── content/                # Content ingestion & retrieval
│   ├── quiz/                   # Quiz generation & tracking
│   ├── mastery/                # Mastery tracking module
│   ├── recommender/            # Adaptive recommendation engine
│   └── utils/                  # Shared utilities
├── migrations/                 # Alembic migrations
├── requirements.txt
├── docker-compose.yml
└── Dockerfile
```

## License

[Your License Here]

## Contributors

[Your Team]
