# Project Structure

Complete overview of the Adaptive Medical Learning System backend architecture.

## Directory Layout

```
backend/
├── app/                          # Main application code
│   ├── main.py                   # FastAPI application entry point
│   ├── config.py                 # Configuration management
│   ├── db.py                     # Database session management
│   │
│   ├── auth/                     # Authentication module
│   │   ├── router.py             # Auth API endpoints
│   │   ├── service.py            # Auth business logic
│   │   └── schemas.py            # Pydantic schemas
│   │
│   ├── users/                    # User management module
│   │   ├── models.py             # User database models
│   │   ├── router.py             # User API endpoints
│   │   ├── service.py            # User business logic
│   │   └── schemas.py            # Pydantic schemas
│   │
│   ├── content/                  # Content management module
│   │   ├── models.py             # Topic & Chunk models
│   │   ├── router.py             # Content API endpoints
│   │   ├── service.py            # Content business logic
│   │   ├── schemas.py            # Pydantic schemas
│   │   ├── ingestion.py          # PDF ingestion pipeline
│   │   ├── splitter.py           # Text chunking logic
│   │   └── embedding.py          # Embedding generation
│   │
│   ├── quiz/                     # Quiz module
│   │   ├── models.py             # Question & Answer models
│   │   ├── router.py             # Quiz API endpoints
│   │   ├── service.py            # Quiz business logic
│   │   └── schemas.py            # Pydantic schemas
│   │
│   ├── mastery/                  # Mastery tracking module
│   │   ├── models.py             # Mastery & StudyPlanLog models
│   │   ├── router.py             # Mastery API endpoints
│   │   ├── service.py            # Mastery business logic
│   │   └── schemas.py            # Pydantic schemas
│   │
│   ├── recommender/              # Adaptive recommendation engine
│   │   ├── router.py             # Recommender API endpoints
│   │   ├── service.py            # Recommender business logic
│   │   ├── planner.py            # Study plan generation algorithm
│   │   └── schemas.py            # Pydantic schemas
│   │
│   └── utils/                    # Shared utilities
│       ├── security.py           # JWT, password hashing, OTP
│       └── timestamps.py         # Date/time utilities
│
├── migrations/                   # Alembic database migrations
│   ├── env.py                    # Migration environment config
│   ├── script.py.mako            # Migration template
│   └── versions/                 # Migration version files
│
├── scripts/                      # Helper scripts
│   ├── setup.sh                  # Initial setup script
│   └── init_db.py                # Database initialization
│
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker image definition
├── docker-compose.yml            # Multi-container setup
├── alembic.ini                   # Alembic configuration
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── README.md                     # Project documentation
├── QUICKSTART.md                 # Quick start guide
└── PROJECT_STRUCTURE.md          # This file
```

## Module Descriptions

### Auth Module
**Purpose**: Handle user authentication with OTP and JWT

**Key Components**:
- OTP generation and verification (mock in dev, SMS in production)
- JWT token creation and validation
- Bearer token authentication

**API Endpoints**:
- `POST /auth/login-otp` - Request OTP
- `POST /auth/verify-otp` - Verify OTP and get JWT token

### Users Module
**Purpose**: Manage student profiles and preferences

**Key Components**:
- User profile management
- Study level and target specialty tracking
- User statistics and progress

**Database Models**:
- `User`: Student information and preferences

**API Endpoints**:
- `GET /users/{user_id}` - Get user profile
- `PUT /users/{user_id}` - Update user profile
- `GET /users/{user_id}/profile` - Get detailed profile with statistics

### Content Module
**Purpose**: Manage medical content ingestion and retrieval

**Key Components**:
- PDF upload and processing
- Text extraction (PyMuPDF, pdfminer)
- Intelligent text chunking
- Embedding generation (OpenAI)
- Vector storage (pgvector)
- Semantic search

**Database Models**:
- `Topic`: Medical topics (hierarchical)
- `Chunk`: Text segments with embeddings

**API Endpoints**:
- `POST /content/topics` - Create topic
- `GET /content/topics` - List topics
- `POST /content/upload-pdf` - Upload PDF for ingestion
- `GET /content/topics/{topic_id}/summary` - Get AI-generated summary
- `POST /content/search` - Semantic content search

**Processing Pipeline**:
1. PDF Upload → Storage
2. Text Extraction → Raw text
3. Text Splitting → Chunks (300-700 words)
4. Embedding Generation → Vector representations
5. Database Storage → Searchable chunks

### Quiz Module
**Purpose**: Generate and manage quiz questions

**Key Components**:
- AI-powered question generation (GPT-4o-mini)
- Question database
- Answer tracking
- Performance analysis

**Database Models**:
- `QuizQuestion`: MCQ questions (4 options)
- `QuizAnswer`: Student responses

**API Endpoints**:
- `GET /quiz/generate` - Generate/fetch quiz questions
- `POST /quiz/answer` - Submit answer
- `POST /quiz/questions` - Create question manually
- `GET /quiz/questions/{id}` - Get question details

**Question Generation**:
- Based on topic content chunks
- Residency exam level difficulty
- Clinical vignette format
- Four options with one correct answer
- Detailed explanations

### Mastery Module
**Purpose**: Track student proficiency per topic

**Key Components**:
- Mastery score calculation (0.0 to 1.0)
- Performance-based updates
- Progress dashboards
- Weak/strong topic identification

