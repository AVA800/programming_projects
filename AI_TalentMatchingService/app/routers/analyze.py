from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.utils.pdf import extract_text_from_pdf
from app.services.chunking import chunk_text
from app.services.embeddings import embed_text

router = APIRouter(prefix="/analyze", tags=["Analyze"])

# Upload Resume
@router.post("/resume")
async def upload_resume(
    candidate_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Ensure candidate exists
    candidate = db.query(models.Candidate).filter_by(id=candidate_id).first()
    if not candidate:
        candidate = models.Candidate(id=candidate_id)
        db.add(candidate)
        db.commit()

    # Extract text from PDF
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    # Chunk text
    chunks = chunk_text(text)

    # Save chunks with embeddings
    for chunk in chunks:
        embedding = embed_text(chunk)
        db.add(models.ResumeChunk(
            candidate_id=candidate_id,
            content=chunk,
            embedding=embedding
        ))

    db.commit()
    return {"message": "Resume processed", "candidate_id": candidate_id}

# Upload Job Description
@router.post("/job")
async def upload_job(
    job_id: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    # Ensure job exists
    job = db.query(models.Job).filter_by(id=job_id).first()
    if not job:
        job = models.Job(id=job_id)
        db.add(job)
        db.commit()

    # Chunk job description
    chunks = chunk_text(description)

    # Save chunks with embeddings
    for chunk in chunks:
        embedding = embed_text(chunk)
        db.add(models.JobChunk(
            job_id=job_id,
            content=chunk,
            embedding=embedding
        ))

    db.commit()
    return {"message": "Job processed", "job_id": job_id}