#!/usr/bin/env python3
"""
JobTrack Setup Script
Creates the complete project structure for your job tracking application
"""

import os
import sys
from pathlib import Path


def create_file(path, content=""):
    """Create a file with optional content"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")


def setup_jobtrack():
    """Create the complete JobTrack project structure"""
    
    print("Setting up JobTrack project...\n")
    
    # Base directory
    base = Path("jobtrack")
    base.mkdir(exist_ok=True)
    
    # .gitignore
    gitignore = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Database
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Environment
.env
"""
    create_file(base / ".gitignore", gitignore)
    
    # README.md
    readme = """# JobTrack

An open-source job application tracker to help manage your job search.

## Features

- Track job applications through different stages
- Store company info, salaries, and important dates
- Manage interview schedules and notes
- Analytics dashboard to track your progress

## Tech Stack

- **Backend**: Python + FastAPI
- **Database**: SQLite
- **Frontend**: HTML + JavaScript
- **CI/CD**: GitHub Actions

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python -m uvicorn backend.app.main:app --reload
   ```

3. Open your browser to `http://localhost:8000`

## Project Structure

```
jobtrack/
├── backend/          # API and database
├── frontend/         # Web interface
├── tests/           # Automated tests
└── docs/            # Documentation
```

## Contributing

This is a learning project and open for contributions! See CONTRIBUTING.md for guidelines.

## License

MIT License - feel free to use and modify!
"""
    create_file(base / "README.md", readme)
    
    # requirements.txt
    requirements = """# Core dependencies
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
python-multipart==0.0.6

# Database
aiosqlite==0.19.0

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0

# Code quality
ruff==0.1.13
"""
    create_file(base / "requirements.txt", requirements)
    
    # Backend structure
    backend = base / "backend"
    
    # backend/__init__.py
    create_file(backend / "__init__.py", "")
    
    # backend/app/__init__.py
    create_file(backend / "app" / "__init__.py", "")
    
    # backend/app/database.py
    database_code = """\"\"\"
Database initialization and connection management
\"\"\"

import sqlite3
from pathlib import Path
from typing import Optional


class Database:
    \"\"\"Handle SQLite database operations\"\"\"
    
    def __init__(self, db_path: str = "jobtrack.db"):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
    
    def connect(self):
        \"\"\"Establish database connection\"\"\"
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Return rows as dictionaries
        return self.connection
    
    def close(self):
        \"\"\"Close database connection\"\"\"
        if self.connection:
            self.connection.close()
    
    def initialize_schema(self):
        \"\"\"Create database tables if they don't exist\"\"\"
        conn = self.connect()
        cursor = conn.cursor()
        
        # Jobs table
        cursor.execute(\"\"\"
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                position TEXT NOT NULL,
                location TEXT,
                job_url TEXT,
                salary_min INTEGER,
                salary_max INTEGER,
                status TEXT DEFAULT 'wishlist',
                date_added DATE DEFAULT CURRENT_DATE,
                date_applied DATE,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        \"\"\")
        
        # Contacts table
        cursor.execute(\"\"\"
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER,
                name TEXT,
                role TEXT,
                email TEXT,
                phone TEXT,
                FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
            )
        \"\"\")
        
        # Interviews table
        cursor.execute(\"\"\"
            CREATE TABLE IF NOT EXISTS interviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER,
                interview_date DATETIME,
                interview_type TEXT,
                notes TEXT,
                FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
            )
        \"\"\")
        
        conn.commit()
        self.close()
        print("Database schema initialized")


# Global database instance
db = Database()


def get_db():
    \"\"\"Dependency for FastAPI endpoints\"\"\"
    connection = db.connect()
    try:
        yield connection
    finally:
        connection.close()
"""
    create_file(backend / "app" / "database.py", database_code)
    
    # backend/app/models.py
    models_code = """\"\"\"
Pydantic models for request/response validation
\"\"\"

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class JobBase(BaseModel):
    \"\"\"Base job model with common fields\"\"\"
    company: str = Field(..., min_length=1, max_length=200)
    position: str = Field(..., min_length=1, max_length=200)
    location: Optional[str] = None
    job_url: Optional[str] = None
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    status: str = Field(default="wishlist")
    notes: Optional[str] = None


class JobCreate(JobBase):
    \"\"\"Model for creating a new job\"\"\"
    pass


class JobUpdate(BaseModel):
    \"\"\"Model for updating a job (all fields optional)\"\"\"
    company: Optional[str] = None
    position: Optional[str] = None
    location: Optional[str] = None
    job_url: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    status: Optional[str] = None
    date_applied: Optional[date] = None
    notes: Optional[str] = None


class Job(JobBase):
    \"\"\"Complete job model with all fields\"\"\"
    id: int
    date_added: date
    date_applied: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ContactBase(BaseModel):
    \"\"\"Base contact model\"\"\"
    job_id: int
    name: str
    role: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class ContactCreate(ContactBase):
    \"\"\"Model for creating a contact\"\"\"
    pass


class Contact(ContactBase):
    \"\"\"Complete contact model\"\"\"
    id: int
    
    class Config:
        from_attributes = True


class InterviewBase(BaseModel):
    \"\"\"Base interview model\"\"\"
    job_id: int
    interview_date: datetime
    interview_type: Optional[str] = None
    notes: Optional[str] = None


class InterviewCreate(InterviewBase):
    \"\"\"Model for creating an interview\"\"\"
    pass


class Interview(InterviewBase):
    \"\"\"Complete interview model\"\"\"
    id: int
    
    class Config:
        from_attributes = True
"""
    create_file(backend / "app" / "models.py", models_code)
    
    # backend/app/main.py
    main_code = """\"\"\"
JobTrack FastAPI Application
Main entry point for the API
\"\"\"

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
    \"\"\"Initialize database on app startup\"\"\"
    db.initialize_schema()


@app.get("/")
async def root():
    \"\"\"Health check endpoint\"\"\"
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
    \"\"\"
    Get all jobs, optionally filtered by status
    
    - **status**: Filter by job status (wishlist, applied, interviewing, offer, rejected)
    \"\"\"
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
    \"\"\"
    Create a new job application
    
    - **company**: Company name (required)
    - **position**: Job position (required)
    - **location**: Job location
    - **job_url**: Link to job posting
    - **salary_min**: Minimum salary
    - **salary_max**: Maximum salary
    - **status**: Current status (default: wishlist)
    - **notes**: Additional notes
    \"\"\"
    cursor = conn.cursor()
    
    cursor.execute(\"\"\"
        INSERT INTO jobs (company, position, location, job_url, salary_min, 
                         salary_max, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    \"\"\", (
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
    \"\"\"Get a specific job by ID\"\"\"
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
    \"\"\"Update a job application\"\"\"
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
    \"\"\"Delete a job application\"\"\"
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    
    conn.commit()
    return None


@app.get("/api/stats")
async def get_stats(conn: sqlite3.Connection = Depends(get_db)):
    \"\"\"Get analytics and statistics\"\"\"
    cursor = conn.cursor()
    
    # Total jobs by status
    cursor.execute(\"\"\"
        SELECT status, COUNT(*) as count
        FROM jobs
        GROUP BY status
    \"\"\")
    status_counts = {row['status']: row['count'] for row in cursor.fetchall()}
    
    # Total jobs
    cursor.execute("SELECT COUNT(*) as total FROM jobs")
    total = cursor.fetchone()['total']
    
    # Recent activity
    cursor.execute(\"\"\"
        SELECT DATE(date_added) as date, COUNT(*) as count
        FROM jobs
        WHERE date_added >= date('now', '-30 days')
        GROUP BY DATE(date_added)
        ORDER BY date
    \"\"\")
    recent_activity = [dict(row) for row in cursor.fetchall()]
    
    return {
        "total_jobs": total,
        "by_status": status_counts,
        "recent_activity": recent_activity
    }
"""
    create_file(backend / "app" / "main.py", main_code)
    
    # Tests
    tests_dir = base / "tests"
    create_file(tests_dir / "__init__.py", "")
    
    test_code = """\"\"\"
API Tests for JobTrack
\"\"\"

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import db


@pytest.fixture
def client():
    \"\"\"Create a test client\"\"\"
    # Use in-memory database for tests
    db.db_path = ":memory:"
    db.initialize_schema()
    
    with TestClient(app) as test_client:
        yield test_client


def test_root(client):
    \"\"\"Test root endpoint\"\"\"
    response = client.get("/")
    assert response.status_code == 200
    assert "JobTrack API" in response.json()["message"]


def test_create_job(client):
    \"\"\"Test creating a job\"\"\"
    job_data = {
        "company": "Tech Corp",
        "position": "Product Manager",
        "location": "Remote",
        "status": "wishlist"
    }
    
    response = client.post("/api/jobs", json=job_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["company"] == "Tech Corp"
    assert data["position"] == "Product Manager"
    assert "id" in data


def test_get_jobs(client):
    \"\"\"Test getting all jobs\"\"\"
    # Create a job first
    client.post("/api/jobs", json={
        "company": "Test Company",
        "position": "Developer"
    })
    
    response = client.get("/api/jobs")
    assert response.status_code == 200
    
    jobs = response.json()
    assert len(jobs) > 0


def test_get_job_by_id(client):
    \"\"\"Test getting a specific job\"\"\"
    # Create a job
    create_response = client.post("/api/jobs", json={
        "company": "Example Corp",
        "position": "Engineer"
    })
    job_id = create_response.json()["id"]
    
    # Get the job
    response = client.get(f"/api/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json()["company"] == "Example Corp"


def test_update_job(client):
    \"\"\"Test updating a job\"\"\"
    # Create a job
    create_response = client.post("/api/jobs", json={
        "company": "Old Company",
        "position": "Role"
    })
    job_id = create_response.json()["id"]
    
    # Update the job
    response = client.put(f"/api/jobs/{job_id}", json={
        "status": "applied"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "applied"


def test_delete_job(client):
    \"\"\"Test deleting a job\"\"\"
    # Create a job
    create_response = client.post("/api/jobs", json={
        "company": "Delete Me",
        "position": "Test"
    })
    job_id = create_response.json()["id"]
    
    # Delete the job
    response = client.delete(f"/api/jobs/{job_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(f"/api/jobs/{job_id}")
    assert get_response.status_code == 404


def test_get_stats(client):
    \"\"\"Test analytics endpoint\"\"\"
    response = client.get("/api/stats")
    assert response.status_code == 200
    
    data = response.json()
    assert "total_jobs" in data
    assert "by_status" in data
"""
    create_file(tests_dir / "test_api.py", test_code)
    
    # GitHub Actions CI
    workflows_dir = base / ".github" / "workflows"
    ci_yaml = """name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/ -v
    
    - name: Lint with Ruff
      run: |
        ruff check backend/
"""
    create_file(workflows_dir / "ci.yml", ci_yaml)
    
    # Frontend placeholder
    frontend_dir = base / "frontend"
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JobTrack - Job Application Tracker</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>JobTrack</h1>
            <p>Track your job applications</p>
        </header>
        
        <main>
            <section class="add-job">
                <h2>Add New Job</h2>
                <p>Coming soon in Week 3!</p>
            </section>
            
            <section class="job-list">
                <h2>Your Jobs</h2>
                <p>API will be ready after Week 2</p>
            </section>
        </main>
    </div>
    
    <script src="app.js"></script>
