"""
Pydantic schemas for quiz endpoints.
"""

from datetime import datetime

from pydantic import BaseModel, Field, validator


class QuestionOption(BaseModel):
    """Single question option."""

    label: str = Field(..., description="Option label (A, B, C, D)")
    text: str = Field(..., description="Option text")


class QuizQuestionResponse(BaseModel):
    """Schema for quiz question (without correct answer)."""

    id: int
    topic_id: int
    stem: str
    options: list[QuestionOption]
    difficulty: str

    class Config:
        from_attributes = True


class QuizQuestionDetailResponse(BaseModel):
    """Schema for quiz question with correct answer and explanation."""

    id: int
    topic_id: int
    stem: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    explanation: str | None
    difficulty: str
    created_at: datetime

    class Config:
        from_attributes = True


class QuizGenerateRequest(BaseModel):
    """Schema for generating quiz questions."""

    topic_id: int = Field(..., description="Topic to generate questions for")
    count: int = Field(5, ge=1, le=20, description="Number of questions")
    difficulty: str | None = Field(None, description="Filter by difficulty")

    @validator("difficulty")
    def validate_difficulty(cls, v):
        if v and v not in ["easy", "medium", "hard"]:
            raise ValueError("Difficulty must be easy, medium, or hard")
        return v


class QuizAnswerSubmit(BaseModel):
    """Schema for submitting quiz answer."""

    user_id: int = Field(..., description="User ID")
    question_id: int = Field(..., description="Question ID")
    chosen_option: str = Field(..., description="Chosen option (A, B, C, D)")
    response_time_sec: float | None = Field(None, ge=0, description="Time taken in seconds")

    @validator("chosen_option")
    def validate_option(cls, v):
        if v.upper() not in ["A", "B", "C", "D"]:
            raise ValueError("Option must be A, B, C, or D")
        return v.upper()


class QuizAnswerResponse(BaseModel):
    """Schema for quiz answer result."""

    answer_id: int
    correct: bool
    correct_option: str
    explanation: str | None
    user_answer: str

    # Mastery update info
    topic_id: int
    new_mastery_score: float


class QuizStatistics(BaseModel):
    """Schema for user's quiz statistics."""

    user_id: int
    total_questions: int
    correct_answers: int
    accuracy: float
    average_response_time: float
    by_difficulty: dict


class QuestionCreate(BaseModel):
    """Schema for creating a question manually."""

    topic_id: int
    stem: str = Field(..., min_length=10)
    option_a: str = Field(..., min_length=1)
    option_b: str = Field(..., min_length=1)
    option_c: str = Field(..., min_length=1)
    option_d: str = Field(..., min_length=1)
    correct_option: str = Field(..., pattern="^[A-D]$")
    explanation: str | None = None
    difficulty: str = Field("medium", pattern="^(easy|medium|hard)$")
