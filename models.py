from sqlalchemy import Column, String, Text, Float
from database import Base

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True)
    company = Column(String)
    title = Column(String)
    description = Column(Text)
    location = Column(String)
    url = Column(String)
    match_score = Column(Float, default=0.0)