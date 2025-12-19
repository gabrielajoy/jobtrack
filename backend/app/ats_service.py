"""
ATS Analysis Service
Uses Claude API to analyze resumes against job descriptions
"""

from dotenv import load_dotenv
load_dotenv()  # Load .env file
import os
from anthropic import Anthropic

# Initialize the client (reads ANTHROPIC_API_KEY from environment)
client = Anthropic()


def analyze_resume_ats(resume_text: str, job_description: str) -> dict:
    """
    Analyze a resume against a job description for ATS compatibility.
    
    Returns:
        dict with score, missing_keywords, suggestions, and summary
    """
    
    prompt = f"""You are an expert ATS (Applicant Tracking System) analyzer and career coach.

Analyze this resume against the job description and provide:
1. An ATS compatibility score from 0-100
2. Keywords from the job description that are MISSING from the resume
3. Specific suggestions to improve the resume for this role
4. A brief summary of the analysis

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Respond in this exact JSON format (no markdown, just pure JSON):
{{
    "score": <number 0-100>,
    "missing_keywords": ["keyword1", "keyword2", ...],
    "suggestions": ["suggestion1", "suggestion2", ...],
    "summary": "Brief 2-3 sentence summary of the analysis"
}}
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Parse the response
    response_text = message.content[0].text
    
    # Parse JSON from response
    import json
    try:
        result = json.loads(response_text)
    except json.JSONDecodeError:
        # If parsing fails, return a default structure
        result = {
            "score": 0,
            "missing_keywords": [],
            "suggestions": ["Could not analyze - please try again"],
            "summary": response_text
        }
    
    return result


def generate_cover_letter(
    resume_text: str, 
    job_description: str, 
    company_name: str,
    tone: str = "professional"
) -> str:
    """
    Generate a personalized cover letter.
    
    Args:
        resume_text: The candidate's resume
        job_description: The job posting
        company_name: Name of the company
        tone: Writing tone (professional, enthusiastic, conversational)
    
    Returns:
        Generated cover letter text
    """
    
    prompt = f"""You are an expert career coach and professional writer.

Write a compelling cover letter for this candidate applying to {company_name}.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

INSTRUCTIONS:
- Tone: {tone}
- Length: 3-4 paragraphs
- Highlight relevant experience from the resume
- Show enthusiasm for the specific role and company
- Include a strong opening and call to action
- Do NOT use placeholder text like [Your Name] - write it as a complete letter

Write the cover letter now:"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text