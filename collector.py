import requests
import feedparser
from database import SessionLocal
from models import Job

def fetch_greenhouse(company_slug):
    url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        print(f"[Greenhouse] {company_slug} fetch failed: {e}")
        return

    db = SessionLocal()
    for job in data.get("jobs", []):
        description = job.get("content", "")
        db.merge(Job(
            id=str(job["id"]),
            company=company_slug,
            title=job.get("title", "No Title"),
            description=description,
            location=job.get("location", {}).get("name", "Unknown"),
            url=job.get("absolute_url", "#")
        ))
    db.commit()
    db.close()
    print(f"[Greenhouse] {company_slug} done.")

def fetch_lever(company_slug):
    url = f"https://api.lever.co/v0/postings/{company_slug}?mode=json"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        print(f"[Lever] {company_slug} fetch failed: {e}")
        return

    db = SessionLocal()
    for job in data:
        description = job.get("descriptionPlain", "") or job.get("description", "")
        location = job.get("categories", {}).get("location", "Unknown")
        db.merge(Job(
            id=job["id"],
            company=company_slug,
            title=job.get("text", "No Title"),
            description=description,
            location=location,
            url=job.get("hostedUrl", "#")
        ))
    db.commit()
    db.close()
    print(f"[Lever] {company_slug} done.")

def fetch_rss(rss_url, company_name="Unknown"):
    try:
        feed = feedparser.parse(rss_url)
    except Exception as e:
        print(f"[RSS] {company_name} parse failed: {e}")
        return

    db = SessionLocal()
    for entry in feed.entries:
        job_id = entry.get("id") or entry.get("link")
        db.merge(Job(
            id=job_id,
            company=company_name,
            title=entry.get("title", "No Title"),
            description=entry.get("summary", ""),
            location="Unknown",
            url=entry.get("link", "#")
        ))
    db.commit()
    db.close()
    print(f"[RSS] {company_name} done.")

if __name__ == "__main__":
    # Greenhouse 테스트
    greenhouse_companies = ["airbnb", "stripe"]
    for c in greenhouse_companies:
        fetch_greenhouse(c)

    # # Lever 테스트
    # lever_companies = ["netflix", "coinbase"]
    # for c in lever_companies:
    #     fetch_lever(c)

    # # RSS 테스트 (예시)
    # rss_feeds = {
    #     "example_company": "https://www.example.com/jobs/rss"
    # }
    # for company, url in rss_feeds.items():
    #     fetch_rss(url, company)