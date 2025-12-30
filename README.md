# 💼 JobTrack

An AI-powered job application tracker to help manage your job search.

## ✨ Features

- **📋 Job Tracking** - Track applications through different stages with inline status editing
- **🔗 URL Import** - Paste a job URL to auto-extract company, position, location, and description
- **📄 Resume Management** - Upload PDF, DOCX, or TXT resumes with automatic text extraction
- **🎯 ATS Analyzer** - Check how well your resume matches a job description
- **✉️ Cover Letter Generator** - Generate personalized cover letters with AI
- **📊 Dashboard** - Track your progress with visual statistics

## 🚀 Quick Start

### Windows
```
Double-click start.bat
```

### Mac/Linux
```bash
chmod +x start.sh
./start.sh
```

Then open http://localhost:8000

## 💰 Free vs Paid Mode

JobTrack offers two modes to accommodate different needs:

### 🆓 Free Mode (Default)
No API costs! Uses:
- **ATS Analysis**: Smart keyword matching algorithm
- **Cover Letters**: Ollama (free, runs locally)
- **URL Import**: HTML parsing with regex

**Setup for Cover Letters (Optional):**
1. Install Ollama: https://ollama.ai
2. Run: `ollama pull llama3.2`
3. That's it!

### 💳 Claude Mode (Paid)
Higher quality AI features using Claude API:
- More nuanced ATS analysis
- Better cover letter generation  
- Smarter URL extraction

**Setup:**
1. Get API key: https://console.anthropic.com/
2. Edit `backend/app/config.py`:
   ```python
   AI_MODE = "claude"
   ```
3. Create `.env` file:
   ```
   ANTHROPIC_API_KEY=your-key-here
   ```

## 📁 Project Structure

```
jobtrack/
├── backend/
│   └── app/
│       ├── main.py           # API endpoints
│       ├── database.py       # SQLite database
│       ├── models.py         # Data models
│       ├── config.py         # AI mode config
│       ├── ats_service.py    # Claude AI service (paid)
│       ├── ats_service_free.py  # Free alternatives
│       └── file_service.py   # Resume parsing
├── frontend/
│   └── index.html           # Web interface
├── start.bat                # Windows launcher
├── start.sh                 # Mac/Linux launcher
└── requirements.txt
```

## 🛠️ Manual Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/gabrielanot/jobtrack.git
   cd jobtrack
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Mac/Linux
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python -m uvicorn backend.app.main:app --reload
   ```

5. **Open** http://localhost:8000

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/jobs` | GET, POST | List/create jobs |
| `/api/jobs/{id}` | GET, PUT, DELETE | Get/update/delete job |
| `/api/resumes` | GET, POST | List/create resumes |
| `/api/resumes/upload` | POST | Upload resume file |
| `/api/resumes/{id}/content` | GET | Get resume text |
| `/api/analyze-ats` | POST | Analyze resume vs job |
| `/api/generate-cover-letter` | POST | Generate cover letter |
| `/api/ats/extract-from-url` | POST | Extract job from URL |
| `/api/info` | GET | Get API/AI mode info |

## 🤝 Contributing

This is an open-source learning project! Contributions welcome.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use and modify!

## 🐛 Issues & Feedback

Found a bug or have a suggestion? [Open an issue](https://github.com/gabrielanot/jobtrack/issues)

---

Made with ❤️ for job seekers everywhere