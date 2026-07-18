"""initial schema — create all tables

Revision ID: fd0a91205e04
Revises: 
Create Date: 2026-07-17 23:10:33.260813

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fd0a91205e04'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all tables."""
    # Core content tables
    op.create_table('universities',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('slug', sa.VARCHAR(100), unique=True, index=True),
        sa.Column('name_fa', sa.VARCHAR(200), nullable=False),
        sa.Column('name_ps', sa.VARCHAR(200)),
        sa.Column('name_en', sa.VARCHAR(200)),
        sa.Column('description_fa', sa.TEXT(), nullable=False),
        sa.Column('description_ps', sa.TEXT()),
        sa.Column('description_en', sa.TEXT()),
        sa.Column('history_fa', sa.TEXT()),
        sa.Column('chancellor_name', sa.VARCHAR(200)),
        sa.Column('logo_url', sa.VARCHAR(500)),
        sa.Column('established_year', sa.INTEGER()),
        sa.Column('stats', postgresql.JSON()),
        sa.Column('lat', sa.FLOAT()),
        sa.Column('lng', sa.FLOAT()),
        sa.Column('is_active', sa.BOOLEAN(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table('faculties',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('university_id', sa.UUID(), sa.ForeignKey('universities.id'), nullable=False),
        sa.Column('slug', sa.VARCHAR(100), unique=True, index=True),
        sa.Column('sort_order', sa.INTEGER(), server_default='0'),
        sa.Column('name_fa', sa.VARCHAR(200), nullable=False),
        sa.Column('name_ps', sa.VARCHAR(200)),
        sa.Column('name_en', sa.VARCHAR(200)),
        sa.Column('description_fa', sa.TEXT(), nullable=False),
        sa.Column('description_ps', sa.TEXT()),
        sa.Column('description_en', sa.TEXT()),
        sa.Column('vision_fa', sa.TEXT()),
        sa.Column('mission_fa', sa.TEXT()),
        sa.Column('cover_image_url', sa.VARCHAR(500)),
        sa.Column('youtube_video_id', sa.VARCHAR(50)),
        sa.Column('dean_name', sa.VARCHAR(200)),
        sa.Column('established_year', sa.INTEGER()),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table('departments',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('faculty_id', sa.UUID(), sa.ForeignKey('faculties.id'), nullable=False),
        sa.Column('slug', sa.VARCHAR(100), unique=True, index=True),
        sa.Column('name_fa', sa.VARCHAR(200), nullable=False),
        sa.Column('name_ps', sa.VARCHAR(200)),
        sa.Column('name_en', sa.VARCHAR(200)),
        sa.Column('description_fa', sa.TEXT(), nullable=False),
        sa.Column('description_ps', sa.TEXT()),
        sa.Column('description_en', sa.TEXT()),
        sa.Column('department_type', sa.VARCHAR(10), nullable=False, server_default='degree', index=True),
        sa.Column('vision_fa', sa.TEXT()),
        sa.Column('mission_fa', sa.TEXT()),
        sa.Column('duration_years', sa.INTEGER(), server_default='4'),
        sa.Column('degree_type', sa.VARCHAR(50), server_default='لیسانس'),
        sa.Column('subjects', postgresql.JSON(), server_default='[]'),
        sa.Column('career_paths', postgresql.JSON(), server_default='[]'),
        sa.Column('required_skills', postgresql.JSON(), server_default='[]'),
        sa.Column('suitable_for', postgresql.JSON(), server_default='[]'),
        sa.Column('job_market_fa', sa.TEXT()),
        sa.Column('difficulty_level', sa.VARCHAR(50)),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table('student_projects',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('department_id', sa.UUID(), sa.ForeignKey('departments.id'), nullable=False),
        sa.Column('title_fa', sa.VARCHAR(300), nullable=False),
        sa.Column('description_fa', sa.TEXT(), nullable=False),
        sa.Column('image_url', sa.VARCHAR(500)),
        sa.Column('students', sa.VARCHAR(300)),
        sa.Column('year', sa.INTEGER()),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table('alumni_stories',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('department_id', sa.UUID(), sa.ForeignKey('departments.id'), nullable=False),
        sa.Column('full_name', sa.VARCHAR(200), nullable=False),
        sa.Column('graduation_year', sa.INTEGER(), nullable=False),
        sa.Column('current_position', sa.VARCHAR(300), nullable=False),
        sa.Column('story_fa', sa.TEXT(), nullable=False),
        sa.Column('photo_url', sa.VARCHAR(500)),
        sa.Column('youtube_video_id', sa.VARCHAR(50)),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table('career_roadmaps',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('department_id', sa.UUID(), sa.ForeignKey('departments.id'), nullable=False),
        sa.Column('career_title_fa', sa.VARCHAR(200), nullable=False),
        sa.Column('steps', postgresql.JSON(), server_default='[]'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    # News
    op.create_table('news',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('university_id', sa.UUID(), sa.ForeignKey('universities.id')),
        sa.Column('title_fa', sa.VARCHAR(300), nullable=False),
        sa.Column('title_ps', sa.VARCHAR(300)),
        sa.Column('title_en', sa.VARCHAR(300)),
        sa.Column('body_fa', sa.TEXT(), nullable=False),
        sa.Column('body_ps', sa.TEXT()),
        sa.Column('body_en', sa.TEXT()),
        sa.Column('cover_image_url', sa.VARCHAR(500)),
        sa.Column('is_published', sa.BOOLEAN(), nullable=False, server_default='false'),
        sa.Column('published_at', sa.TIMESTAMP()),
        sa.Column('send_notification', sa.BOOLEAN(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    # FAQs
    op.create_table('faqs',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('university_id', sa.UUID(), sa.ForeignKey('universities.id')),
        sa.Column('question_fa', sa.TEXT(), nullable=False),
        sa.Column('answer_fa', sa.TEXT(), nullable=False),
        sa.Column('question_ps', sa.TEXT()),
        sa.Column('answer_ps', sa.TEXT()),
        sa.Column('question_en', sa.TEXT()),
        sa.Column('answer_en', sa.TEXT()),
        sa.Column('category', sa.VARCHAR(100)),
        sa.Column('sort_order', sa.INTEGER(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    # Kankor
    op.create_table('kankor_cutoffs',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('department_id', sa.UUID(), sa.ForeignKey('departments.id'), nullable=False),
        sa.Column('year', sa.INTEGER(), nullable=False),
        sa.Column('min_score', sa.Float(), nullable=False),
        sa.Column('capacity', sa.INTEGER()),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table('kankor_guides',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('title_fa', sa.VARCHAR(300), nullable=False),
        sa.Column('body_fa', sa.TEXT(), nullable=False),
        sa.Column('category', sa.VARCHAR(100)),
        sa.Column('sort_order', sa.INTEGER(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    # Quiz
    op.create_table('quiz_questions',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('question_fa', sa.TEXT(), nullable=False),
        sa.Column('category', sa.VARCHAR(100)),
        sa.Column('sort_order', sa.INTEGER(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table('quiz_options',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('question_id', sa.UUID(), sa.ForeignKey('quiz_questions.id'), nullable=False),
        sa.Column('text_fa', sa.VARCHAR(300), nullable=False),
        sa.Column('trait_weights', postgresql.JSON(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table('department_trait_profiles',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('department_id', sa.UUID(), sa.ForeignKey('departments.id'), nullable=False, unique=True),
        sa.Column('trait_weights', postgresql.JSON(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    # Exams
    op.create_table('exams',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('title_fa', sa.VARCHAR(300), nullable=False),
        sa.Column('title_en', sa.VARCHAR(300)),
        sa.Column('description_fa', sa.TEXT()),
        sa.Column('category', sa.VARCHAR(100), nullable=False),
        sa.Column('year', sa.INTEGER()),
        sa.Column('duration_minutes', sa.INTEGER(), nullable=False),
        sa.Column('total_questions', sa.INTEGER(), nullable=False),
        sa.Column('passing_score', sa.Float(), nullable=False),
        sa.Column('max_score', sa.Float(), nullable=False, server_default='100'),
        sa.Column('is_active', sa.BOOLEAN(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table('exam_questions',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('exam_id', sa.UUID(), sa.ForeignKey('exams.id'), nullable=False),
        sa.Column('question_fa', sa.TEXT(), nullable=False),
        sa.Column('question_en', sa.TEXT()),
        sa.Column('sort_order', sa.INTEGER(), nullable=False, server_default='0'),
        sa.Column('points', sa.INTEGER(), nullable=False, server_default='1'),
        sa.Column('subject', sa.VARCHAR(50)),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table('exam_options',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('question_id', sa.UUID(), sa.ForeignKey('exam_questions.id'), nullable=False),
        sa.Column('text_fa', sa.VARCHAR(500), nullable=False),
        sa.Column('text_en', sa.VARCHAR(500)),
        sa.Column('is_correct', sa.BOOLEAN(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table('exam_results',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('exam_id', sa.UUID(), sa.ForeignKey('exams.id'), nullable=False),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id')),
        sa.Column('session_id', sa.VARCHAR(100), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('raw_score', sa.Float(), nullable=False),
        sa.Column('total_points', sa.INTEGER(), nullable=False),
        sa.Column('correct_answers', sa.INTEGER(), nullable=False),
        sa.Column('wrong_answers', sa.INTEGER(), nullable=False),
        sa.Column('empty_answers', sa.INTEGER(), nullable=False),
        sa.Column('total_answers', sa.INTEGER(), nullable=False),
        sa.Column('subject_scores', postgresql.JSON(), nullable=False),
        sa.Column('answers', postgresql.JSON(), nullable=False),
        sa.Column('time_taken_seconds', sa.INTEGER()),
        sa.Column('started_at', sa.TIMESTAMP()),
        sa.Column('completed_at', sa.TIMESTAMP()),
        sa.Column('exam_year', sa.INTEGER()),
        sa.Column('compared_to_avg', sa.Float()),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    # Question Bank
    op.create_table('question_bank',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('subject', sa.VARCHAR(50), nullable=False, index=True),
        sa.Column('difficulty', sa.VARCHAR(20), nullable=False, server_default='medium'),
        sa.Column('question_fa', sa.TEXT(), nullable=False),
        sa.Column('question_en', sa.TEXT()),
        sa.Column('options', postgresql.JSON(), nullable=False),
        sa.Column('explanation_fa', sa.TEXT()),
        sa.Column('source', sa.VARCHAR(100)),
        sa.Column('year', sa.INTEGER(), index=True),
        sa.Column('grade', sa.VARCHAR(10), index=True),
        sa.Column('chapter', sa.VARCHAR(150)),
        sa.Column('is_verified', sa.BOOLEAN(), nullable=False, server_default='false'),
        sa.Column('is_active', sa.BOOLEAN(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table('exam_blueprints',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('name_fa', sa.VARCHAR(300), nullable=False),
        sa.Column('description_fa', sa.TEXT()),
        sa.Column('total_minutes', sa.INTEGER(), nullable=False, server_default='160'),
        sa.Column('sections', postgresql.JSON(), nullable=False),
        sa.Column('is_active', sa.BOOLEAN(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    # Mock Kankor
    op.create_table('mock_exam_sessions',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('session_id', sa.VARCHAR(100), nullable=False, index=True),
        sa.Column('blueprint_id', sa.UUID(), sa.ForeignKey('exam_blueprints.id', ondelete='SET NULL')),
        sa.Column('questions', postgresql.JSON(), nullable=False),
        sa.Column('answers', postgresql.JSON(), server_default='{}'),
        sa.Column('started_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('completed_at', sa.TIMESTAMP()),
        sa.Column('score', sa.Float()),
        sa.Column('subject_scores', postgresql.JSON(), server_default='{}'),
        sa.Column('time_taken_seconds', sa.INTEGER()),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    # Auth
    op.create_table('admin_users',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('email', sa.VARCHAR(200), nullable=False, unique=True, index=True),
        sa.Column('hashed_password', sa.VARCHAR(200), nullable=False),
        sa.Column('full_name', sa.VARCHAR(200), nullable=False),
        sa.Column('role', sa.VARCHAR(50), nullable=False),
        sa.Column('is_active', sa.BOOLEAN(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table('refresh_tokens',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('admin_id', sa.UUID(), sa.ForeignKey('admin_users.id'), nullable=False),
        sa.Column('token_hash', sa.VARCHAR(200), nullable=False, unique=True, index=True),
        sa.Column('expires_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('revoked', sa.BOOLEAN(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table('users',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('email', sa.VARCHAR(200), nullable=False, unique=True, index=True),
        sa.Column('phone', sa.VARCHAR(20), unique=True, index=True),
        sa.Column('full_name', sa.VARCHAR(200), nullable=False),
        sa.Column('hashed_password', sa.VARCHAR(200), nullable=False),
        sa.Column('is_active', sa.BOOLEAN(), nullable=False, server_default='true'),
        sa.Column('is_verified', sa.BOOLEAN(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    # Notifications
    op.create_table('academic_events',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('title_fa', sa.VARCHAR(300), nullable=False),
        sa.Column('description_fa', sa.TEXT()),
        sa.Column('event_date', sa.DATE(), nullable=False),
        sa.Column('event_type', sa.VARCHAR(50), nullable=False),
        sa.Column('remind_days_before', sa.INTEGER(), nullable=False, server_default='7'),
        sa.Column('is_active', sa.BOOLEAN(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    # AI / RAG
    op.create_table('rag_chunks',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('source_type', sa.VARCHAR(50), nullable=False),
        sa.Column('source_id', sa.UUID(), sa.ForeignKey('departments.id')),
        sa.Column('content', sa.TEXT(), nullable=False),
        sa.Column('language', sa.VARCHAR(5), nullable=False, server_default='fa'),
        sa.Column('embedding', sa.NullType()),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table('ai_chat_logs',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('session_id', sa.VARCHAR(100), nullable=False),
        sa.Column('user_message', sa.TEXT(), nullable=False),
        sa.Column('ai_response', sa.TEXT(), nullable=False),
        sa.Column('was_cached', sa.BOOLEAN(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
    )

    # pgvector extension and index
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("CREATE INDEX ix_rag_embedding ON rag_chunks USING hnsw (embedding vector_cosine_ops)")


def downgrade() -> None:
    """Drop all tables."""
    op.execute("DROP INDEX IF EXISTS ix_rag_embedding")
    op.drop_table('ai_chat_logs')
    op.drop_table('rag_chunks')
    op.drop_table('academic_events')
    op.drop_table('users')
    op.drop_table('refresh_tokens')
    op.drop_table('admin_users')
    op.drop_table('mock_exam_sessions')
    op.drop_table('exam_blueprints')
    op.drop_table('question_bank')
    op.drop_table('exam_results')
    op.drop_table('exam_options')
    op.drop_table('exam_questions')
    op.drop_table('exams')
    op.drop_table('department_trait_profiles')
    op.drop_table('quiz_options')
    op.drop_table('quiz_questions')
    op.drop_table('kankor_guides')
    op.drop_table('kankor_cutoffs')
    op.drop_table('faqs')
    op.drop_table('news')
    op.drop_table('career_roadmaps')
    op.drop_table('alumni_stories')
    op.drop_table('student_projects')
    op.drop_table('departments')
    op.drop_table('faculties')
    op.drop_table('universities')
