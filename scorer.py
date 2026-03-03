from analyzer import extract_keywords

USER_SKILLS = ["python", "c++", "unity", "fastapi", "sql"]

def calculate_score(job_description):
    job_keywords = extract_keywords(job_description)
    score = 0
    for skill in USER_SKILLS:
        if skill in job_keywords:
            score += 20
    return min(score, 100)