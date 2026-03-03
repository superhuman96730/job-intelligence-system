from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from database import engine, Base, SessionLocal
from models import Job
from scorer import calculate_score

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def dashboard(request: Request):
    db = SessionLocal()
    jobs = db.query(Job).all()

    for job in jobs:
        job.match_score = calculate_score(job.description or "")
    db.commit()

    sorted_jobs = sorted(jobs, key=lambda x: x.match_score, reverse=True)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "jobs": sorted_jobs
    })