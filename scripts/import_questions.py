#!/usr/bin/env python3
"""
Import questions from JSON files to the question bank.

Usage:
  python scripts/import_questions.py scripts/sample_questions.json
  python scripts/import_questions.py scripts/question_format.json

Format: see scripts/question_format.json
"""

import asyncio
import json
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.database import SessionLocal, engine, Base
from app.modules.question_bank.models import QuestionBank


async def import_questions(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Support single question or array
    if isinstance(data, dict):
        data = [data]

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    imported = 0
    errors = 0

    async with SessionLocal() as db:
        for i, item in enumerate(data):
            try:
                # Validate required fields
                if "question_fa" not in item or "options" not in item:
                    print(f"  [{i+1}] SKIP: missing question_fa or options")
                    errors += 1
                    continue

                # Validate options
                options = item["options"]
                if len(options) < 2:
                    print(f"  [{i+1}] SKIP: needs at least 2 options")
                    errors += 1
                    continue

                has_correct = any(opt.get("is_correct") for opt in options)
                if not has_correct:
                    print(f"  [{i+1}] SKIP: no correct answer marked")
                    errors += 1
                    continue

                grade = item.get("grade")
                if grade is not None and str(grade) not in ("10", "11", "12"):
                    print(f"  [{i+1}] SKIP: grade must be 10, 11 or 12 (got {grade!r})")
                    errors += 1
                    continue

                q = QuestionBank(
                    subject=item.get("subject", "general"),
                    difficulty=item.get("difficulty", "medium"),
                    question_fa=item["question_fa"],
                    question_en=item.get("question_en"),
                    options=options,
                    explanation_fa=item.get("explanation_fa"),
                    source=item.get("source"),
                    year=item.get("year"),
                    grade=str(grade) if grade is not None else None,
                    chapter=item.get("chapter"),
                    is_verified=item.get("is_verified", False),
                    is_active=True,
                )
                db.add(q)
                imported += 1

                if imported % 50 == 0:
                    await db.commit()
                    print(f"  ... imported {imported} so far")

            except Exception as e:
                print(f"  [{i+1}] ERROR: {e}")
                errors += 1

        await db.commit()

    print(f"\nDone! Imported: {imported}, Errors: {errors}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/import_questions.py <questions.json>")
        sys.exit(1)
    asyncio.run(import_questions(sys.argv[1]))
