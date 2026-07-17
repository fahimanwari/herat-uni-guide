import Link from "next/link";
import { notFound } from "next/navigation";
import { Header } from "../../components/layout/Header";
import { Footer } from "../../components/layout/Footer";
import { Card, SectionTitle, Badge } from "../../components/ui";
import { api } from "../../lib/api";

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  try {
    const fac = await api.faculties.get(slug);
    return { title: `${fac.name_fa} | پوهنتون هرات` };
  } catch {
    return { title: "پوهنځی | پوهنتون هرات" };
  }
}

export default async function FacultyPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  let faculty: import("../../lib/types").FacultyDetail | null = null;
  try {
    faculty = await api.faculties.get(slug);
  } catch {
    notFound();
  }

  let departments: import("../../lib/types").DepartmentListItem[] = [];
  try {
    departments = await api.departments.list(faculty!.id);
  } catch {
    departments = [];
  }

  const degreeDepts = departments.filter((d) => d.department_type === "degree");
  const serviceDepts = departments.filter((d) => d.department_type === "service");

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
            <span className="text-foreground">{faculty.name_fa}</span>
          </nav>

          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-2">
              {faculty.name_fa}
            </h1>
            {faculty.name_en && (
              <p className="text-muted text-lg">{faculty.name_en}</p>
            )}
          </div>

          {/* Vision & Mission */}
          {(faculty.vision_fa || faculty.mission_fa) && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              {faculty.vision_fa && (
                <Card>
                  <h3 className="font-bold text-lg mb-2 text-primary-600">دیدگاه</h3>
                  <p className="text-foreground">{faculty.vision_fa}</p>
                </Card>
              )}
              {faculty.mission_fa && (
                <Card>
                  <h3 className="font-bold text-lg mb-2 text-primary-600">ماموریت</h3>
                  <p className="text-foreground">{faculty.mission_fa}</p>
                </Card>
              )}
            </div>
          )}

          {/* Description */}
          <Card className="mb-8">
            <p className="text-foreground leading-relaxed">{faculty.description_fa}</p>
          </Card>

          {/* Degree Departments */}
          {degreeDepts.length > 0 && (
            <section className="mb-12">
              <SectionTitle
                title="رشته‌های فارغ‌ده"
                subtitle="این رشته‌ها در کانکور قابل انتخاب هستند"
              />
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {degreeDepts.map((dept) => (
                  <Link key={dept.id} href={`/faculties/${slug}/${dept.slug}`}>
                    <Card clickable className="h-full">
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="font-bold text-lg text-foreground">
                          {dept.name_fa}
                        </h3>
                        <Badge variant="success">قابل انتخاب</Badge>
                      </div>
                      {dept.name_en && (
                        <p className="text-muted text-sm">{dept.name_en}</p>
                      )}
                    </Card>
                  </Link>
                ))}
              </div>
            </section>
          )}

          {/* Service Departments */}
          {serviceDepts.length > 0 && (
            <section className="mb-12">
              <SectionTitle
                title="دیپارتمنت‌های خدماتی"
                subtitle="خدمات آموزشی — در کانکور انتخاب نمی‌شوند"
              />
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {serviceDepts.map((dept) => (
                  <Card key={dept.id}>
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 className="font-bold text-foreground">{dept.name_fa}</h3>
                        {dept.name_en && (
                          <p className="text-muted text-sm mt-1">{dept.name_en}</p>
                        )}
                      </div>
                      <Badge variant="neutral">خدماتی</Badge>
                    </div>
                  </Card>
                ))}
              </div>
            </section>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
