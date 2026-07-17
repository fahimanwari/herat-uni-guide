"""
Seed admin user and academic events.
Run: python seed_admin.py
"""

import asyncio
from datetime import date, timedelta

from app.database import SessionLocal
from app.modules.admin_auth.service import AdminAuthService
from app.modules.notifications.repository import EventRepository


async def seed():
    async with SessionLocal() as db:
        # Create admin user
        auth_service = AdminAuthService(db)
        try:
            admin = await auth_service.create_admin(
                email="admin@herat-uni.edu.af",
                password="admin123",
                full_name="مدیر سیستم",
                role="admin",
            )
            print(f"Admin created: {admin.email}")
        except Exception as e:
            print(f"Admin may already exist: {e}")

        # Create sample academic events
        event_repo = EventRepository(db)
        events = [
            {
                "title_fa": "آغاز ثبت‌نام کانکور ۱۴۰۵",
                "description_fa": "ثبت‌نام امتحان کانکور از این تاریخ آغاز می‌شود.",
                "event_date": date(1405, 3, 1),  # Approximate
                "event_type": "kankor_registration",
                "remind_days_before": 7,
            },
            {
                "title_fa": "روز امتحان کانکور",
                "description_fa": "امتحان ورودی پوهنتون‌های دولتی.",
                "event_date": date(1405, 5, 15),  # Approximate
                "event_type": "kankor_exam",
                "remind_days_before": 3,
            },
            {
                "title_fa": "اعلام نتایج کانکور",
                "description_fa": "نتایج امتحان کانکور اعلام می‌شود.",
                "event_date": date(1405, 6, 15),  # Approximate
                "event_type": "kankor_results",
                "remind_days_before": 1,
            },
        ]

        for ev_data in events:
            try:
                await event_repo.create(ev_data)
                print(f"Event created: {ev_data['title_fa']}")
            except Exception as e:
                print(f"Event error: {e}")

        print("\nDone!")
        print("Admin login: admin@herat-uni.edu.af / admin123")


if __name__ == "__main__":
    asyncio.run(seed())
