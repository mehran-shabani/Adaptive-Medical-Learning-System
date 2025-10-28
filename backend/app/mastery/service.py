"""
Mastery service layer for tracking and updating proficiency.
"""

import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.content.models import Topic
from app.mastery.models import Mastery
from app.mastery.schemas import MasteryScore, TopicMasteryDetail, UserMasteryDashboard
from app.quiz.models import QuizAnswer
from app.users.models import User
from app.utils.timestamps import days_since, utcnow

logger = logging.getLogger(__name__)


class MasteryService:
    """Service class for mastery tracking operations."""

    @staticmethod
    def get_or_create_mastery(user_id: int, topic_id: int, db: Session) -> Mastery:
        """
        Get existing mastery record or create new one.

        Args:
            user_id: User ID
            topic_id: Topic ID
            db: Database session

        Returns:
            Mastery: Mastery record
        """
        mastery = db.query(Mastery).filter(Mastery.user_id == user_id, Mastery.topic_id == topic_id).first()

        if not mastery:
            mastery = Mastery(
                user_id=user_id,
                topic_id=topic_id,
                mastery_score=settings.MASTERY_INITIAL_SCORE,
                review_count=0,
                created_at=utcnow(),
            )
            db.add(mastery)
            db.commit()
            db.refresh(mastery)
            logger.info(f"Created new mastery record: user={user_id}, topic={topic_id}")

        return mastery

    @staticmethod
    def update_mastery_from_quiz(user_id: int, topic_id: int, correct: bool, db: Session) -> Mastery:
        """
        Update mastery score based on quiz result.

        Uses incremental learning algorithm:
        - Correct answer: increase score
        - Incorrect answer: decrease score
        - Score bounded between 0.0 and 1.0

        Args:
            user_id: User ID
            topic_id: Topic ID
            correct: Whether answer was correct
            db: Database session

        Returns:
            Mastery: Updated mastery record
        """
        mastery = MasteryService.get_or_create_mastery(user_id, topic_id, db)

        old_score = mastery.mastery_score

        if correct:
            # Increase score with diminishing returns as score approaches 1.0
            increment = settings.MASTERY_CORRECT_INCREMENT * (1.0 - mastery.mastery_score)
            mastery.mastery_score = min(1.0, mastery.mastery_score + increment)
        else:
            # Decrease score
            mastery.mastery_score = max(0.0, mastery.mastery_score - settings.MASTERY_INCORRECT_DECREMENT)

        mastery.last_reviewed_at = utcnow()
        mastery.review_count += 1

        db.commit()
        db.refresh(mastery)

        logger.info(
            f"Updated mastery: user={user_id}, topic={topic_id}, "
            f"old={old_score:.3f}, new={mastery.mastery_score:.3f}, correct={correct}"
        )

        return mastery

    @staticmethod
    def get_user_mastery_dashboard(user_id: int, db: Session) -> UserMasteryDashboard:
        """
        Get comprehensive mastery dashboard for user.

        Args:
            user_id: User ID
            db: Database session

        Returns:
            UserMasteryDashboard: Dashboard with all mastery metrics

        Raises:
            HTTPException: If user not found
        """
        # Validate user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Get all mastery records for user
        masteries = db.query(Mastery).filter(Mastery.user_id == user_id).all()

        if not masteries:
            # Return empty dashboard
            return UserMasteryDashboard(
                user_id=user_id,
                overall_mastery=0.0,
                total_topics=0,
                strong_topics=[],
                weak_topics=[],
                recent_activity=[],
                by_system={},
            )

        # Calculate overall mastery
        overall_mastery = sum(m.mastery_score for m in masteries) / len(masteries)

        # Get topic names
        topic_map = {
            topic.id: topic for topic in db.query(Topic).filter(Topic.id.in_([m.topic_id for m in masteries])).all()
        }

        # Create mastery scores with topic info
        mastery_scores = []
        for m in masteries:
            topic = topic_map.get(m.topic_id)
            if topic:
                mastery_scores.append(
                    MasteryScore(
                        topic_id=m.topic_id,
                        topic_name=topic.name,
                        system_name=topic.system_name,
                        mastery_score=m.mastery_score,
                        last_reviewed_at=m.last_reviewed_at,
                        review_count=m.review_count,
                    )
                )

        # Categorize topics
        strong_topics = [m for m in mastery_scores if m.mastery_score >= settings.MASTERY_WEAK_THRESHOLD]
        weak_topics = [m for m in mastery_scores if m.mastery_score < settings.MASTERY_WEAK_THRESHOLD]

        # Sort by score
        strong_topics.sort(key=lambda x: x.mastery_score, reverse=True)
        weak_topics.sort(key=lambda x: x.mastery_score)

        # Recent activity (last reviewed)
        recent_activity = sorted(
            [m for m in mastery_scores if m.last_reviewed_at], key=lambda x: x.last_reviewed_at, reverse=True
        )[:10]

        # Group by system
        by_system = {}
        for m in mastery_scores:
            system = m.system_name or "General"
            if system not in by_system:
                by_system[system] = {"count": 0, "average_mastery": 0.0, "topics": []}
            by_system[system]["count"] += 1
            by_system[system]["topics"].append(m.mastery_score)

        # Calculate averages
        for system in by_system:
            scores = by_system[system]["topics"]
            by_system[system]["average_mastery"] = sum(scores) / len(scores)
            del by_system[system]["topics"]  # Remove detailed scores

        return UserMasteryDashboard(
            user_id=user_id,
            overall_mastery=round(overall_mastery, 3),
            total_topics=len(masteries),
            strong_topics=strong_topics[:10],  # Top 10
            weak_topics=weak_topics[:10],  # Bottom 10
            recent_activity=recent_activity,
            by_system=by_system,
        )

    @staticmethod
    def get_topic_mastery_detail(user_id: int, topic_id: int, db: Session) -> TopicMasteryDetail:
        """
        Get detailed mastery information for a specific topic.

        Args:
            user_id: User ID
            topic_id: Topic ID
            db: Database session

        Returns:
            TopicMasteryDetail: Detailed mastery information
        """
        mastery = MasteryService.get_or_create_mastery(user_id, topic_id, db)

        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")

        # Get quiz statistics for this topic
        from app.quiz.models import QuizQuestion

        quiz_answers = (
            db.query(QuizAnswer)
            .join(QuizQuestion)
            .filter(QuizAnswer.user_id == user_id, QuizQuestion.topic_id == topic_id)
            .all()
        )

        total_questions = len(quiz_answers)
        correct_answers = sum(1 for a in quiz_answers if a.correct)
        accuracy = correct_answers / total_questions if total_questions > 0 else 0.0

        # Determine if needs review
        needs_review = False
        recommended_action = "Keep learning"

        if mastery.mastery_score < settings.MASTERY_WEAK_THRESHOLD:
            needs_review = True
            recommended_action = "Study content and practice more questions"
        elif (
            mastery.last_reviewed_at
            and days_since(mastery.last_reviewed_at) > settings.SPACED_REPETITION_THRESHOLD_DAYS
        ):
            needs_review = True
            recommended_action = "Review for spaced repetition"

        return TopicMasteryDetail(
            topic_id=topic_id,
            topic_name=topic.name,
            mastery_score=mastery.mastery_score,
            last_reviewed_at=mastery.last_reviewed_at,
            review_count=mastery.review_count,
            total_questions_answered=total_questions,
            correct_answers=correct_answers,
            accuracy=round(accuracy, 3),
            needs_review=needs_review,
            recommended_action=recommended_action,
        )

    @staticmethod
    def get_weak_topics_for_review(user_id: int, limit: int, db: Session) -> list[Mastery]:
        """
        Get topics that need review based on mastery and time since last review.

        Prioritizes:
        1. Low mastery scores
        2. Topics not reviewed recently (spaced repetition)

        Args:
            user_id: User ID
            limit: Maximum number of topics to return
            db: Database session

        Returns:
            List[Mastery]: Topics needing review
        """
        # Get all user's masteries
        masteries = db.query(Mastery).filter(Mastery.user_id == user_id).all()

        # Score each mastery for priority
        scored_masteries = []
        for m in masteries:
            priority_score = 0.0

            # Low mastery score contributes to priority
            priority_score += (1.0 - m.mastery_score) * 100

            # Time since last review contributes to priority
            if m.last_reviewed_at:
                days = days_since(m.last_reviewed_at)
                priority_score += min(days * 5, 50)  # Cap at 50 points
            else:
                priority_score += 50  # Never reviewed

            scored_masteries.append((priority_score, m))

        # Sort by priority (descending) and return top N
        scored_masteries.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored_masteries[:limit]]
