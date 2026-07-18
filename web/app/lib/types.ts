export interface UniversityListItem {
  id: string;
  slug: string;
  name_fa: string;
  name_en: string | null;
  established_year: number | null;
  logo_url: string | null;
}

export interface UniversityDetail extends UniversityListItem {
  name_ps: string | null;
  description_fa: string;
  description_ps: string | null;
  description_en: string | null;
  history_fa: string | null;
  chancellor_name: string | null;
  stats: Record<string, number> | null;
  lat: number | null;
  lng: number | null;
}

export interface FacultyListItem {
  id: string;
  slug: string;
  name_fa: string;
  name_en: string | null;
  cover_image_url: string | null;
  sort_order: number;
}

export interface FacultyDetail extends FacultyListItem {
  university_id: string;
  name_ps: string | null;
  description_fa: string;
  description_ps: string | null;
  description_en: string | null;
  vision_fa: string | null;
  mission_fa: string | null;
  youtube_video_id: string | null;
  dean_name: string | null;
  established_year: number | null;
}

export interface DepartmentListItem {
  id: string;
  slug: string;
  name_fa: string;
  name_en: string | null;
  degree_type: string;
  department_type: "degree" | "service";
}

export interface DepartmentDetail extends DepartmentListItem {
  faculty_id: string;
  name_ps: string | null;
  description_fa: string;
  description_ps: string | null;
  description_en: string | null;
  vision_fa: string | null;
  mission_fa: string | null;
  duration_years: number;
  subjects: string[];
  career_paths: CareerPath[];
  required_skills: string[];
  suitable_for: string[];
  job_market_fa: string | null;
  difficulty_level: string | null;
  student_projects: StudentProject[];
  alumni_stories: AlumniStory[];
  career_roadmaps: CareerRoadmap[];
}

export interface CareerPath {
  title: string;
  desc: string;
}

export interface StudentProject {
  id: string;
  title_fa: string;
  description_fa: string;
  image_url: string | null;
  students: string | null;
  year: number | null;
}

export interface AlumniStory {
  id: string;
  full_name: string;
  graduation_year: number;
  current_position: string;
  story_fa: string;
  photo_url: string | null;
  youtube_video_id: string | null;
}

export interface CareerRoadmap {
  id: string;
  career_title_fa: string;
  steps: RoadmapStep[];
}

export interface RoadmapStep {
  title: string;
  desc: string;
  resources: { name: string; url: string }[];
}

export interface NewsListItem {
  id: string;
  title_fa: string;
  title_en: string | null;
  cover_image_url: string | null;
  published_at: string | null;
}

export interface FaqListItem {
  id: string;
  question_fa: string;
  category: string | null;
  sort_order: number;
}

export interface FaqDetail extends FaqListItem {
  answer_fa: string;
  question_ps: string | null;
  answer_ps: string | null;
  question_en: string | null;
  answer_en: string | null;
}

export interface ExamListItem {
  id: string;
  title_fa: string;
  title_en: string | null;
  category: string;
  year: number | null;
  duration_minutes: number;
  total_questions: number;
  passing_score: number;
}

export interface ExamDetail extends ExamListItem {
  description_fa: string | null;
  max_score: number;
}
