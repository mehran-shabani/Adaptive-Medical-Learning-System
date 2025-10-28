"""
Database initialization script.
Creates tables and optionally loads sample data.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.config import settings
from app.content.models import Topic
from app.db import Base, SessionLocal, engine
from app.users.models import User
from app.utils.timestamps import utcnow


def init_database():
    """Initialize database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")


def load_sample_data():
    """Load sample data for testing."""
    print("\nLoading sample data...")

    db = SessionLocal()

    try:
        # Create sample topics
        topics = [
            Topic(
                name="Diabetic Ketoacidosis (DKA)",
                system_name="Endocrine",
                description="Acute metabolic complication of diabetes",
                created_at=utcnow(),
            ),
            Topic(
                name="Acute Kidney Injury (AKI)",
                system_name="Renal",
                description="Sudden decrease in kidney function",
                created_at=utcnow(),
            ),
            Topic(
                name="Myocardial Infarction",
                system_name="Cardiovascular",
                description="Heart attack - coronary artery occlusion",
                created_at=utcnow(),
            ),
            Topic(
                name="Sepsis and Septic Shock",
                system_name="Infectious Disease",
                description="Life-threatening organ dysfunction due to infection",
                created_at=utcnow(),
            ),
            Topic(
                name="Stroke - Ischemic",
                system_name="Neurology",
                description="Cerebral ischemia due to arterial occlusion",
                created_at=utcnow(),
            ),
        ]

        for topic in topics:
            db.add(topic)

        db.commit()
        print(f"✓ Created {len(topics)} sample topics")

        # Create sample user
        user = User(
            phone_number="09123456789",
            name="Medical Student Demo",
            study_level="intern",
            target_specialty="internal_medicine",
            created_at=utcnow(),
        )
        db.add(user)
        db.commit()
        print(f"✓ Created sample user (phone: {user.phone_number})")

        print("\n✓ Sample data loaded successfully!")
        print("\nYou can now:")
        print("1. Login with phone: 09123456789")
        print("2. Upload PDF content for topics")
        print("3. Generate quiz questions")
        print("4. Get personalized study plans")

    except Exception as e:
        print(f"✗ Error loading sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=================================")
    print("Database Initialization")
    print("=================================")
    print(f"Database URL: {settings.DATABASE_URL}")
    print()

    response = input("This will create/recreate all tables. Continue? (yes/no): ")

    if response.lower() in ["yes", "y"]:
        init_database()

        load_sample = input("\nLoad sample data? (yes/no): ")
        if load_sample.lower() in ["yes", "y"]:
            load_sample_data()

        print("\n✓ Initialization complete!")
    else:
        print("Cancelled.")
