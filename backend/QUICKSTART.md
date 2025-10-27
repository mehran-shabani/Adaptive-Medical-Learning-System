# Quick Start Guide

Get the Adaptive Medical Learning System up and running in minutes.

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 14+ with pgvector extension
- Redis 7+ (for background tasks)
- OpenAI API key

## Installation

### Option 1: Docker (Recommended)

1. Clone the repository and navigate to backend directory
2. Copy environment file:
```bash
cp .env.example .env
```

3. Edit `.env` and add your OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-key-here
```

4. Start all services:
```bash
docker-compose up -d
```

5. Run migrations:
```bash
docker-compose exec api alembic upgrade head
```

6. Access the API:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### Option 2: Local Setup

1. Run setup script:
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

2. Activate virtual environment:
```bash
source venv/bin/activate
```

3. Edit `.env` with your configuration

4. Start PostgreSQL and Redis

5. Run migrations:
```bash
alembic upgrade head
```

6. (Optional) Load sample data:
```bash
python scripts/init_db.py
```

7. Start the server:
```bash
uvicorn app.main:app --reload
```

## First Steps

### 1. Test the API

Visit http://localhost:8000/docs for interactive API documentation.

### 2. Create a User (via OTP)

```bash
# Request OTP
curl -X POST "http://localhost:8000/api/v1/auth/login-otp" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "09123456789"}'

# In development mode, the OTP will be shown in the response
# Verify OTP and get token
curl -X POST "http://localhost:8000/api/v1/auth/verify-otp" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "09123456789", "otp_code": "123456"}'
```

### 3. Create a Topic

```bash
curl -X POST "http://localhost:8000/api/v1/content/topics" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Diabetic Ketoacidosis",
    "system_name": "Endocrine",
    "description": "Acute metabolic complication of diabetes"
  }'
```

### 4. Upload PDF Content

```bash
curl -X POST "http://localhost:8000/api/v1/content/upload-pdf" \
  -F "file=@/path/to/medical-textbook.pdf" \
  -F "topic_id=1" \
  -F "source_reference=Harrison's Internal Medicine, 21st Ed"
```

### 5. Generate Quiz Questions

```bash
curl -X GET "http://localhost:8000/api/v1/quiz/generate?topic_id=1&count=5"
```

### 6. Get Study Plan

```bash
curl -X GET "http://localhost:8000/api/v1/recommender/1/plan?duration_minutes=120"
```

## Common Issues

### PostgreSQL Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database exists: `createdb adaptive_medical_learning`

### pgvector Extension Missing
```sql
-- Connect to your database and run:
CREATE EXTENSION vector;
```

### Redis Connection Error
- Ensure Redis is running: `redis-cli ping`
- Check REDIS_URL in .env

### OpenAI API Errors
- Verify your API key is valid
- Check you have sufficient credits
- Review rate limits

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black app/
isort app/
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

### Viewing Logs
```bash
# Docker
docker-compose logs -f api

# Local
# Logs appear in console
```

## Next Steps

1. **Customize Configuration**: Review `app/config.py` for tuning parameters
2. **Add Content**: Upload your medical textbook PDFs
3. **Test Frontend**: Connect your Flutter/mobile app
4. **Monitor Performance**: Check API response times and optimize
5. **Deploy**: Follow deployment guide for production setup

## Support

For issues or questions:
- Check documentation in `/docs`
- Review API documentation at `/docs`
- Check logs for error messages
- Review environment configuration

## Security Notes

⚠️ **Before deploying to production:**

1. Change JWT_SECRET_KEY to a secure random value
2. Update database credentials
3. Configure proper CORS origins
4. Enable HTTPS
5. Set up proper firewall rules
6. Review all environment variables