**Database Models**:
- `Mastery`: User-topic proficiency scores
- `StudyPlanLog`: Historical study plans

**API Endpoints**:
- `GET /mastery/{user_id}` - Get mastery dashboard
- `GET /mastery/{user_id}/topic/{topic_id}` - Get topic mastery details

**Algorithm**:
- Correct answer: +increment (diminishing returns near 1.0)
- Incorrect answer: -decrement
- Tracks last review date for spaced repetition

### Recommender Module
**Purpose**: Generate personalized study plans

**Key Components**:
- Adaptive learning algorithm
- Spaced repetition scheduling
- Priority-based topic selection
- Time allocation optimization

**API Endpoints**:
- `GET /recommender/{user_id}/plan` - Generate study plan
- `POST /recommender/{user_id}/plan` - Generate plan (POST version)

**Algorithm**:
1. **Topic Selection**:
   - Low mastery scores (< 0.7)
   - Long since last review (> 2 days)
   - Never studied topics

2. **Prioritization**:
   - High priority: mastery < 0.5
   - Medium priority: mastery < 0.7
   - Low priority: mastery >= 0.7

3. **Time Allocation**:
   - Higher priority → more time
   - Minimum 20 minutes per topic
   - Proportional to priority weights

4. **Study Block Structure**:
   - Content review (40-60% of time)
   - Quiz practice (40-60% of time)
   - Reasoning and recommendations

## Database Schema

### Core Tables

```sql
-- Users
users (
    id, phone_number, name, study_level, 
    target_specialty, created_at, updated_at
)

-- Topics (hierarchical)
topics (
    id, parent_id, name, system_name, 
    source_reference, description, created_at
)

-- Content Chunks with Embeddings
chunks (
    id, topic_id, page_start, page_end, text,
    embedding_vector [1536], source_pdf_path, 
    metadata, created_at
)

-- Quiz Questions
quiz_questions (
    id, topic_id, stem, option_a, option_b, 
    option_c, option_d, correct_option, 
    explanation, difficulty, source_chunk_id, created_at
)

-- Quiz Answers
quiz_answers (
    id, user_id, question_id, chosen_option,
    correct, response_time_sec, created_at
)

-- Mastery Tracking
masteries (
    id, user_id, topic_id, mastery_score,
    last_reviewed_at, review_count, 
    created_at, updated_at
)

-- Study Plan Logs
study_plan_logs (
    id, user_id, plan_json, duration_minutes,
    completed, created_at
)
```

## Configuration

All configuration is managed in `app/config.py` using Pydantic Settings:

- Database connection
- JWT settings
- OpenAI API configuration
- Vector database settings
- File upload limits
- Mastery algorithm parameters
- Recommender settings

## Technology Stack

### Core Framework
- **FastAPI**: Modern, fast web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

### Database
- **PostgreSQL**: Primary database
- **pgvector**: Vector similarity search
- **SQLAlchemy**: ORM
- **Alembic**: Database migrations

### AI/ML
- **OpenAI API**: LLM for summaries and questions
- **text-embedding-3-small**: Text embeddings (1536d)

### Processing
- **PyMuPDF**: PDF text extraction
- **pdfminer.six**: Alternative PDF processor

### Background Tasks
- **Celery**: Distributed task queue
- **Redis**: Message broker

### Security
- **python-jose**: JWT tokens
- **passlib**: Password hashing

## API Design Patterns

### Separation of Concerns
- **Router**: Handle HTTP requests/responses
- **Service**: Business logic
- **Models**: Database schema
- **Schemas**: API contracts (Pydantic)

### Error Handling
- Consistent HTTPException usage
- Proper status codes
- Detailed error messages (in debug mode)

### Authentication
- JWT Bearer token in Authorization header
- Token validation on protected endpoints

### Async Operations
- PDF ingestion runs in background
- Embedding generation batched
- Long-running operations return job IDs

## Development Workflow

1. **Create Feature Branch**
2. **Add/Update Models** → `app/<module>/models.py`
3. **Create Migration** → `alembic revision --autogenerate`
4. **Add Business Logic** → `app/<module>/service.py`
5. **Define API Contract** → `app/<module>/schemas.py`
6. **Implement Endpoints** → `app/<module>/router.py`
7. **Test** → Manual testing via `/docs`
8. **Commit** → Git commit

## Deployment Checklist

- [ ] Change JWT_SECRET_KEY
- [ ] Update database credentials
- [ ] Configure CORS origins
- [ ] Set up SSL/TLS
- [ ] Configure firewall
- [ ] Set up monitoring
- [ ] Configure log aggregation
- [ ] Set up backup strategy
- [ ] Review rate limiting
- [ ] Test error handling
- [ ] Load test critical endpoints

## Future Enhancements

### Planned Features
- [ ] SuperMemo SM-2 algorithm
- [ ] Confidence-based learning
- [ ] Topic dependency graphs
- [ ] Learning style adaptation
- [ ] Image/figure extraction from PDFs
- [ ] Video content support
- [ ] Collaborative learning features
- [ ] Mobile app optimization

### Infrastructure
- [ ] Kubernetes deployment
- [ ] Horizontal scaling
- [ ] CDN for media files
- [ ] Advanced caching
- [ ] Real-time updates (WebSockets)
- [ ] Analytics dashboard
