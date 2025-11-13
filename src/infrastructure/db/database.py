from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from pathlib import Path

# SQLite database URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/ai_lab.db")

# Create SQLAlchemy engine
# connect_args={"check_same_thread": False} is needed for SQLite
# when using multiple threads, which is common in web applications.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()


def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database with all tables"""
    # Import all models to ensure they are registered
    from .models import (
        Idea,
        Project,
        WorkItem,
        Milestone,
        CustomField,
        CustomFieldValue,
        ProjectView,
        AutomationRule,
    )

    # Import and setup auto-sync
    from .auto_sync import setup_auto_sync

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized with new SQLAlchemy models")

    # Setup automatic GitHub sync
    setup_auto_sync()
    print("✅ Auto-sync configured for GitHub integration")


def drop_all_tables():
    """Drop all tables (for development/reset)"""
    Base.metadata.drop_all(bind=engine)
    print("🗑️  All database tables dropped")


def reset_db():
    """Reset database by dropping and recreating all tables"""
    drop_all_tables()
    init_db()
