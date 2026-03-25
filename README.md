# 🚀 AI-Powered Job Application Agent

An intelligent web application that automates job searching, CV selection, cover letter generation, and email sending using AI.

## ✨ Features

- 🔍 **Multi-Platform Job Search** - Searches across LinkedIn, Indeed, Glassdoor, Monster, and Google Jobs
- 🤖 **AI-Powered CV Selection** - Automatically selects the best CV version for each job
- ✍️ **Custom Cover Letter Generation** - Creates tailored cover letters using AI (Groq)
- 📧 **Email Finder** - Uses Hunter.io API to find company emails
- 📤 **Automated Email Sending** - Sends applications via Gmail with attachments
- 🎨 **Luxury UI** - Beautiful interface with sunlight, leather brown, and green tones
- 📱 **Responsive Design** - Works on desktop and mobile

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI**: Groq API (Llama 3.3 70B)
- **Email**: Gmail SMTP
- **Email Finder**: Hunter.io API
- **PDF Generation**: ReportLab

## 📁 Project Structure

```
job-agent/
├── app.py                  # Main Flask application
├── src/                    # Core modules
│   ├── agent.py           # AI agent for CV selection & cover letter
│   ├── email_finder.py    # Email finding with Hunter.io
│   ├── job_search.py      # Multi-platform job search
│   ├── generate_pdf.py    # PDF generation for cover letters
│   └── gmail_sender.py    # Gmail email sending
├── templates/             # HTML templates
│   └── index.html
├── static/                # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── cv_versions/           # CV PDF files
├── applications/          # Generated applications (gitignored)
├── docs/                  # Documentation
│   └── DEPLOYMENT.md
├── .env                   # Environment variables (gitignored)
├── requirements.txt       # Python dependencies
├── Procfile              # For deployment
├── render.yaml           # Render.com config
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Gmail account with App Password
- Groq API key (free at https://console.groq.com)
- Hunter.io API key (optional, for email finding)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/job-application-agent.git
   cd job-application-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key
   GMAIL_USER=your.email@gmail.com
   GMAIL_APP_PASSWORD=your_gmail_app_password
   HUNTER_API_KEY=your_hunter_api_key
   ```

4. **Add your CV files**
   
   Place your CV PDF files in `cv_versions/` folder:
   - `CV_Data_Analyst.pdf`
   - `CV_Data_Engineer.pdf`
   - `CV_Product_Support.pdf`

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   
   Navigate to `http://localhost:5000`

## 📖 Usage

1. **Search for Jobs**
   - Enter job keywords (e.g., "software engineer")
   - Select location and job type
   - Click "Search Jobs"

2. **Apply to Jobs**
   - Choose between:
     - **Apply with Manual Email** - Enter email manually
     - **Apply with System Search** - Use Hunter.io to find email
   
3. **Review & Send**
   - System generates CV and cover letter
   - Review the application
   - Click "Send Email Now"

4. **Track Applications**
   - View total applications in the dashboard
   - Check `applications/` folder for saved documents

## 🌐 Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions.

**Quick Deploy Options:**
- **Render.com** (Recommended) - Free tier, auto-deploy from GitHub
- **Railway.app** - $5 free credit/month
- **PythonAnywhere** - Always-on free tier

## 🔑 API Keys Setup

### Groq API (Required)
1. Go to https://console.groq.com
2. Sign up for free account
3. Create API key
4. Add to `.env` file

### Gmail App Password (Required)
1. Enable 2-Factor Authentication on Gmail
2. Go to Google Account → Security → App Passwords
3. Generate app password
4. Add to `.env` file

### Hunter.io API (Optional)
1. Go to https://hunter.io
2. Sign up for free account (50 searches/month)
3. Get API key from dashboard
4. Add to `.env` file

## 🎨 UI Theme

The application features a luxury design with:
- **Sunlight Yellow/Gold** - Highlights and accents
- **Brown Leather** - Headers and buttons
- **Green Tones** - Success states and actions
- **Cream/Beige** - Backgrounds

## 📝 License

MIT License - Feel free to use and modify

## 👤 Author

**Ramesh Kadariya**
- Email: hello.contactramesh@gmail.com
- Website: https://www.rameshkadariya.com.np
- GitHub: https://github.com/rameshkadariya
- LinkedIn: https://www.linkedin.com/in/ramesh-kadariya-638979280

## 🙏 Acknowledgments

- Groq for AI API
- Hunter.io for email finding
- Flask community
- ReportLab for PDF generation

---

Made with ❤️ by Ramesh Kadariya