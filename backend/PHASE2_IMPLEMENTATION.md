# Phase 2 Backend Implementation Complete

This document summarizes the Phase 2 enhancements to the AdaptiveMed backend.

## ✅ Completed Features

### 1. Role Management & Access Control
- ✅ Added `UserRole` enum (student, faculty, admin) to User model
- ✅ Created `require_role()` dependency for FastAPI route protection
- ✅ Added `get_current_user_from_token()` for JWT validation
- ✅ JWT tokens now include role information
- ✅ Upload PDF restricted to faculty/admin only
- ✅ All protected routes require Bearer JWT

### 2. Task Queue & Job Tracking
- ✅ Created `IngestionJob` model with status tracking
- ✅ Statuses: queued → running → done/error
- ✅ Added `GET /content/ingestion-status/{job_id}` endpoint
- ✅ Ingestion service creates and updates job status
- ✅ Error handling with error_message logging

### 3. Study Logging
- ✅ `StudyPlanLog` already existed and is saved after plan generation
- ✅ `QuizAnswer` saved after each answer submission
- ✅ Mastery updated after quiz submission
- ✅ `last_reviewed_at` set to now() after quiz

### 4. Spaced Repetition Logic
- ✅ Added `calculate_review_priority()` method to StudyPlanner
- ✅ Algorithm:
  - mastery < 0.7 & not reviewed for >2 days → HIGH
  - mastery 0.7-0.85 & not reviewed for >7 days → MEDIUM
  - mastery >= 0.85 → LOW (only if explicitly requested)
- ✅ Priority reflected in study plan blocks

### 5. Content Summaries with Citations
- ✅ Added `CitationInfo` schema
- ✅ Added `citations` array to `TopicSummaryResponse`
- ✅ Citations include source_reference and chunk_id
- ✅ Example: `{"source_reference": "Harrison 21e p.304-305", "chunk_id": 182}`

### 6. LLM Hallucination Restrictions
- ✅ Created `app/content/llm_client.py` with centralized LLM client
- ✅ Added `MEDICAL_CONTENT_SYSTEM_PROMPT` constant:
  - Only use provided chunks
  - Do not invent drug names or guidelines
  - If insufficient source, return "INSUFFICIENT_SOURCE"
- ✅ Updated ContentService to use LLMClient
- ✅ Updated QuizService to use LLMClient

### 7. Pagination/Filtering in Quiz
- ✅ `GET /quiz/generate` supports:
  - `topic_id` (required)
  - `limit` parameter (default 5, max 20)
  - `difficulty` filter (easy/medium/hard)
- ✅ All generated questions saved to DB with question_id

### 8. Healthcheck & Versioning
- ✅ Updated `/health` endpoint:
  ```json
  {"status": "ok", "version": "0.1.0"}
  ```
- ✅ Public endpoint (no auth required)
- ✅ Version 0.1.0 noted as in development

### 9. Security Enhancements
Protected endpoints (require Bearer JWT):
- ✅ `/content/topics/{id}/summary`
- ✅ `/content/ingestion-status/{job_id}`
- ✅ `/content/search`
- ✅ `/quiz/generate`
- ✅ `/quiz/answer`
- ✅ `/recommender/{user_id}/plan`
- ✅ `/mastery/{user_id}`
- ✅ `/mastery/{user_id}/topic/{topic_id}`

Public endpoints (no auth):
- `/auth/login-otp`
- `/auth/verify-otp`
- `/health`
- `/`

### 10. Copyright & Data Privacy
- ✅ Added comments in `ingestion.py`:
  - PDF files must be legally licensed
  - Raw PDF stored in persistent storage
  - Each chunk has `source_reference` metadata
  - Citations for transparency and legal compliance

## API Contract Compliance

### Authentication
```
POST /auth/verify-otp
Response: {
  "access_token": "<JWT>",
  "user_id": 42,
  "role": "student"
}
```

### Mastery Dashboard
```
GET /user/{user_id}/mastery
Authorization: Bearer <JWT>
Response: {
  "user_id": 42,
  "topics": [
    {
      "topic_id": 10,
      "topic_name": "نارسایی قلبی حاد",
      "system_name": "قلب",
      "mastery_score": 0.62,
      "last_reviewed_at": "2025-10-20T14:21:00Z"
    }
  ]
}
```

### Study Plan
```
GET /recommender/{user_id}/plan
Authorization: Bearer <JWT>
Response: {
  "duration_minutes": 120,
  "blocks": [
    {
      "topic": "DKA Management",
      "priority": "HIGH",
      "study_minutes": 30,
      "spaced_repetition_reason": "low mastery + long since last review"
    }
  ]
}
```

### Quiz
```
GET /quiz/generate?topic_id=5&limit=5&difficulty=medium
Authorization: Bearer <JWT>

POST /quiz/answer
Authorization: Bearer <JWT>
Body: {
  "user_id": 42,
  "question_id": 771,
  "chosen_option": "A",
  "response_time_sec": 41
}
```

### Content Summary with Citations
```
GET /content/topic/10/summary
Authorization: Bearer <JWT>
Response: {
  "topic": "DKA Management",
  "key_points": ["..."],
  "high_yield_traps": ["..."],
  "citations": [
    {
      "source_reference": "Harrison 21e p.304-305",
      "chunk_id": 182
    }
  ]
}
```

## Database Migrations Required

New models added:
1. `IngestionJob` table
2. `User.role` column
3. Updated `Chunk` metadata structure for citations

Run migrations:
```bash
cd backend
alembic revision --autogenerate -m "Phase 2: Add role, ingestion jobs, citations"
alembic upgrade head
```

## Testing

All endpoints require testing with:
- Valid JWT tokens
- Role-based access (student vs faculty)
- Error cases (expired tokens, missing auth)

## Next Steps for Frontend

The backend is now ready for frontend integration. All API contracts match the specifications in the original prompt document.
