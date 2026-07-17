"use client";

import Script from "next/script";

const UMAMI_WEBSITE_ID = process.env.NEXT_PUBLIC_UMAMI_WEBSITE_ID;

export function Analytics() {
  if (!UMAMI_WEBSITE_ID) return null;

  return (
    <Script
      defer
      src="https://analytics.example.com/script.js"
      data-website-id={UMAMI_WEBSITE_ID}
    />
  );
}
