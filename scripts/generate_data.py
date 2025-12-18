"""Generate sample job data for testing"""

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
    """Generate random job applications"""
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
        
        cursor.execute("""
            INSERT INTO jobs (company, position, location, salary_min, 
                            salary_max, status, date_added)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (company, position, location, salary_min, salary_max, status, date_added))
    
    conn.commit()
    db.close()
    print(f"Generated {num_jobs} sample jobs")

if __name__ == "__main__":
    generate_jobs(20)
