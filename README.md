# JobTrack

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
