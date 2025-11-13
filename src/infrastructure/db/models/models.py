from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Float,
    Boolean,
    ForeignKey,
    JSON,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import json
from datetime import datetime
from typing import Optional

from ..database import Base  # Import Base from database.py in the parent directory


class Idea(Base):
    __tablename__ = "ideas"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(
        String, nullable=False
    )  # Enum: backlog, refining, ready, implemented, archived
    priority = Column(String, nullable=False)  # Enum: low, medium, high, critical
    category = Column(
        String, nullable=False
    )  # Enum: infrastructure, automation, development, research, optimization
    tags = Column(JSON, default=list)  # Stored as JSON
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    estimated_effort = Column(String)
    dependencies = Column(JSON, default=list)  # Stored as JSON
    acceptance_criteria = Column(JSON, default=list)  # Stored as JSON
    notes = Column(Text)
    author = Column(String)
    open_questions = Column(JSON, default=list)  # Stored as JSON
    next_steps = Column(JSON, default=list)  # Stored as JSON
    target_audience = Column(String)
    benefits = Column(JSON, default=list)  # Stored as JSON
    prerequisites = Column(JSON, default=list)  # Stored as JSON
    github_issue_id = Column(Integer)  # GitHub issue number for sync
    github_synced_at = Column(DateTime)  # Last sync timestamp

    def __repr__(self):
        return f"<Idea(id='{self.id}', title='{self.title}', status='{self.status}')>"


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(
        String, nullable=False
    )  # Enum: planning, active, on_hold, completed, archived
    priority = Column(String, nullable=False)  # Enum: low, medium, high, critical
    category = Column(
        String, nullable=False
    )  # Enum: infrastructure, automation, development, research, optimization
    visibility = Column(String, default="private")  # Enum: private, public
    owner = Column(String, nullable=False)
    team = Column(JSON, default=list)  # List of team members
    tags = Column(JSON, default=list)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    start_date = Column(DateTime)
    target_date = Column(DateTime)
    source_idea = Column(String)  # Reference to idea if converted
    vision = Column(Text)
    objectives = Column(JSON, default=list)
    deliverables = Column(JSON, default=list)
    technologies = Column(JSON, default=list)
    acceptance_criteria = Column(JSON, default=list)
    risks = Column(JSON, default=list)
    progress_percentage = Column(Integer, default=0)
    health_status = Column(
        String, default="healthy"
    )  # Enum: healthy, at_risk, critical
    repository_url = Column(String)
    github_repo_id = Column(Integer)  # GitHub repository ID
    notes = Column(Text)

    # Relationships
    work_items = relationship("WorkItem", back_populates="project")
    milestones = relationship("Milestone", back_populates="project")
    custom_fields = relationship("CustomField", back_populates="project")
    views = relationship("ProjectView", back_populates="project")

    def __repr__(self):
        return f"<Project(id='{self.id}', name='{self.name}', status='{self.status}')>"


class WorkItem(Base):
    __tablename__ = "work_items"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(
        String, nullable=False
    )  # Enum: todo, in_progress, review, done, blocked
    priority = Column(String, nullable=False)  # Enum: low, medium, high, critical
    type = Column(
        String, nullable=False
    )  # Enum: feature, bug, task, research, documentation, infrastructure
    issue_type = Column(String, default="issue")  # Enum: issue, draft, pull_request
    project_id = Column(String, ForeignKey("projects.id"))
    assignee = Column(String)
    author = Column(String)
    labels = Column(JSON, default=list)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    due_date = Column(DateTime)
    estimated_hours = Column(Float)
    actual_hours = Column(Float)
    milestone_id = Column(String, ForeignKey("milestones.id"))
    parent_issue_id = Column(String, ForeignKey("work_items.id"))  # For sub-issues
    dependencies = Column(JSON, default=list)
    acceptance_criteria = Column(JSON, default=list)
    blockers = Column(JSON, default=list)
    notes = Column(Text)
    file_path = Column(String)
    repository_url = Column(String)
    github_issue_id = Column(Integer)  # GitHub issue number for sync
    github_synced_at = Column(DateTime)  # Last sync timestamp
    github_repo_url = Column(String)  # GitHub repository URL
    is_draft = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)

    # Relationships
    project = relationship("Project", back_populates="work_items")
    milestone = relationship("Milestone", back_populates="work_items")
    parent_issue = relationship("WorkItem", remote_side=[id])
    custom_field_values = relationship("CustomFieldValue", back_populates="work_item")

    def __repr__(self):
        return (
            f"<WorkItem(id='{self.id}', title='{self.title}', status='{self.status}')>"
        )


class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    project_id = Column(String, ForeignKey("projects.id"))
    status = Column(
        String, default="pending"
    )  # Enum: pending, in_progress, completed, blocked
    due_date = Column(DateTime)
    completed_date = Column(DateTime)
    progress_percentage = Column(Integer, default=0)
    dependencies = Column(JSON, default=list)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    project = relationship("Project", back_populates="milestones")
    work_items = relationship("WorkItem", back_populates="milestone")

    def __repr__(self):
        return (
            f"<Milestone(id='{self.id}', title='{self.title}', status='{self.status}')>"
        )


class CustomField(Base):
    __tablename__ = "custom_fields"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    field_type = Column(
        String, nullable=False
    )  # Enum: text, number, date, single_select, iteration
    project_id = Column(String, ForeignKey("projects.id"))
    options = Column(JSON)  # For single_select fields
    required = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    project = relationship("Project", back_populates="custom_fields")
    values = relationship("CustomFieldValue", back_populates="field")

    def __repr__(self):
        return f"<CustomField(id='{self.id}', name='{self.name}', type='{self.field_type}')>"


class CustomFieldValue(Base):
    __tablename__ = "custom_field_values"

    id = Column(String, primary_key=True, index=True)
    field_id = Column(String, ForeignKey("custom_fields.id"))
    work_item_id = Column(String, ForeignKey("work_items.id"))
    value = Column(JSON)  # Flexible storage for different field types
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    field = relationship("CustomField", back_populates="values")
    work_item = relationship("WorkItem", back_populates="custom_field_values")

    def __repr__(self):
        return f"<CustomFieldValue(field_id='{self.field_id}', work_item_id='{self.work_item_id}')>"


class ProjectView(Base):
    __tablename__ = "project_views"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    project_id = Column(String, ForeignKey("projects.id"))
    layout = Column(String, default="table")  # Enum: table, board, roadmap
    filters = Column(JSON, default=dict)
    sort_config = Column(JSON, default=dict)
    group_config = Column(JSON, default=dict)
    is_default = Column(Boolean, default=False)
    created_by = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    project = relationship("Project", back_populates="views")

    def __repr__(self):
        return (
            f"<ProjectView(id='{self.id}', name='{self.name}', layout='{self.layout}')>"
        )


class AutomationRule(Base):
    __tablename__ = "automation_rules"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    project_id = Column(String, ForeignKey("projects.id"))
    trigger_type = Column(
        String, nullable=False
    )  # Enum: item_added, item_changed, status_changed
    trigger_conditions = Column(JSON, default=dict)
    actions = Column(JSON, default=list)
    enabled = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return f"<AutomationRule(id='{self.id}', name='{self.name}', enabled='{self.enabled}')>"
