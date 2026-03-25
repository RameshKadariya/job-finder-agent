import requests
from bs4 import BeautifulSoup
import time
import re
import json

def extract_emails_from_job_post(job_description, job_html=""):
    """
    Extract emails directly from job posting text and HTML
    This is the BEST source - emails in job posts are meant for applications!
    """
    emails = set()
    
    # Email regex pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Extract from description text
    if job_description:
        found = re.findall(email_pattern, job_description)
        emails.update(found)
    
    # Extract from HTML
    if job_html:
        # Parse HTML
        soup = BeautifulSoup(job_html, 'html.parser')
        
        # Method 1: mailto links
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            if href.startswith('mailto:'):
                email = href.replace('mailto:', '').split('?')[0].strip()
                emails.add(email)
        
        # Method 2: Extract from all text
        text = soup.get_text()
        found = re.findall(email_pattern, text)
        emails.update(found)
        
        # Method 3: Check image alt text (some posts put emails in images)
        for img in soup.find_all('img', alt=True):
            alt_text = img.get('alt', '')
            found = re.findall(email_pattern, alt_text)
            emails.update(found)
    
    # Filter out ONLY obvious fakes (FIXED: Allow Gmail/Yahoo for startups)
    valid_emails = []
    for email in emails:
        email = email.strip().lower()
        
        # Skip ONLY obvious fakes
        if any(x in email for x in [
            'example.com', 'test.com', 'sample.com',
            'noreply@', 'donotreply@', 'no-reply@',
            'placeholder', 'yourcompany'
        ]):
            continue
        
        if '@' in email and '.' in email.split('@')[1]:
            valid_emails.append(email)
    
    return valid_emails


def search_jobs_google(keywords, location="", job_type=""):
    """
    Search for jobs using Google search - ENHANCED with email extraction
    """
    jobs = []
    
    # Build search query
    query = f"{keywords} jobs {location} {job_type}".strip()
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&ibp=htl;jobs"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract job listings (simplified - Google's structure changes often)
        job_cards = soup.find_all('div', class_='PwjeAc')
        
        for card in job_cards[:15]:  # Increased to 15 jobs
            try:
                title = card.find('div', class_='BjJfJf').text if card.find('div', class_='BjJfJf') else "N/A"
                company = card.find('div', class_='vNEEBe').text if card.find('div', class_='vNEEBe') else "N/A"
                
                # Extract emails from job card
                job_html = str(card)
                description = card.get_text()
                emails_in_post = extract_emails_from_job_post(description, job_html)
                
                jobs.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'description': description,
                    'source': 'Google Jobs',
                    'emails_in_post': emails_in_post  # NEW: Emails found in job post
                })
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"⚠️  Google Jobs: {e}")
    
    return jobs


def search_jobs_indeed(keywords, location=""):
    """
    Search for jobs on Indeed - ENHANCED with email extraction
    """
    jobs = []
    
    query = keywords.replace(' ', '+')
    loc = location.replace(' ', '+')
    url = f"https://www.indeed.com/jobs?q={query}&l={loc}&sort=date"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find job cards
        job_cards = soup.find_all('div', class_='job_seen_beacon')
        
        for card in job_cards[:15]:
            try:
                title_elem = card.find('h2', class_='jobTitle')
                title = title_elem.text.strip() if title_elem else "N/A"
                
                company_elem = card.find('span', class_='companyName')
                company = company_elem.text.strip() if company_elem else "N/A"
                
                location_elem = card.find('div', class_='companyLocation')
                job_location = location_elem.text.strip() if location_elem else location
                
                snippet_elem = card.find('div', class_='job-snippet')
                description = snippet_elem.text.strip() if snippet_elem else keywords
                
                # Extract emails from job description
                job_html = str(card)
                emails_in_post = extract_emails_from_job_post(description, job_html)
                
                jobs.append({
                    'title': title,
                    'company': company,
                    'location': job_location,
                    'description': description,
                    'source': 'Indeed',
                    'emails_in_post': emails_in_post  # NEW: Emails found in job post
                })
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"⚠️  Indeed: {e}")
    
    return jobs


def search_jobs_linkedin(keywords, location=""):
    """
    Search for jobs on LinkedIn - ENHANCED with email extraction
    """
    jobs = []
    
    query = keywords.replace(' ', '%20')
    loc = location.replace(' ', '%20')
    url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location={loc}&f_TPR=r86400"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find job cards (LinkedIn structure)
        job_cards = soup.find_all('div', class_='base-card')
        
        for card in job_cards[:15]:
            try:
                title_elem = card.find('h3', class_='base-search-card__title')
                title = title_elem.text.strip() if title_elem else "N/A"
                
                company_elem = card.find('h4', class_='base-search-card__subtitle')
                company = company_elem.text.strip() if company_elem else "N/A"
                
                location_elem = card.find('span', class_='job-search-card__location')
                job_location = location_elem.text.strip() if location_elem else location
                
                # Extract emails from job card
                job_html = str(card)
                description = card.get_text()
                emails_in_post = extract_emails_from_job_post(description, job_html)
                
                jobs.append({
                    'title': title,
                    'company': company,
                    'location': job_location,
                    'description': description,
                    'source': 'LinkedIn',
                    'emails_in_post': emails_in_post  # NEW: Emails found in job post
                })
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"⚠️  LinkedIn: {e}")
    
    return jobs


