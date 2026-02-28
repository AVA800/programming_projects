import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def llm(prompt: str) -> str:
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )

    if resp.status_code != 200:
        raise Exception(f"LLM request failed: {resp.status_code} {resp.text}")

    data = resp.json()

    if "response" not in data:
        raise Exception(f"Invalid LLM response: {data}")

    return data["response"]


def summarize_match(    
    resume_text,
    job_text
):
    prompt = f"""
    Analyze the Candidate Resume against the Job Requirements. 
    
    RULES FOR ACCURACY:
    1. 'OR' LOGIC: If a job asks for 'FastAPI or Go', and the candidate has one, mark it as a STRENGTH, not a gap.
    2. CERTIFICATIONS: If the job asks for 'Cloud Practitioner or higher' and the candidate has 'Cloud Practitioner', it is a FULL MATCH.
    3. NO ASSUMPTIONS: Do not assume a candidate knows AWS just because they know Docker. If it is not on the resume, it is a MISSING SKILL.
    4. SENIORITY: Explicitly mention if the candidate meets the '3+ years' requirement.
    5. SENIORITY VERIFICATION: If the candidate is a recent graduate or 'aspiring', do NOT list '3+ years of experience' as a strength. Only list it if the resume explicitly shows dates totaling 3 years.
    JOB:
    {job_text}

    RESUME:
    {resume_text}

    FORMAT:
    **STRENGTHS**
    * (List matches here)
    **GAPS**
    * (List missing requirements here)
"""

    return llm(prompt)


def ask_question_about_candidate(candidate_id, job_id, question, db):
    from app.db import models

    resume_chunks = db.query(models.ResumeChunk).filter_by(candidate_id=candidate_id).all()
    job_chunks = db.query(models.JobChunk).filter_by(job_id=job_id).all()

    resume_text = "\n".join([c.content for c in resume_chunks])
    job_text = "\n".join([j.content for j in job_chunks])

    prompt = f"""
You are an AI hiring assistant.
Use ONLY the evidence provided in the resume and job description.
If a skill or experience is not explicitly mentioned, assume the candidate does NOT have it.
Do NOT infer or invent skills.
Do NOT assume seniority or years of experience unless stated.

Candidate ID: {candidate_id}
Job ID: {job_id}

Question: {question}

Resume Evidence:
{resume_text}

Job Requirements:
{job_text}

Answer the question using only the evidence above.
"""

    return {"answer": llm(prompt)}