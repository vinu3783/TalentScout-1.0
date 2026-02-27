"""
utils/storage.py
─────────────────
Simulated local data persistence for candidate screening records.

In production, replace the JSON file write with a call to a secure,
encrypted database (e.g., PostgreSQL with RLS, or a GDPR-compliant SaaS).

Privacy notes:
  - No full interview answers are stored.
  - The JSON log is excluded from version control via .gitignore.
  - Phone and email are stored as-is for demo purposes; in production
    these should be encrypted at rest.
"""

import json
import os
from datetime import datetime, timezone


LOG_FILE = "candidates_log.json"


def save_candidate(candidate: dict, answers: list[dict]) -> bool:
    """
    Append a candidate screening record to the local JSON log.

    Args:
        candidate: Dict with keys: name, email, phone, experience,
                   position, location, tech_stack.
        answers:   List of {"question": str, "answered": bool} dicts.

    Returns:
        True if saved successfully, False otherwise.
    """
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "name":          candidate.get("name", ""),
        "email":         candidate.get("email", ""),
        "phone":         candidate.get("phone", ""),
        "experience":    candidate.get("experience", ""),
        "position":      candidate.get("position", ""),
        "location":      candidate.get("location", ""),
        "tech_stack":    candidate.get("tech_stack", ""),
        "questions_asked": len(answers),
        "screening_complete": True,
    }

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return True
    except IOError:
        return False


def load_all_candidates() -> list[dict]:
    """
    Read all previously saved candidate records.

    Returns:
        List of record dicts, most recent first.
    """
    if not os.path.exists(LOG_FILE):
        return []
    records = []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except IOError:
        return []
    return list(reversed(records))   # newest first