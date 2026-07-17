"""
SQLAdmin — quick admin panel for content management.
Access: http://localhost:8000/admin
"""

from sqladmin import Admin, ModelView
from app.database import engine, Base
from app.main import app

from app.modules.universities.models import University
from app.modules.faculties.models import Faculty
from app.modules.departments.models import Department, StudentProject, AlumniStory, CareerRoadmap
from app.modules.news.models import News
from app.modules.faqs.models import Faq
from app.modules.kankor.models import KankorCutoff, KankorGuide
from app.modules.quiz.models import QuizQuestion, QuizOption, DepartmentTraitProfile
from app.modules.ai.models import RagChunk, AiChatLog
from app.modules.admin_auth.models import AdminUser, RefreshToken
from app.modules.notifications.models import AcademicEvent


admin = Admin(app, engine)


class UniversityAdmin(ModelView, model=University):
    column_list = [University.name_fa, University.slug, University.is_active]


class FacultyAdmin(ModelView, model=Faculty):
    column_list = [Faculty.name_fa, Faculty.slug, Faculty.university_id]


class DepartmentAdmin(ModelView, model=Department):
    column_list = [Department.name_fa, Department.slug, Department.department_type, Department.faculty_id]


class StudentProjectAdmin(ModelView, model=StudentProject):
    column_list = [StudentProject.title_fa, StudentProject.department_id]


class AlumniStoryAdmin(ModelView, model=AlumniStory):
    column_list = [AlumniStory.full_name, AlumniStory.department_id]


class CareerRoadmapAdmin(ModelView, model=CareerRoadmap):
    column_list = [CareerRoadmap.career_title_fa, CareerRoadmap.department_id]


class NewsAdmin(ModelView, model=News):
    column_list = [News.title_fa, News.is_published, News.published_at]


class FaqAdmin(ModelView, model=Faq):
    column_list = [Faq.question_fa, Faq.category]


class KankorCutoffAdmin(ModelView, model=KankorCutoff):
    column_list = [KankorCutoff.department_id, KankorCutoff.year, KankorCutoff.min_score]


class KankorGuideAdmin(ModelView, model=KankorGuide):
    column_list = [KankorGuide.title_fa, KankorGuide.category]


class QuizQuestionAdmin(ModelView, model=QuizQuestion):
    column_list = [QuizQuestion.question_fa, QuizQuestion.category]


class QuizOptionAdmin(ModelView, model=QuizOption):
    column_list = [QuizOption.text_fa, QuizOption.question_id]


class DepartmentTraitProfileAdmin(ModelView, model=DepartmentTraitProfile):
    column_list = [DepartmentTraitProfile.department_id]


class RagChunkAdmin(ModelView, model=RagChunk):
    column_list = [RagChunk.source_type, RagChunk.language]


class AiChatLogAdmin(ModelView, model=AiChatLog):
    column_list = [AiChatLog.session_id, AiChatLog.was_cached, AiChatLog.created_at]


class AcademicEventAdmin(ModelView, model=AcademicEvent):
    column_list = [AcademicEvent.title_fa, AcademicEvent.event_date, AcademicEvent.event_type]


# Register all models
admin.add_model_view(UniversityAdmin)
admin.add_model_view(FacultyAdmin)
admin.add_model_view(DepartmentAdmin)
admin.add_model_view(StudentProjectAdmin)
admin.add_model_view(AlumniStoryAdmin)
admin.add_model_view(CareerRoadmapAdmin)
admin.add_model_view(NewsAdmin)
admin.add_model_view(FaqAdmin)
admin.add_model_view(KankorCutoffAdmin)
admin.add_model_view(KankorGuideAdmin)
admin.add_model_view(QuizQuestionAdmin)
admin.add_model_view(QuizOptionAdmin)
admin.add_model_view(DepartmentTraitProfileAdmin)
admin.add_model_view(RagChunkAdmin)
admin.add_model_view(AiChatLogAdmin)
admin.add_model_view(AcademicEventAdmin)
