import Link from "next/link";
import { notFound } from "next/navigation";
import { Header } from "../../../components/layout/Header";
import { Footer } from "../../../components/layout/Footer";
import { Card, SectionTitle, Badge } from "../../../components/ui";
import { api } from "../../../lib/api";

export async function generateMetadata({ params }: { params: Promise<{ slug: string; dept: string }> }) {
  const { dept } = await params;
  try {
    const d = await api.departments.get(dept);
    return { title: `${d.name_fa} | پوهنتون هرات` };
  } catch {
    return { title: "رشته | پوهنتون هرات" };
  }
}

export default async function DepartmentPage({
  params,
}: {
  params: Promise<{ slug: string; dept: string }>;
}) {
  const { slug, dept } = await params;
  let department: import("../../../lib/types").DepartmentDetail | null = null;
  try {
    department = await api.departments.get(dept);
  } catch {
    notFound();
  }

  let faculty: import("../../../lib/types").FacultyDetail | null = null;
  try {
    faculty = await api.faculties.get(slug);
  } catch {
    faculty = null;
  }

  return (
    <>
      <Header />
      <main className="flex-1 py-12">
        <div className="max-w-7xl mx-auto px-4">
          {/* Breadcrumb */}
          <nav className="text-sm text-muted mb-6">
            <Link href="/" className="hover:text-primary-600">خانه</Link>
            <span className="mx-2">←</span>
            <Link href="/faculties" className="hover:text-primary-600">پوهنځی‌ها</Link>
            <span className="mx-2">←</span>
            {faculty && (
              <>
                <Link href={`/faculties/${slug}`} className="hover:text-primary-600">
                  {faculty.name_fa}
                </Link>
                <span className="mx-2">←</span>
              </>
            )}
            <span className="text-foreground">{department.name_fa}</span>
          </nav>

          {/* Header */}
          <div className="mb-8">
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-3xl md:text-4xl font-bold text-foreground">
                {department.name_fa}
              </h1>
              {department.department_type === "degree" ? (
                <Badge variant="success">فارغ‌ده</Badge>
              ) : (
                <Badge variant="neutral">خدماتی</Badge>
              )}
            </div>
            {department.name_en && (
              <p className="text-muted text-lg">{department.name_en}</p>
            )}
          </div>

          {/* Vision & Mission */}
          {(department.vision_fa || department.mission_fa) && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              {department.vision_fa && (
                <Card>
                  <h3 className="font-bold text-lg mb-2 text-primary-600">دیدگاه</h3>
                  <p className="text-foreground">{department.vision_fa}</p>
                </Card>
              )}
              {department.mission_fa && (
                <Card>
                  <h3 className="font-bold text-lg mb-2 text-primary-600">ماموریت</h3>
                  <p className="text-foreground">{department.mission_fa}</p>
                </Card>
              )}
            </div>
          )}

          {/* Description */}
          <Card className="mb-8">
            <p className="text-foreground leading-relaxed">{department.description_fa}</p>
          </Card>

          {/* Info Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <Card>
              <div className="text-sm text-muted mb-1">مدت تحصیل</div>
              <div className="font-bold text-lg">{department.duration_years} سال</div>
            </Card>
            <Card>
              <div className="text-sm text-muted mb-1">مدرک</div>
              <div className="font-bold text-lg">{department.degree_type}</div>
            </Card>
            {department.difficulty_level && (
              <Card>
                <div className="text-sm text-muted mb-1">سطح دشواری</div>
                <div className="font-bold text-lg">{department.difficulty_level}</div>
              </Card>
            )}
          </div>

          {/* Subjects */}
          {department.subjects.length > 0 && (
            <section className="mb-8">
              <SectionTitle title="مضامین اصلی" />
              <div className="flex flex-wrap gap-2">
                {department.subjects.map((s, i) => (
                  <Badge key={i} variant="neutral">{s}</Badge>
                ))}
              </div>
            </section>
          )}

          {/* Career Paths */}
          {department.career_paths.length > 0 && (
            <section className="mb-8">
              <SectionTitle title="آینده شغلی" />
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {department.career_paths.map((cp, i) => (
                  <Card key={i}>
                    <h4 className="font-bold text-foreground">{cp.title}</h4>
                    <p className="text-muted text-sm mt-1">{cp.desc}</p>
                  </Card>
                ))}
              </div>
            </section>
          )}

          {/* Skills */}
          {department.required_skills.length > 0 && (
            <section className="mb-8">
              <SectionTitle title="مهارت‌های لازم" />
              <ul className="space-y-2">
                {department.required_skills.map((s, i) => (
                  <li key={i} className="flex items-center gap-2 text-foreground">
                    <span className="w-2 h-2 rounded-full bg-accent-500" />
                    {s}
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Suitable For */}
          {department.suitable_for.length > 0 && (
            <section className="mb-8">
              <SectionTitle title="مناسب چه کسی است؟" />
              <ul className="space-y-2">
                {department.suitable_for.map((s, i) => (
                  <li key={i} className="flex items-center gap-2 text-foreground">
                    <span className="w-2 h-2 rounded-full bg-gold-500" />
                    {s}
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Job Market */}
          {department.job_market_fa && (
            <section className="mb-8">
              <SectionTitle title="بازار کار" />
              <Card>
                <p className="text-foreground leading-relaxed">{department.job_market_fa}</p>
              </Card>
            </section>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
