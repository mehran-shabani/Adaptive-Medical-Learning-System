"""
Study plan generation logic using adaptive learning algorithms.
"""
from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from app.mastery.models import Mastery
from app.mastery.service import MasteryService
from app.content.models import Topic
from app.config import settings
from app.utils.timestamps import utcnow, days_since

logger = logging.getLogger(__name__)


class StudyPlanner:
    """
    Adaptive study planner using spaced repetition and mastery-based prioritization.
    
    Algorithm:
    1. Get all user's masteries
    2. Score topics based on:
       - Low mastery score (weak areas)
       - Time since last review (spaced repetition)
       - Never studied topics
    3. Allocate time across selected topics
    4. For each topic: review content + practice questions
    """
    
    def __init__(self, db: Session):
        """
        Initialize study planner.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def generate_study_plan(
        self,
        user_id: int,
        duration_minutes: int,
        focus_topics: Optional[List[int]] = None
    ) -> dict:
        """
        Generate adaptive study plan for user.
        
        Args:
            user_id: User ID
            duration_minutes: Available study time
            focus_topics: Optional list of topic IDs to focus on
            
        Returns:
            dict: Study plan with ordered blocks
            
        Example:
            plan = planner.generate_study_plan(user_id=1, duration_minutes=120)
        """
        logger.info(f"Generating {duration_minutes}min study plan for user {user_id}")
        
        # Step 1: Get topics needing review
        if focus_topics:
            # Use specified topics
            topics_to_study = self._get_specific_topics(user_id, focus_topics)
        else:
            # Use adaptive selection
            topics_to_study = self._select_topics_for_study(user_id, duration_minutes)
        
        if not topics_to_study:
            return self._create_empty_plan(user_id, duration_minutes)
        
        # Step 2: Allocate time across topics
        time_allocation = self._allocate_time(topics_to_study, duration_minutes)
        
        # Step 3: Create study blocks
        study_blocks = []
        for (topic, mastery, priority), allocated_minutes in zip(topics_to_study, time_allocation):
            block = self._create_study_block(
                topic=topic,
                mastery=mastery,
                allocated_minutes=allocated_minutes,
                priority=priority
            )
            study_blocks.append(block)
        
        # Step 4: Assemble complete plan
        plan = {
            "user_id": user_id,
            "duration_minutes": duration_minutes,
            "generated_at": utcnow(),
            "blocks": study_blocks,
            "total_topics": len(study_blocks),
            "focus_areas": [block["topic"] for block in study_blocks[:3]],
            "average_current_mastery": sum(b["current_mastery"] for b in study_blocks) / len(study_blocks) if study_blocks else 0.0
        }
        
        logger.info(f"Generated plan with {len(study_blocks)} study blocks")
        return plan
    
    def _select_topics_for_study(
        self,
        user_id: int,
        duration_minutes: int
    ) -> List[Tuple[Topic, Mastery, str]]:
        """
        Select topics for study using adaptive algorithm.
        
        Returns list of (topic, mastery, priority_level) tuples.
        """
        # Get weak topics that need review
        weak_masteries = MasteryService.get_weak_topics_for_review(
            user_id=user_id,
            limit=10,
            db=self.db
        )
        
        # Get topic objects
        topic_ids = [m.topic_id for m in weak_masteries]
        topics = self.db.query(Topic).filter(Topic.id.in_(topic_ids)).all()
        topic_map = {t.id: t for t in topics}
        
        # Create tuples with priority
        selected = []
        for mastery in weak_masteries:
            topic = topic_map.get(mastery.topic_id)
            if not topic:
                continue
            
            # Determine priority using spaced repetition algorithm
            priority = self.calculate_review_priority(mastery)
            
            selected.append((topic, mastery, priority))
        
        # Limit based on available time (rough estimate: 30-40 min per topic)
        max_topics = max(3, duration_minutes // 35)
        return selected[:max_topics]
    
    def _get_specific_topics(
        self,
        user_id: int,
        topic_ids: List[int]
    ) -> List[Tuple[Topic, Mastery, str]]:
        """Get specific topics requested by user."""
        topics = self.db.query(Topic).filter(Topic.id.in_(topic_ids)).all()
        
        result = []
        for topic in topics:
            mastery = MasteryService.get_or_create_mastery(user_id, topic.id, self.db)
            priority = self.calculate_review_priority(mastery)
            result.append((topic, mastery, priority))
        
        return result
    
    def _allocate_time(
        self,
        topics: List[Tuple[Topic, Mastery, str]],
        total_minutes: int
    ) -> List[int]:
        """
        Allocate study time across topics based on priority.
        
        Higher priority (weaker topics) get more time.
        """
        if not topics:
            return []
        
        # Assign weights based on priority (case-insensitive)
        priority_weights = {
            "HIGH": 1.5,
            "high": 1.5,
            "MEDIUM": 1.0,
            "medium": 1.0,
            "LOW": 0.7,
            "low": 0.7
        }
        
        weights = [priority_weights[priority] for _, _, priority in topics]
        total_weight = sum(weights)
        
        # Allocate proportionally
        allocations = []
        remaining = total_minutes
        
        for i, weight in enumerate(weights):
            if i == len(weights) - 1:
                # Give remaining time to last topic
                allocations.append(remaining)
            else:
                allocated = int((weight / total_weight) * total_minutes)
                allocated = max(20, allocated)  # Minimum 20 minutes
                allocations.append(allocated)
                remaining -= allocated
        
        return allocations
    
    def _create_study_block(
        self,
        topic: Topic,
        mastery: Mastery,
        allocated_minutes: int,
        priority: str
    ) -> dict:
        """
        Create a study block for a topic.
        
        Divides time between content review and quiz practice.
        """
        # Determine time split
        if mastery.mastery_score < 0.3:
            # Very weak: more content review
            review_minutes = int(allocated_minutes * 0.6)
            quiz_minutes = allocated_minutes - review_minutes
        elif mastery.mastery_score < 0.7:
            # Medium: balanced
            review_minutes = int(allocated_minutes * 0.5)
            quiz_minutes = allocated_minutes - review_minutes
        else:
            # Strong: more practice
            review_minutes = int(allocated_minutes * 0.4)
            quiz_minutes = allocated_minutes - review_minutes
        
        # Determine reason for inclusion
        reason = self._get_recommendation_reason(mastery)
        
        # Get number of questions (roughly 1-2 min per question)
        num_questions = max(3, quiz_minutes // 2)
        
        block = {
            "topic_id": topic.id,
            "topic": topic.name,
            "duration_minutes": allocated_minutes,
            "review_material": f"Review {topic.name} for {review_minutes} minutes",
            "quiz_questions": [],  # Will be populated by service layer
            "quiz_question_count": num_questions,
            "current_mastery": round(mastery.mastery_score, 3),
            "reason": reason,
            "priority": priority
        }
        
        return block
    
    def _get_recommendation_reason(self, mastery: Mastery) -> str:
        """
        Get human-readable reason for recommending this topic.
        
        Implements spaced repetition logic based on:
        - Mastery score (< 0.7 = weak, 0.7-0.85 = medium, >= 0.85 = strong)
        - Days since last review
        - Review history
        """
        reasons = []
        
        if mastery.mastery_score < 0.5:
            reasons.append("Low mastery - needs foundational review")
        elif mastery.mastery_score < settings.MASTERY_WEAK_THRESHOLD:
            reasons.append("Below target mastery")
        
        if mastery.last_reviewed_at:
            days = days_since(mastery.last_reviewed_at)
            if days > settings.SPACED_REPETITION_THRESHOLD_DAYS:
                reasons.append(f"Not reviewed for {days} days - spaced repetition")
        else:
            reasons.append("Never reviewed - new topic")
        
        return " | ".join(reasons) if reasons else "Recommended for review"
    
    def calculate_review_priority(self, mastery: Mastery) -> str:
        """
        Calculate review priority using spaced repetition principles.
        
        Algorithm:
        - If mastery_score < 0.7 and days_since(last_reviewed) > 2 → HIGH priority
        - If mastery_score 0.7-0.85 and days_since(last_reviewed) > 7 → MEDIUM priority  
        - If mastery_score >= 0.85 → LOW priority (only if user explicitly requests)
        
        Args:
            mastery: Mastery record
            
        Returns:
            str: Priority level ("HIGH", "MEDIUM", "LOW")
        """
        if mastery.last_reviewed_at:
            days = days_since(mastery.last_reviewed_at)
        else:
            days = 9999  # Never reviewed
        
        # High priority: weak mastery + not reviewed recently
        if mastery.mastery_score < 0.7 and days > 2:
            return "HIGH"
        
        # Medium priority: medium mastery + not reviewed in a week
        if 0.7 <= mastery.mastery_score < 0.85 and days > 7:
            return "MEDIUM"
        
        # Low priority: strong mastery (only review if explicitly requested)
        if mastery.mastery_score >= 0.85:
            return "LOW"
        
        # Default to medium
        return "MEDIUM"
    
    def _create_empty_plan(self, user_id: int, duration_minutes: int) -> dict:
        """Create empty plan when no topics available."""
        return {
            "user_id": user_id,
            "duration_minutes": duration_minutes,
            "generated_at": utcnow(),
            "blocks": [],
            "total_topics": 0,
            "focus_areas": [],
            "average_current_mastery": 0.0,
            "message": "No topics available for study. Start by uploading content or taking quizzes."
        }


# TODO: Implement more sophisticated algorithms:
# - SuperMemo SM-2 algorithm for spaced repetition
# - Leitner system for flashcard-style review
# - Confidence-based learning
# - Topic dependency graphs (e.g., must master Topic A before Topic B)
# - Learning style adaptation
