from sqlalchemy.orm import Session
from app.db import models
from app.services.llm import summarize_match
from app.services.embeddings import compute_embedding_similarity

def seniority_alignment(candidate, job):
    diff = abs(candidate - job)
    if diff > 0.5:
        return 0.0
    return 1 - diff

def compare_candidate_job(candidate_id, job_id, db):
    # 1. Load data
    resume_chunks = db.query(models.ResumeChunk).filter_by(candidate_id=candidate_id).all()
    job_chunks = db.query(models.JobChunk).filter_by(job_id=job_id).all()
    resume_text = " ".join([c.content for c in resume_chunks])
    job_text = " ".join([j.content for j in job_chunks])

    # 2. Extract Seniority
    candidate_sen = extract_seniority(resume_text)
    job_sen = extract_job_seniority(job_text)
    
    # 3. Security Override
    # This prevents students with no jobs from ranking too high
    if not any(word in resume_text.lower() for word in ["experience", "work", "history"]):
        candidate_sen = min(candidate_sen, 0.2)

    # 4. Calculate Scores
    avg_score = compute_embedding_similarity(resume_chunks, job_chunks)
    sen_alignment = 1.0 - abs(job_sen - candidate_sen)

    # 5. Calculate Semantic similarity and Base Alignment
    avg_score = compute_embedding_similarity(resume_chunks, job_chunks)
    sen_alignment = 1.0 - abs(job_sen - candidate_sen)
    
    # Start with the base weighted average (30/70 split)
    calculated_score = (0.3 * avg_score) + (0.7 * sen_alignment)

    # 6. Apply Hard Penalty for Mismatch
    if candidate_sen <= 0.3 and job_sen >= 0.6:
        print(f"--- PENALTY TRIGGERED FOR {candidate_id} ---")
        calculated_score = calculated_score * 0.5 
    else:
        print(f"DEBUG: No penalty for {candidate_id}. Job:{job_sen}, Cand:{candidate_sen}")
    
    # 7. Final Normalize and assign to final_score
    final_score = max(0.0, min(calculated_score, 1.0))
    print(f"DEBUG: {candidate_id} final_score is {final_score}")

    # 8. LLM summary
    summary = summarize_match(resume_text=resume_text, job_text=job_text)

    return {
        "candidate_id": candidate_id,
        "match_score": round(final_score, 4),
        "seniority_detected": candidate_sen,
        "summary": summary
    }

def rank_candidates_for_job(job_id, db: Session):
    candidates = db.query(models.ResumeChunk.candidate_id).distinct()
    results = [compare_candidate_job(c[0], job_id, db) for c in candidates]
    return sorted(results, key=lambda x: x["match_score"], reverse=True)


def rank_jobs_for_candidate(candidate_id, db: Session):
    jobs = db.query(models.JobChunk.job_id).distinct()
    results = [compare_candidate_job(candidate_id, j[0], db) for j in jobs]
    return sorted(results, key=lambda x: x["match_score"], reverse=True)

def extract_seniority(text: str) -> float:
    text = text.lower()
    
    # 1. Check for Mid-Senior/3+ Years
    if any(k in text for k in ["3+ years", "3 years", "4 years", "5 years", "software engineer ii"]):
        return 0.6
    
    # 2. Check for Professional Experience
    if any(k in text for k in ["2+ years", "2 years", "backend developer", "software engineer"]):
        return 0.5 
    
    # 3. Check for Junior
    if any(k in text for k in ["junior", "entry level", "1 year"]):
        return 0.3
        
    # 4. Check for Intern/Aspiring
    if any(k in text for k in ["intern", "aspiring", "student", "recent grad", "2024"]):
        return 0.1
        
    return 0.2


def extract_job_seniority(text: str) -> float:
    text = text.lower()

    if "software engineer iii" in text or "senior" in text:
        return 0.8
    if "software engineer ii" in text or "mid" in text or "3+ years" in text:
        return 0.6
    if "software engineer i" in text or "junior" in text:
        return 0.3
    if "principal" in text or "staff" in text:
        return 0.95

    return 0.5