</body>
</html>
"""
    create_file(frontend_dir / "index.html", html)
    
    css = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    background: #f5f5f5;
    color: #333;
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    text-align: center;
    margin-bottom: 40px;
}

header h1 {
    font-size: 2.5rem;
    color: #2563eb;
}

/* More styles coming in Week 3! */
"""
    create_file(frontend_dir / "styles.css", css)
    
    js = """// JobTrack Frontend
// API integration coming in Week 3!

console.log('JobTrack loaded');

// Placeholder for future functionality
"""
    create_file(frontend_dir / "app.js", js)
    
    # Scripts directory
    scripts_dir = base / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    
    generate_data = """\"\"\"Generate sample job data for testing\"\"\"

import sqlite3
from datetime import datetime, timedelta
import random
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from backend.app.database import db

# Sample data
companies = ['Google', 'Meta', 'Amazon', 'Apple', 'Microsoft', 'Netflix', 'Tesla']
positions = ['Product Manager', 'Senior PM', 'Lead Product Manager', 'Technical PM']
locations = ['Remote', 'San Francisco', 'New York', 'Seattle', 'Austin']
statuses = ['wishlist', 'applied', 'interviewing', 'offer', 'rejected']

def generate_jobs(num_jobs=20):
    \"\"\"Generate random job applications\"\"\"
    # Initialize database first
    db.initialize_schema()
    
    conn = db.connect()
    cursor = conn.cursor()
    
    for _ in range(num_jobs):
        company = random.choice(companies)
        position = random.choice(positions)
        location = random.choice(locations)
        status = random.choice(statuses)
        salary_min = random.randint(100, 180) * 1000
        salary_max = salary_min + random.randint(20, 60) * 1000
        
        # Random date in last 60 days
        days_ago = random.randint(0, 60)
        date_added = (datetime.now() - timedelta(days=days_ago)).date()
        
        cursor.execute(\"\"\"
            INSERT INTO jobs (company, position, location, salary_min, 
                            salary_max, status, date_added)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        \"\"\", (company, position, location, salary_min, salary_max, status, date_added))
    
    conn.commit()
    db.close()
    print(f"Generated {num_jobs} sample jobs")

if __name__ == "__main__":
    generate_jobs(20)
"""
    create_file(scripts_dir / "generate_data.py", generate_data)
    
    # Contributing guide
    contributing = """# Contributing to JobTrack

Thank you for your interest in contributing! This is a learning project, and contributions are welcome.

## Getting Started

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run tests (`pytest tests/`)
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature`)
7. Open a Pull Request

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Write tests for new features

## Running Tests

```bash
pytest tests/ -v
```

## Questions?

Open an issue or reach out to the maintainer.
"""
    create_file(base / "docs" / "CONTRIBUTING.md", contributing)
    
    # pyproject.toml
    pyproject = """[tool.ruff]
line-length = 100
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
"""
    create_file(base / "pyproject.toml", pyproject)
    
    print("\nJobTrack project created successfully!")
    print(f"\nProject location: {base.absolute()}")
    print("\nNext steps:")
    print("   1. cd jobtrack")
    print("   2. git init")
    print("   3. pip install -r requirements.txt")
    print("   4. python -m uvicorn backend.app.main:app --reload")
    print("\nThen open http://localhost:8000/docs to see your API!\n")


if __name__ == "__main__":
    setup_jobtrack()