def search_jobs_glassdoor(keywords, location=""):
    """
    Search Glassdoor - ENHANCED with email extraction
    """
    jobs = []
    
    query = keywords.replace(' ', '-')
    loc = location.replace(' ', '-')
    url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={query}&locT=C&locId={loc}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        job_cards = soup.find_all('li', class_='react-job-listing')
        
        for card in job_cards[:10]:
            try:
                title = card.get('data-job-title', 'N/A')
                company = card.get('data-employer-name', 'N/A')
                
                # Extract emails from job card
                job_html = str(card)
                description = card.get_text()
                emails_in_post = extract_emails_from_job_post(description, job_html)
                
                jobs.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'description': description,
                    'source': 'Glassdoor',
                    'emails_in_post': emails_in_post  # NEW: Emails found in job post
                })
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"⚠️  Glassdoor: {e}")
    
    return jobs


def search_jobs_monster(keywords, location=""):
    """
    Search Monster - ENHANCED with email extraction
    """
    jobs = []
    
    query = keywords.replace(' ', '+')
    url = f"https://www.monster.com/jobs/search?q={query}&where={location}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        job_cards = soup.find_all('div', class_='job-cardstyle__JobCardComponent')
        
        for card in job_cards[:10]:
            try:
                title_elem = card.find('h2')
                title = title_elem.text.strip() if title_elem else "N/A"
                
                company_elem = card.find('div', class_='company')
                company = company_elem.text.strip() if company_elem else "N/A"
                
                # Extract emails from job card
                job_html = str(card)
                description = card.get_text()
                emails_in_post = extract_emails_from_job_post(description, job_html)
                
                jobs.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'description': description,
                    'source': 'Monster',
                    'emails_in_post': emails_in_post  # NEW: Emails found in job post
                })
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"⚠️  Monster: {e}")
    
    return jobs


def search_all_jobs(keywords, location="Remote", job_type=""):
    """
    Search across ALL job boards - ENHANCED
    """
    print(f"\n🔍 BROAD SEARCH: {keywords} | Location: {location} | Type: {job_type}\n")
    
    all_jobs = []
    
    # Search Google Jobs
    print("🌐 Searching Google Jobs...")
    google_jobs = search_jobs_google(keywords, location, job_type)
    all_jobs.extend(google_jobs)
    print(f"   Found: {len(google_jobs)} jobs")
    time.sleep(1)
    
    # Search Indeed
    print("🔵 Searching Indeed...")
    indeed_jobs = search_jobs_indeed(keywords, location)
    all_jobs.extend(indeed_jobs)
    print(f"   Found: {len(indeed_jobs)} jobs")
    time.sleep(1)
    
    # Search LinkedIn
    print("💼 Searching LinkedIn...")
    linkedin_jobs = search_jobs_linkedin(keywords, location)
    all_jobs.extend(linkedin_jobs)
    print(f"   Found: {len(linkedin_jobs)} jobs")
    time.sleep(1)
    
    # Search Glassdoor
    print("🏢 Searching Glassdoor...")
    glassdoor_jobs = search_jobs_glassdoor(keywords, location)
    all_jobs.extend(glassdoor_jobs)
    print(f"   Found: {len(glassdoor_jobs)} jobs")
    time.sleep(1)
    
    # Search Monster
    print("👹 Searching Monster...")
    monster_jobs = search_jobs_monster(keywords, location)
    all_jobs.extend(monster_jobs)
    print(f"   Found: {len(monster_jobs)} jobs")
    
    # Remove duplicates
    unique_jobs = []
    seen = set()
    for job in all_jobs:
        key = (job['title'].lower(), job['company'].lower())
        if key not in seen and job['company'] != "N/A":
            seen.add(key)
            unique_jobs.append(job)
    
    print(f"\n✅ TOTAL: {len(unique_jobs)} unique jobs from {len(all_jobs)} results\n")
    
    # Show email extraction summary
    jobs_with_emails = sum(1 for j in unique_jobs if j.get('emails_in_post'))
    if jobs_with_emails > 0:
        print(f"📧 {jobs_with_emails} jobs have emails in their posts!")
        print(f"   (These will be used directly - no scraping needed)\n")
    
    return unique_jobs


if __name__ == "__main__":
    # Test the job search
    keywords = input("Enter job keywords (e.g., 'Data Analyst'): ")
    location = input("Enter location (e.g., 'Remote', 'Nepal'): ")
    
    jobs = search_all_jobs(keywords, location)
    
    for i, job in enumerate(jobs, 1):
        print(f"{i}. {job['title']} at {job['company']} ({job['location']}) - {job['source']}")
