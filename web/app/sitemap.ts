import type { MetadataRoute } from "next";

const BASE_URL = "https://guide.hu.edu.af";

async function fetchSlugs(path: string): Promise<string[]> {
  try {
    const res = await fetch(`process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:9000/api/v1"/${path}`, {
      next: { revalidate: 3600 },
    });
    if (!res.ok) return [];
    const data = await res.json();
    return data.map((item: { slug: string }) => item.slug);
  } catch {
    return [];
  }
}

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const now = new Date().toISOString();

  // Static pages
  const staticPages: MetadataRoute.Sitemap = [
    { url: BASE_URL, lastModified: now, changeFrequency: "daily", priority: 1 },
    { url: `${BASE_URL}/faculties`, lastModified: now, changeFrequency: "weekly", priority: 0.9 },
    { url: `${BASE_URL}/kankor`, lastModified: now, changeFrequency: "monthly", priority: 0.8 },
    { url: `${BASE_URL}/kankor/chance`, lastModified: now, changeFrequency: "monthly", priority: 0.9 },
    { url: `${BASE_URL}/quiz`, lastModified: now, changeFrequency: "monthly", priority: 0.8 },
    { url: `${BASE_URL}/chat`, lastModified: now, changeFrequency: "monthly", priority: 0.7 },
  ];

  // Dynamic pages
  const facultySlugs = await fetchSlugs("faculties");
  const faculties = facultySlugs.map((slug) => ({
    url: `${BASE_URL}/faculties/${slug}`,
    lastModified: now,
    changeFrequency: "weekly" as const,
    priority: 0.8,
  }));

  return [...staticPages, ...faculties];
}
