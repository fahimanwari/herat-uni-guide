import uuid
from datetime import datetime

from sqlalchemy import String, Text, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    faculty_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("faculties.id"))
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    # Three-language
    name_fa: Mapped[str] = mapped_column(String(200))
    name_ps: Mapped[str | None] = mapped_column(String(200))
    name_en: Mapped[str | None] = mapped_column(String(200))
    description_fa: Mapped[str] = mapped_column(Text)
    description_ps: Mapped[str | None] = mapped_column(Text)
    description_en: Mapped[str | None] = mapped_column(Text)

    # ⭐ Hierarchy: 'degree' = graduable (selectable in Kankor)
    #                 'service' = service-only (cannot be selected)
    department_type: Mapped[str] = mapped_column(
        String(10), default="degree", index=True
    )
    vision_fa: Mapped[str | None] = mapped_column(Text)
    mission_fa: Mapped[str | None] = mapped_column(Text)

    duration_years: Mapped[int] = mapped_column(Integer, default=4)
    degree_type: Mapped[str] = mapped_column(String(50), default="لیسانس")
    subjects: Mapped[list] = mapped_column(JSON, default=list)
    career_paths: Mapped[list] = mapped_column(JSON, default=list)
    required_skills: Mapped[list] = mapped_column(JSON, default=list)
    suitable_for: Mapped[list] = mapped_column(JSON, default=list)
    job_market_fa: Mapped[str | None] = mapped_column(Text)
    difficulty_level: Mapped[str | None] = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    faculty = relationship("Faculty", back_populates="departments")
    student_projects = relationship("StudentProject", back_populates="department")
    alumni_stories = relationship("AlumniStory", back_populates="department")
    career_roadmaps = relationship("CareerRoadmap", back_populates="department")
    cutoffs = relationship("KankorCutoff", back_populates="department")


class StudentProject(Base):
    __tablename__ = "student_projects"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    department_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("departments.id"))
    title_fa: Mapped[str] = mapped_column(String(300))
    description_fa: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(500))
    students: Mapped[str | None] = mapped_column(String(300))
    year: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    department = relationship("Department", back_populates="student_projects")


class AlumniStory(Base):
    __tablename__ = "alumni_stories"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    department_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("departments.id"))
    full_name: Mapped[str] = mapped_column(String(200))
    graduation_year: Mapped[int] = mapped_column(Integer)
    current_position: Mapped[str] = mapped_column(String(300))
    story_fa: Mapped[str] = mapped_column(Text)
    photo_url: Mapped[str | None] = mapped_column(String(500))
    youtube_video_id: Mapped[str | None] = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    department = relationship("Department", back_populates="alumni_stories")


class CareerRoadmap(Base):
    __tablename__ = "career_roadmaps"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    department_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("departments.id"))
    career_title_fa: Mapped[str] = mapped_column(String(200))
    steps: Mapped[list] = mapped_column(JSON, default=list)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    department = relationship("Department", back_populates="career_roadmaps")
