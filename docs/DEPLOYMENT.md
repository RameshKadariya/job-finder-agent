# 🚀 Deployment Guide - Job Application Agent

## Option 1: Render.com (RECOMMENDED - Easiest & Free)

### Step 1: Prepare Your Code
1. Create a GitHub account if you don't have one: https://github.com
2. Create a new repository (e.g., "job-application-agent")
3. Push your code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/job-application-agent.git
   git push -u origin main
   ```

### Step 2: Deploy on Render
1. Go to https://render.com and sign up (use GitHub to sign in)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: job-application-agent
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free

### Step 3: Add Environment Variables
In Render dashboard, go to "Environment" and add:
- `GROQ_API_KEY` = your_groq_api_key
- `GMAIL_USER` = hello.contactramesh@gmail.com
- `GMAIL_APP_PASSWORD` = your_gmail_app_password
- `HUNTER_API_KEY` = your_hunter_api_key

### Step 4: Deploy
Click "Create Web Service" and wait 5-10 minutes for deployment.

Your app will be live at: `https://job-application-agent.onrender.com`

---

## Option 2: Railway.app (Fast & Easy)

### Step 1: Prepare Code
Same as Render - push to GitHub

### Step 2: Deploy on Railway
1. Go to https://railway.app and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Python and deploys

### Step 3: Add Environment Variables
In Railway dashboard, add the same environment variables as above.

Your app will be live at: `https://your-app.up.railway.app`

---

## Option 3: PythonAnywhere (Always-On Free)

### Step 1: Sign Up
1. Go to https://www.pythonanywhere.com
2. Create a free account

### Step 2: Upload Code
1. Go to "Files" tab
2. Upload your project files
3. Or use Git to clone your repository

### Step 3: Create Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Flask"
4. Set Python version to 3.10
5. Configure WSGI file to point to your app

### Step 4: Set Environment Variables
1. Go to "Files" tab
2. Edit `.env` file with your API keys

Your app will be live at: `https://YOUR_USERNAME.pythonanywhere.com`

---

## 📝 Important Notes:

### Free Tier Limitations:
- **Render**: Sleeps after 15 min inactivity (wakes in ~30 sec)
- **Railway**: $5 credit/month (~500 hours)
- **PythonAnywhere**: Always-on but limited CPU

### Before Deploying:
1. ✅ Make sure `.env` is in `.gitignore` (already done)
2. ✅ Test locally: `python app.py`
3. ✅ Commit all changes to Git
4. ✅ Have your API keys ready

### After Deploying:
1. Test the live URL
2. Check if email sending works
3. Monitor logs for errors

---

## 🔧 Troubleshooting:

### App won't start:
- Check logs in hosting dashboard
- Verify all environment variables are set
- Make sure `requirements.txt` is correct

### Email not sending:
- Verify Gmail credentials in environment variables
- Check if Gmail App Password is correct
- Test locally first

### Hunter.io not working:
- Verify API key is correct
- Check if you have remaining searches

---

## 🎉 Success!

Once deployed, share your app URL with others!

Example: `https://job-application-agent.onrender.com`