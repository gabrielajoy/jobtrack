# JobTrack

An open-source, AI-powered job application tracker to help manage your job search.

## Features

- **Job Tracking** - Track applications through stages: wishlist → applied → interviewing → offer → rejected
- **Resume Management** - Store multiple resume versions with metadata
- **AI ATS Analyzer** - Check resume-job fit with Claude AI, get missing keywords and suggestions
- **AI Cover Letter Generator** - Generate personalized cover letters in different tones
- **Analytics Dashboard** - View job counts by status and recent activity
- **Modern Frontend** - Dark-themed dashboard with responsive design

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python + FastAPI |
| Database | SQLite |
| AI/LLM | Anthropic Claude API |
| Frontend | HTML + CSS + JavaScript |
| CI/CD | GitHub Actions |

## Getting Started

### Prerequisites

- Python 3.9+
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/gabrielajoy/jobtrack.git
   cd jobtrack
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Create .env file in project root
   echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
   ```

4. **Run the application:**
   ```bash
   python -m uvicorn backend.app.main:app --reload
   ```

5. **Open your browser:**
   - Frontend: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

## Project Structure

```
jobtrack/
├── backend/
│   └── app/
│       ├── main.py          # FastAPI app + endpoints
│       ├── database.py      # SQLite schema
│       ├── models.py        # Pydantic models
│       └── ats_service.py   # AI analysis service
├── frontend/
│   └── index.html           # Dashboard UI
├── tests/
│   └── test_api.py          # API tests
├── scripts/
│   └── generate_data.py     # Sample data generator
├── docs/
│   └── CONTRIBUTING.md
├── .env                     # API keys (not in repo)
├── requirements.txt
└── README.md
```

## API Endpoints

### Jobs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/jobs` | List all jobs (optional `?status=` filter) |
| POST | `/api/jobs` | Create new job |
| GET | `/api/jobs/{id}` | Get single job |
| PUT | `/api/jobs/{id}` | Update job |
| DELETE | `/api/jobs/{id}` | Delete job |
| GET | `/api/stats` | Get analytics |

### Resumes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/resumes` | List all resumes |
| POST | `/api/resumes` | Register new resume |
| GET | `/api/resumes/{id}` | Get single resume |
| PUT | `/api/resumes/{id}` | Update resume |

### AI Features
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/analyze-ats` | Analyze resume against job description |
| POST | `/api/generate-cover-letter` | Generate personalized cover letter |

## Frontend

The frontend is a single-page dashboard built with vanilla HTML/CSS/JS.

### Pages

- **Dashboard** - Overview stats and recent applications
- **Jobs** - Full job list with status filter tabs
- **ATS Analyzer** - Paste resume + job description, get AI analysis
- **Cover Letter** - Generate cover letters with tone selection
- **Resumes** - Manage saved resume versions

### Customization

**Change API URL** (if running on different port):
```javascript
// In frontend/index.html, line 1 of <script>
const API_URL = 'http://localhost:8000';
```

**Change theme colors:**
```css
/* In frontend/index.html, CSS :root variables */
:root {
    --accent-primary: #6366f1;
    --bg-primary: #0a0a0f;
    /* ... */
}
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=backend
```

## Development

### Adding a new feature

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make changes and commit:
   ```bash
   git add .
   git commit -m "Add: Your feature description"
   ```

3. Push and create PR:
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit message convention

- `Add:` New feature or file
- `Fix:` Bug fix
- `Update:` Modify existing feature
- `Remove:` Delete code/file
- `Docs:` Documentation only

## Roadmap

- [x] Job tracking CRUD
- [x] Resume storage
- [x] AI ATS analysis
- [x] AI cover letter generator
- [x] Frontend dashboard
- [ ] Resume file upload (PDF/DOCX parsing)
- [ ] Contact management
- [ ] Interview scheduling
- [ ] Email notifications
- [ ] User authentication

## Contributing

This is a learning project and open for contributions! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## License

MIT License - feel free to use and modify!

---

**Built by [@gabrielajoy](https://github.com/gabrielajoy)**
