import uuid

from pydantic import BaseModel, ConfigDict


# --- Department ---

class DepartmentListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str
    name_fa: str
    name_en: str | None
    degree_type: str
    department_type: str


class DepartmentDetail(DepartmentListItem):
    faculty_id: uuid.UUID
    name_ps: str | None
    description_fa: str
    description_ps: str | None
    description_en: str | None
    vision_fa: str | None
    mission_fa: str | None
    duration_years: int
    subjects: list
    career_paths: list
    required_skills: list
    suitable_for: list
    job_market_fa: str | None
    difficulty_level: str | None
    student_projects: list[StudentProjectSchema] = []
    alumni_stories: list[AlumniStorySchema] = []
    career_roadmaps: list[CareerRoadmapSchema] = []


class DepartmentCreate(BaseModel):
    faculty_id: uuid.UUID
    slug: str
    name_fa: str
    description_fa: str
    name_ps: str | None = None
    name_en: str | None = None
    description_ps: str | None = None
    description_en: str | None = None
    department_type: str = "degree"
    vision_fa: str | None = None
    mission_fa: str | None = None
    duration_years: int = 4
    degree_type: str = "لیسانس"
    subjects: list = []
    career_paths: list = []
    required_skills: list = []
    suitable_for: list = []
    job_market_fa: str | None = None
    difficulty_level: str | None = None


class DepartmentUpdate(BaseModel):
    name_fa: str | None = None
    description_fa: str | None = None
    name_ps: str | None = None
    name_en: str | None = None
    description_ps: str | None = None
    description_en: str | None = None
    department_type: str | None = None
    vision_fa: str | None = None
    mission_fa: str | None = None
    duration_years: int | None = None
    degree_type: str | None = None
    subjects: list | None = None
    career_paths: list | None = None
    required_skills: list | None = None
    suitable_for: list | None = None
    job_market_fa: str | None = None
    difficulty_level: str | None = None


# --- Student Project ---

class StudentProjectSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title_fa: str
    description_fa: str
    image_url: str | None
    students: str | None
    year: int | None


class StudentProjectCreate(BaseModel):
    title_fa: str
    description_fa: str
    image_url: str | None = None
    students: str | None = None
    year: int | None = None


# --- Alumni Story ---

class AlumniStorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str
    graduation_year: int
    current_position: str
    story_fa: str
    photo_url: str | None
    youtube_video_id: str | None


class AlumniStoryCreate(BaseModel):
    full_name: str
    graduation_year: int
    current_position: str
    story_fa: str
    photo_url: str | None = None
    youtube_video_id: str | None = None


# --- Career Roadmap ---

class CareerRoadmapSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    career_title_fa: str
    steps: list


class CareerRoadmapCreate(BaseModel):
    career_title_fa: str
    steps: list = []
