#!/usr/bin/env python3
"""
خودکار تقویم کانکور — از اطلاعیه‌های NEXA/وزارت تاریخ‌ها را استخراج می‌کند
"""

import asyncio
import json
import sys
import os
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import httpx

SOURCES = [
    "https://nexa.gov.af/fa",
    "https://mohe.gov.af",
]

KEYWORDS = ["کانکور", "ثبت‌نام", "بایومتریک", "امتحان", "نتایج"]


async def fetch_kankor_dates():
    from app.database import SessionLocal, engine, Base
    from app.modules.notifications.models import AcademicEvent
    from app.modules.universities.models import University
    from sqlalchemy import select

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        uni = (await db.execute(
            select(University).where(University.slug == "herat-university")
        )).scalar_one_or_none()

        if not uni:
            print("ERROR: Herat University not found")
            return

        new_count = 0
        skip_count = 0

        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            for source_url in SOURCES:
                try:
                    print(f"Fetching: {source_url}")
                    resp = await client.get(source_url)
                    if resp.status_code != 200:
                        continue

                    soup = BeautifulSoup(resp.text, "html.parser")
                    text = soup.get_text()

                    # Find date patterns (Dari/Pashto dates)
                    date_patterns = [
                        r"(\d{1,2})\s*(جدی|حوت|وریا|ثور|جوزا|سرطان|اسد|سنبله|میزان|عقرب|قوس|جدی)",
                        r"(\d{4})/(\d{1,2})/(\d{1,2})",
                    ]

                    for pattern in date_patterns:
                        matches = re.findall(pattern, text)
                        for match in matches:
                            # Simple extraction - in production, use AI for better parsing
                            pass

                    # For now, just log what we find
                    links = soup.find_all("a", href=True)
                    for link in links:
                        link_text = link.get_text(strip=True)
                        if any(kw in link_text for kw in KEYWORDS):
                            print(f"  Potential event: {link_text[:80]}...")

                except Exception as e:
                    print(f"  Error: {e}")

        print("\nNote: This script identifies potential event pages.")
        print("For accurate date extraction, use AI provider or manual entry.")
        print(f"New events: {new_count}, Skipped: {skip_count}")


if __name__ == "__main__":
    from bs4 import BeautifulSoup
    asyncio.run(fetch_kankor_dates())
