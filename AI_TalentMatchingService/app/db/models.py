from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.db.database import Base

# Confirm correct file is loading
print(">>> USING VECTOR SIZE:", 768)


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=True)

    chunks = relationship("ResumeChunk", back_populates="candidate")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=True)

    chunks = relationship("JobChunk", back_populates="job")


class ResumeChunk(Base):
    __tablename__ = "resume_chunks"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(String, ForeignKey("candidates.id"), index=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(768))
    candidate = relationship("Candidate", back_populates="chunks")

class JobChunk(Base):
    __tablename__ = "job_chunks"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("jobs.id"), index=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(768))
    job = relationship("Job", back_populates="chunks")