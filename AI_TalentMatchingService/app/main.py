from fastapi import FastAPI
from app.db.database import Base, engine, init_vector_extension
from app.routers import health, analyze, match

init_vector_extension()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Driven Talent Matching Engine",
    version="1.0",
    description="AI system for analyzing resumes and job postings to rank candidates using embeddings and seniority-aware LLM reasoning."
)

# Routers
app.include_router(health.router)
app.include_router(analyze.router)
app.include_router(match.router)