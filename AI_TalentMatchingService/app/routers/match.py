from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.matching import rank_candidates_for_job
from app.services.llm import ask_question_about_candidate

router = APIRouter(prefix="/match", tags=["Match"])

@router.get("/best-candidate/{job_id}")
def best_candidate(job_id: str, db: Session = Depends(get_db)):
    return rank_candidates_for_job(job_id, db)[0]

@router.get("/all-candidates/{job_id}")
def all_candidates(job_id: str, db: Session = Depends(get_db)):
    return rank_candidates_for_job(job_id, db)

@router.get("/explain/{candidate_id}/{job_id}")
def explain_match(
    candidate_id: str,
    job_id: str,
    question: str = Query(...),
    db: Session = Depends(get_db)
):
    return ask_question_about_candidate(candidate_id, job_id, question, db)