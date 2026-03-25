# 📁 Project Structure

```
job-application-agent/
│
├── 📄 app.py                      # Main Flask application (entry point)
├── 📄 requirements.txt            # Python dependencies
├── 📄 Procfile                    # Deployment configuration
├── 📄 render.yaml                 # Render.com deployment config
├── 📄 .gitignore                  # Git ignore rules
├── 📄 .env                        # Environment variables (not in git)
├── 📄 README.md                   # Project documentation
├── 📄 PROJECT_STRUCTURE.md        # This file
│
├── 📁 src/                        # Core application modules
│   ├── 📄 agent.py               # AI agent (CV selection, cover letter generation)
│   ├── 📄 email_finder.py        # Email finding (Hunter.io + web scraping)
│   ├── 📄 job_search.py          # Multi-platform job search
│   ├── 📄 generate_pdf.py        # PDF generation (ReportLab)
│   └── 📄 gmail_sender.py        # Gmail SMTP email sending
│
├── 📁 templates/                  # HTML templates
│   └── 📄 index.html             # Main web interface
│
├── 📁 static/                     # Static assets
│   ├── 📁 css/
│   │   └── 📄 style.css          # Luxury UI styling
│   └── 📁 js/
│       └── 📄 app.js              # Frontend JavaScript
│
├── 📁 cv_versions/                # CV PDF files
│   ├── 📄 CV_Data_Analyst.pdf
│   ├── 📄 CV_Data_Engineer.pdf
│   └── 📄 CV_Product_Support.pdf
│
├── 📁 applications/               # Generated applications (gitignored)
│   └── [Company_Name]/
│       ├── CV_[Role].pdf
│       ├── CoverLetter_[Role].pdf
│       └── email_draft.txt
│
└── 📁 docs/                       # Documentation
    └── 📄 DEPLOYMENT.md           # Deployment guide
```

## 📝 File Descriptions

### Root Files

- **app.py** - Main Flask application with API endpoints
- **requirements.txt** - All Python package dependencies
- **Procfile** - Tells hosting platforms how to run the app
- **render.yaml** - Configuration for Render.com deployment
- **.gitignore** - Prevents sensitive files from being committed
- **.env** - Environment variables (API keys, credentials)
- **README.md** - Complete project documentation

### src/ - Core Modules

- **agent.py** - AI-powered agent using Groq API
  - Selects best CV based on job description
  - Generates customized cover letters
  - Parses AI responses

- **email_finder.py** - Email discovery system
  - Hunter.io API integration
  - Web scraping fallback
  - AI-powered email selection

- **job_search.py** - Multi-platform job search
  - LinkedIn, Indeed, Glassdoor, Monster, Google Jobs
  - Unified job data format
  - Duplicate removal

- **generate_pdf.py** - PDF generation
  - Creates professional cover letter PDFs
  - Custom styling with green header/footer
  - Uses ReportLab library

- **gmail_sender.py** - Email automation
  - Gmail SMTP integration
  - Attachment handling (CV + Cover Letter)
  - Error handling and logging

### templates/ - HTML Templates

- **index.html** - Main web interface
  - Job search form
  - Job listings display
  - Email modal for manual entry
  - Application status tracking

### static/ - Frontend Assets

- **css/style.css** - Luxury UI styling
  - Sunlight yellow, brown leather, green theme
  - Responsive design
  - Professional animations

- **js/app.js** - Frontend logic
  - Job search functionality
  - Manual email vs system search
  - Application creation workflow
  - Email sending

### cv_versions/ - CV Files

Contains multiple CV versions optimized for different roles:
- Data Analyst
- Data Engineer
- Product Support

### applications/ - Generated Applications

Auto-generated folder structure:
```
applications/
└── Company_Name/
    ├── CV_Role_Name.pdf
    ├── CoverLetter_Role_Name.pdf
    └── email_draft.txt
```

### docs/ - Documentation

- **DEPLOYMENT.md** - Complete deployment guide
  - Render.com instructions
  - Railway.app instructions
  - PythonAnywhere instructions
  - Environment variable setup

## 🔄 Data Flow

1. **User searches for jobs** → `job_search.py` → Returns job listings
2. **User clicks apply** → Choice: Manual email or System search
3. **Email finding** → `email_finder.py` → Hunter.io or manual entry
4. **CV selection** → `agent.py` → AI selects best CV
5. **Cover letter generation** → `agent.py` → AI generates content
6. **PDF creation** → `generate_pdf.py` → Creates cover letter PDF
7. **Email sending** → `gmail_sender.py` → Sends via Gmail SMTP

## 🚀 Deployment Files

- **Procfile** - For Heroku, Render, Railway
- **render.yaml** - Specific to Render.com
- **requirements.txt** - For all platforms
- **.gitignore** - Prevents sensitive data upload

## 🔐 Environment Variables

Required in `.env` file:
```
GROQ_API_KEY=your_groq_api_key
GMAIL_USER=your.email@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
HUNTER_API_KEY=your_hunter_api_key
```

## 📦 Dependencies

See `requirements.txt` for complete list:
- Flask - Web framework
- Groq - AI API
- ReportLab - PDF generation
- BeautifulSoup4 - Web scraping
- Requests - HTTP requests
- python-dotenv - Environment variables

---

**Clean, organized, and ready for deployment! 🎉**