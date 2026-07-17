const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:9000/api/v1";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { next: { revalidate: 300 } });
  if (!res.ok) throw new Error(`API ${res.status}: ${path}`);
  return res.json();
}

export const api = {
  universities: {
    list: () => get<import("./types").UniversityListItem[]>("/universities"),
    get: (slug: string) => get<import("./types").UniversityDetail>(`/universities/${slug}`),
  },
  faculties: {
    list: (universityId?: string) =>
      get<import("./types").FacultyListItem[]>(
        `/faculties${universityId ? `?university_id=${universityId}` : ""}`
      ),
    get: (slug: string) => get<import("./types").FacultyDetail>(`/faculties/${slug}`),
  },
  departments: {
    list: (facultyId?: string) =>
      get<import("./types").DepartmentListItem[]>(
        `/departments${facultyId ? `?faculty_id=${facultyId}` : ""}`
      ),
    get: (slug: string) => get<import("./types").DepartmentDetail>(`/departments/${slug}`),
  },
  news: {
    list: (universityId?: string) =>
      get<import("./types").NewsListItem[]>(
        `/news${universityId ? `?university_id=${universityId}` : ""}`
      ),
  },
  faqs: {
    list: (universityId?: string) =>
      get<import("./types").FaqListItem[]>(
        `/faqs${universityId ? `?university_id=${universityId}` : ""}`
      ),
  },
};
