# Predefined skill taxonomy for resume screening & keyword extraction.
# You can extend this list with additional technical & soft skills as needed.

SKILLS_LIST = [
    "python", "java", "c++", "c", "javascript", "typescript", "html", "css",
    "react", "angular", "vue", "node.js", "express", "flask", "django",
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "redis",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    "data analysis", "data science", "power bi", "tableau", "excel",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "github",
    "linux", "rest api", "graphql", "agile", "scrum",
    "communication", "leadership", "problem solving", "teamwork",
    "project management", "figma", "ui/ux", "photoshop",
]


def extract_skills(text):
    """
    Extracts matched skills from a given text (resume or job description)
    against the predefined SKILLS_LIST taxonomy.
    """
    if not text:
        return []

    text = text.lower()
    found_skills = []

    for skill in SKILLS_LIST:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


def compare_skills(resume_skills, job_skills):
    """
    Compares extracted candidate resume skills with job description requirements.
    Returns matched skills, missing skill gaps, and the overall match percentage.
    """
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = sorted(resume_set & job_set)          # Present in both resume & job description
    missing = sorted(job_set - resume_set)           # Required in job but missing from resume

    if len(job_set) == 0:
        percentage = 0
    else:
        percentage = round((len(matched) / len(job_set)) * 100, 2)

    return matched, missing, percentage

