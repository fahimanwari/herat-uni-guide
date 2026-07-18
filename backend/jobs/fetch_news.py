#!/usr/bin/env python3
"""
هفتگی با cron اجرا می‌شود:
crontab -e →
0 6 * * 6  cd /path/backend && .venv/bin/python jobs/fetch_news.py
"""

import asyncio
import sys
import os
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import httpx
from bs4 import BeautifulSoup

SOURCES = [
    "https://hu.edu.af",
    "https://mohe.gov.af",
    "https://nexa.gov.af/fa",
]
KEYWORDS = ["هرات", "کانکور", "پوهنتون"]


async def fetch_news():
    from app.database import SessionLocal, engine, Base
    from app.modules.news.models import News
    from app.modules.universities.models import University

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        # Get Herat University ID
        from sqlalchemy import select
        uni = (await db.execute(
            select(University).where(University.slug == "herat-university")
        )).scalar_one_or_none()

        if not uni:
            print("ERROR: Herat University not found in database")
            return

        new_count = 0
        skip_count = 0

        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            for source_url in SOURCES:
                try:
                    print(f"Fetching: {source_url}")
                    resp = await client.get(source_url)
                    if resp.status_code != 200:
                        print(f"  HTTP {resp.status_code}, skipping")
                        continue

                    soup = BeautifulSoup(resp.text, "html.parser")
                    links = soup.find_all("a", href=True)

                    for link in links:
                        text = link.get_text(strip=True)
                        if not text or len(text) < 10:
                            continue

                        # Check keywords
                        if not any(kw in text for kw in KEYWORDS):
                            continue

                        href = link["href"]
                        if href.startswith("/"):
                            from urllib.parse import urljoin
                            href = urljoin(source_url, href)

                        # Check for duplicates
                        existing = (await db.execute(
                            select(News).where(News.source_url == href)
                        )).scalar_one_or_none()

                        if existing:
                            skip_count += 1
                            continue

                        # Try to get article content
                        try:
                            article_resp = await client.get(href)
                            if article_resp.status_code == 200:
                                article_soup = BeautifulSoup(article_resp.text, "html.parser")
                                # Remove scripts and styles
                                for tag in article_soup(["script", "style", "nav", "header", "footer"]):
                                    tag.decompose()
                                body_text = article_soup.get_text(separator="\n", strip=True)[:2000]
                            else:
                                body_text = text
                        except:
                            body_text = text

                        # Create AI draft
                        news = News(
                            university_id=uni.id,
                            title_fa=text[:300],
                            body_fa=body_text,
                            source_url=href,
                            is_published=False,
                            is_ai_draft=True,
                        )
                        db.add(news)
                        new_count += 1
                        print(f"  Found: {text[:60]}...")

                except Exception as e:
                    print(f"  Error fetching {source_url}: {e}")

        await db.commit()
        print(f"\nDone! New: {new_count}, Skipped (duplicates): {skip_count}")


if __name__ == "__main__":
    asyncio.run(fetch_news())
