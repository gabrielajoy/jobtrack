"""
JobTrack FastAPI Application
Main entry point for the API
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
import sqlite3

from .database import db, get_db
from .models import Job, JobCreate, JobUpdate


# Initialize FastAPI app
app = FastAPI(
    title="JobTrack API",
    description="API for tracking job applications",
    version="1.0.0"
)

# Configure CORS (allows frontend to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """Initialize database on app startup"""
    db.initialize_schema()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "JobTrack API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api/jobs", response_model=List[Job])
async def get_jobs(
    status: str = None,
    conn: sqlite3.Connection = Depends(get_db)
):
    """
    Get all jobs, optionally filtered by status
    
    - **status**: Filter by job status (wishlist, applied, interviewing, offer, rejected)
    """
    cursor = conn.cursor()
    
    if status:
        cursor.execute(
            "SELECT * FROM jobs WHERE status = ? ORDER BY date_added DESC",
            (status,)
        )
    else:
        cursor.execute("SELECT * FROM jobs ORDER BY date_added DESC")
    
    jobs = cursor.fetchall()
    return [dict(job) for job in jobs]


@app.post("/api/jobs", response_model=Job, status_code=201)
async def create_job(
    job: JobCreate,
    conn: sqlite3.Connection = Depends(get_db)
):
    """
    Create a new job application
    
    - **company**: Company name (required)
    - **position**: Job position (required)
    - **location**: Job location
    - **job_url**: Link to job posting
    - **salary_min**: Minimum salary
    - **salary_max**: Maximum salary
    - **status**: Current status (default: wishlist)
    - **notes**: Additional notes
    """
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO jobs (company, position, location, job_url, salary_min, 
                         salary_max, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        job.company, job.position, job.location, job.job_url,
        job.salary_min, job.salary_max, job.status, job.notes
    ))
    
    conn.commit()
    job_id = cursor.lastrowid
    
    # Fetch the created job
    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    created_job = cursor.fetchone()
    
    return dict(created_job)


@app.get("/api/jobs/{job_id}", response_model=Job)
async def get_job(
    job_id: int,
    conn: sqlite3.Connection = Depends(get_db)
):
    """Get a specific job by ID"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = cursor.fetchone()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return dict(job)


@app.put("/api/jobs/{job_id}", response_model=Job)
async def update_job(
    job_id: int,
    job_update: JobUpdate,
    conn: sqlite3.Connection = Depends(get_db)
):
    """Update a job application"""
    cursor = conn.cursor()
    
    # Check if job exists
    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Build UPDATE query dynamically for provided fields
    update_fields = []
    values = []
    
    for field, value in job_update.model_dump(exclude_unset=True).items():
        update_fields.append(f"{field} = ?")
        values.append(value)
    
    if update_fields:
        values.append(job_id)
        query = f"UPDATE jobs SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
    
    # Return updated job
    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    updated_job = cursor.fetchone()
    
    return dict(updated_job)


@app.delete("/api/jobs/{job_id}", status_code=204)
async def delete_job(
    job_id: int,
    conn: sqlite3.Connection = Depends(get_db)
):
    """Delete a job application"""
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    
    conn.commit()
    return None


@app.get("/api/stats")
async def get_stats(conn: sqlite3.Connection = Depends(get_db)):
    """Get analytics and statistics"""
    cursor = conn.cursor()
    
    # Total jobs by status
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM jobs
        GROUP BY status
    """)
    status_counts = {row['status']: row['count'] for row in cursor.fetchall()}
    
    # Total jobs
    cursor.execute("SELECT COUNT(*) as total FROM jobs")
    total = cursor.fetchone()['total']
    
    # Recent activity
    cursor.execute("""
        SELECT DATE(date_added) as date, COUNT(*) as count
        FROM jobs
        WHERE date_added >= date('now', '-30 days')
        GROUP BY DATE(date_added)
        ORDER BY date
    """)
    recent_activity = [dict(row) for row in cursor.fetchall()]
    
    return {
        "total_jobs": total,
        "by_status": status_counts,
        "recent_activity": recent_activity
    }
