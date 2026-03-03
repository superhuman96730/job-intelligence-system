import re

KEYWORDS = ["python", "c++", "unity", "fastapi", "aws", "docker", "rest", "api", "sql"]

def extract_keywords(text):
    found = []
    text_lower = text.lower()
    for word in KEYWORDS:
        if re.search(r"\b" + word + r"\b", text_lower):
            found.append(word)
    return found