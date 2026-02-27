"""
utils/validators.py
────────────────────
Input validation helpers for each collected field.
All functions return (is_valid: bool, error_message: str).
"""

import re


def validate_name(text: str) -> tuple[bool, str]:
    """
    Name must be at least 2 characters and contain only letters/spaces/hyphens.
    """
    name = text.strip()
    if len(name) < 2:
        return False, "Name seems too short. Please enter your full name."
    if not re.match(r"^[A-Za-z\s\-'\.]+$", name):
        return False, "Name should contain only letters, spaces, hyphens, or apostrophes."
    return True, ""


def validate_email(text: str) -> tuple[bool, str]:
    """Standard RFC-5322-inspired email check."""
    pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, text.strip()):
        return False, "That doesn't look like a valid email. Example: you@domain.com"
    return True, ""


def validate_phone(text: str) -> tuple[bool, str]:
    """
    Accepts 7-15 digits optionally prefixed by + and separated by spaces/dashes/parens.
    """
    cleaned = re.sub(r"[\s\-\(\)\+]", "", text)
    if not cleaned.isdigit():
        return False, "Phone should contain only digits (and optional +, spaces, dashes)."
    if not (7 <= len(cleaned) <= 15):
        return False, f"Phone number looks off ({len(cleaned)} digits). Expected 7–15 digits."
    return True, ""


def validate_experience(text: str) -> tuple[bool, str]:
    """Must contain at least one digit."""
    if not re.search(r"\d", text):
        return False, "Please include a number, e.g. '3' or '5+ years'."
    return True, ""


def validate_position(text: str) -> tuple[bool, str]:
    """Free text, just needs some content."""
    if len(text.strip()) < 3:
        return False, "Please describe the role(s) you're applying for."
    return True, ""


def validate_location(text: str) -> tuple[bool, str]:
    """Free text, just needs some content."""
    if len(text.strip()) < 2:
        return False, "Please share your city and country."
    return True, ""


def validate_tech_stack(text: str) -> tuple[bool, str]:
    """Should mention at least one recognisable tech keyword."""
    if len(text.strip()) < 3:
        return False, "Please list your technologies, e.g. Python, React, PostgreSQL."
    return True, ""


# Stage → validator mapping
VALIDATORS = {
    "collect_name":       validate_name,
    "collect_email":      validate_email,
    "collect_phone":      validate_phone,
    "collect_experience": validate_experience,
    "collect_position":   validate_position,
    "collect_location":   validate_location,
    "collect_tech_stack": validate_tech_stack,
}