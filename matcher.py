import re
from config import SKILLS, EXCLUDE_KEYWORDS

def score_job(title, description, company=None):
    text = f"{title} {description} {company or ''}".lower()
    parts = {"title": title.lower(), "desc": description.lower(), "company": (company or "").lower()}
    combined = parts["title"] + " " + parts["desc"]

    has_go = bool(re.search(r'\bgolang\b', combined)) or bool(re.search(r'\bgo\b', combined))
    if not has_go:
        return 0.0

    for ex in EXCLUDE_KEYWORDS:
        if re.search(ex.lower(), text):
            return 0.0

    score = 0.0
    weights = {"high_priority": 15, "medium_priority": 8, "bonus": 5}

    for category, skills in SKILLS.items():
        weight = weights.get(category, 5)
        for skill in skills:
            if skill in ("go", "golang", "remote"):
                continue
            if re.search(r'\b' + re.escape(skill) + r'\b', text):
                score += weight
                if re.search(r'\b' + re.escape(skill) + r'\b', parts["title"]):
                    score += weight * 0.5

    max_possible = sum(
        sum(weights.get(cat, 5) * 1.5 for _ in SKILLS[cat])
        for cat in ["high_priority", "medium_priority", "bonus"]
    )
    normalized = min(round(score / max_possible * 100, 1), 100.0) if max_possible > 0 else 0.0
    return normalized


def get_matched_skills(title, description, company=None):
    text = f"{title} {description} {company or ''}".lower()
    matched = []
    for category, skills in SKILLS.items():
        for skill in skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text):
                matched.append(skill)
    return matched
