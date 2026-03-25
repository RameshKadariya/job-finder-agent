# 📤 GitHub Push Guide

## Step-by-Step Instructions

### 1. Initialize Git Repository
```bash
git init
```

### 2. Add All Files
```bash
git add .
```

### 3. Check What Will Be Committed (Verify .env is NOT included)
```bash
git status
```

**⚠️ IMPORTANT:** Make sure you see:
- ✅ `.env.example` (should be included)
- ❌ `.env` (should NOT be included - it should say "Untracked files" or not appear)

If `.env` appears in the list to be committed, STOP and run:
```bash
git rm --cached .env
```

### 4. Commit Your Changes
```bash
git commit -m "Initial commit: Job Application Agent"
```

### 5. Add Remote Repository
```bash
git remote add origin https://github.com/RameshKadariya/job-finder-agent.git
```

### 6. Rename Branch to Main
```bash
git branch -M main
```

### 7. Push to GitHub
```bash
git push -u origin main
```

---

## ✅ Verification Checklist

After pushing, check on GitHub:
- ✅ All code files are there
- ✅ `.env.example` is there
- ❌ `.env` is NOT there (should be missing)
- ✅ `cv_versions/` folder with CV files is there
- ✅ `README.md` is visible
- ❌ `applications/` folder is NOT there (gitignored)

---

## 🔐 Environment Variables for Deployment

When deploying to Render.com, you'll need to add these environment variables manually in the Render dashboard:

1. `GROQ_API_KEY` = (your actual Groq API key)
2. `GMAIL_USER` = hello.contactramesh@gmail.com
3. `GMAIL_APP_PASSWORD` = (your actual Gmail app password)
4. `HUNTER_API_KEY` = (your actual Hunter.io API key)

**DO NOT** put these in GitHub! They stay in:
- Local: `.env` file (gitignored)
- Render: Environment variables in dashboard

---

## 🚨 Security Notes

### What to NEVER push to GitHub:
- ❌ `.env` file
- ❌ API keys
- ❌ Passwords
- ❌ Email credentials
- ❌ Any sensitive data

### What IS safe to push:
- ✅ `.env.example` (template with no real values)
- ✅ All code files
- ✅ CV files (they're your public resume)
- ✅ Documentation
- ✅ Configuration files (without secrets)

---

## 📝 Quick Command Summary

```bash
# One-time setup
git init
git add .
git commit -m "Initial commit: Job Application Agent"
git branch -M main
git remote add origin https://github.com/RameshKadariya/job-finder-agent.git
git push -u origin main

# Future updates
git add .
git commit -m "Your commit message"
git push
```

---

## 🎉 After Successful Push

1. Go to: https://github.com/RameshKadariya/job-finder-agent
2. Verify all files are there
3. Check that `.env` is NOT visible
4. Proceed to deploy on Render.com

---

**Ready to push? Follow the steps above!** 🚀