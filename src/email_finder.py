from groq import Groq
from dotenv import load_dotenv
import os
import re
import json
import requests
from bs4 import BeautifulSoup
import time

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")


def find_company_email(company_name, company_url=None, apply_email=None):
    """
    Find REAL company emails using Hunter.io API + web search + scraping
    
    Args:
        company_name: Name of the company
        company_url: Direct URL to company website (if available from job data)
        apply_email: Direct apply email (if available from job data like RemoteOK)
    """
    print(f"   🔍 Searching for {company_name} emails...")
    
    # Check if apply_email is directly provided (RemoteOK, etc.)
    if apply_email and '@' in apply_email:
        valid = filter_valid_emails([apply_email], skip_strict_filter=True)
        if valid:
            print(f"   ✅ Found {len(valid)} email(s) from job data")
            for email in valid:
                print(f"      ✓ {email}")
            return valid
    
    # Step 1: Try Hunter.io API first (most reliable)
    if HUNTER_API_KEY:
        hunter_emails = search_hunter_io(company_name, company_url)
        if hunter_emails:
            # Use Groq to pick best email if multiple found
            if len(hunter_emails) > 1:
                best = pick_best_email(hunter_emails, company_name)
                if best:
                    print(f"   🤖 AI selected best from Hunter.io: {best}")
                    return [best]
            
            print(f"   ✅ Found {len(hunter_emails)} email(s) via Hunter.io")
            for email in hunter_emails:
                print(f"      ✓ {email}")
            return hunter_emails
    
    # Step 2: Use company_url directly if provided
    if company_url:
        print(f"   🌐 Using company URL: {company_url}")
        emails = scrape_company_url(company_url)
        if emails:
            # Use Groq to pick best email if multiple found
            if len(emails) > 1:
                best = pick_best_email(emails, company_name)
                if best:
                    print(f"   🤖 AI selected best: {best}")
                    return [best]
            
            print(f"   ✅ Found {len(emails)} email(s)")
            for email in emails:
                print(f"      ✓ {email}")
            return emails
    
    # Step 3: Search for company website and scrape
    emails = search_and_scrape(company_name)
    
    if emails:
        # Use Groq to pick best email if multiple found
        if len(emails) > 1:
            best = pick_best_email(emails, company_name)
            if best:
                print(f"   🤖 AI selected best: {best}")
                return [best]
        
        print(f"   ✅ Found {len(emails)} email(s)")
        for email in emails:
            print(f"      ✓ {email}")
        return emails
    
    print(f"   ❌ No emails found")
    return []


def search_hunter_io(company_name, company_url=None):
    """
    Search for company emails using Hunter.io API
    """
    if not HUNTER_API_KEY:
        return []
    
    try:
        # Try domain search if we have a URL
        if company_url:
            # Extract domain from URL
            domain = extract_domain_from_url(company_url)
            if domain:
                # Hunter.io Domain Search API
                url = f"https://api.hunter.io/v2/domain-search"
                params = {
                    "domain": domain,
                    "api_key": HUNTER_API_KEY,
                    "limit": 10
                }
                
                response = requests.get(url, params=params, timeout=10)
                time.sleep(1)  # Rate limiting
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("data") and data["data"].get("emails"):
                        emails = [email["value"] for email in data["data"]["emails"]]
                        return filter_valid_emails(emails)
        
        # Try company name search
        url = f"https://api.hunter.io/v2/companies/find"
        params = {
            "domain": f"{company_name.lower().replace(' ', '')}.com",  # Guess domain
            "api_key": HUNTER_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        time.sleep(1)  # Rate limiting
        
        if response.status_code == 200:
            data = response.json()
            if data.get("data") and data["data"].get("emails"):
                emails = [email["value"] for email in data["data"]["emails"]]
                return filter_valid_emails(emails)
    
    except Exception as e:
        print(f"   ⚠️ Hunter.io API error: {e}")
    
    return []


def extract_domain_from_url(url):
    """
    Extract domain from URL
    """
    try:
        # Remove protocol
        if "://" in url:
            url = url.split("://")[1]
        
        # Remove path and query
        domain = url.split("/")[0]
        
        # Remove www prefix
        if domain.startswith("www."):
            domain = domain[4:]
        
        return domain
    except:
        return None


def pick_best_email(emails, company_name):
    """
    Use Groq AI to pick the best email from multiple options
    """
    try:
        prompt = f"""Company: {company_name}
Emails found: {', '.join(emails)}

Pick the single best email for sending a job application.
Prefer: hr@, hrd@, careers@, jobs@, hiring@, recruitment@, info@, contact@

Return ONLY the email address, nothing else."""
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0
        )
        
        best_email = response.choices[0].message.content.strip()
        
        # Validate it's actually one of the emails
        if best_email in emails:
            return best_email
        
        # If AI returned something weird, just return first email
        return emails[0]
        
    except Exception as e:
        print(f"   ⚠️ AI selection failed: {e}")
        return emails[0]


def scrape_company_url(company_url):
    """
    Scrape company URL directly (when provided from job data)
    """
    all_emails = set()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # Scrape main URL
    emails = scrape_url_for_emails(company_url, headers)
    all_emails.update(emails)
    time.sleep(1)  # Rate limiting
    
    # Also check subpages
    for page in ['/contact', '/careers', '/about', '/team', '/contact-us', '/career']:
        try:
            sub_url = company_url.rstrip('/') + page
            sub_emails = scrape_url_for_emails(sub_url, headers)
            all_emails.update(sub_emails)
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"   ⚠️ Failed {page}: {e}")
            continue
    
    return filter_valid_emails(list(all_emails))


def search_and_scrape(company_name):
    """
    Search for company and scrape their website for emails
    """
    all_emails = set()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # Search queries
    search_queries = [
        f"{company_name} contact email",
        f"{company_name} hr email career",
        f"{company_name} recruitment email"
    ]
    
    for query in search_queries[:2]:  # Try first 2
        try:
            # Use DuckDuckGo HTML (no API needed)
            search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
            response = requests.get(search_url, headers=headers, timeout=10)
            time.sleep(1)  # Rate limiting
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Fixed DuckDuckGo URL extraction
                urls_to_check = []
                for link in soup.select('a.result__a'):
                    href = link.get('href', '')
                    if href.startswith('http') and 'duckduckgo' not in href:
                        urls_to_check.append(href)
                
                # Also check result snippets for emails
                for result in soup.find_all('a', class_='result__snippet'):
                    snippet_text = result.get_text()
                    found = extract_emails_from_text(snippet_text)
                    all_emails.update(found)
                
                # Visit top URLs
                for url in urls_to_check[:3]:
                    try:
                        page_emails = scrape_url_for_emails(url, headers)
                        all_emails.update(page_emails)
                        time.sleep(1)  # Rate limiting
                    except Exception as e:
                        print(f"   ⚠️ Failed {url}: {e}")
                        continue
        except Exception as e:
            print(f"   ⚠️ Search failed for '{query}': {e}")
            continue
    
    # If still no emails, try direct company website
    if not all_emails:
        print(f"   ⚠️ No emails found via search, trying direct website access...")
    
    return filter_valid_emails(list(all_emails))


def scrape_url_for_emails(url, headers):
    """
    Scrape a URL for email addresses
    """
    emails = set()
    
    try:
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Method 1: mailto links
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                if href.startswith('mailto:'):
                    email = href.replace('mailto:', '').split('?')[0].strip()
                    emails.add(email)
            
            # Method 2: Extract from page text
            page_text = soup.get_text()
            found = extract_emails_from_text(page_text)
            emails.update(found)
    except Exception as e:
        # Log errors instead of silent failure
        if '404' not in str(e) and 'timeout' not in str(e).lower():
            print(f"   ⚠️ Scrape error for {url}: {e}")
    
    return emails


def extract_emails_from_text(text):
    """
    Extract email addresses from text using regex
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return set(re.findall(email_pattern, text))


def filter_valid_emails(emails, skip_strict_filter=False):
    """
    Filter out fake/invalid emails
    
    Args:
        skip_strict_filter: If True, only check format (for apply_emails from job data)
    """
    valid = []
    seen = set()
    
    for email in emails:
        email = email.strip().lower()
        
        # Skip invalid formats
        if '@' not in email or '.' not in email.split('@')[1]:
            continue
        
        # If skip_strict_filter (for apply_emails), only check obvious fakes
        if skip_strict_filter:
            if any(x in email for x in [
                'example.com', 'sample.com', 'placeholder',
                'noreply@', 'donotreply@', 'no-reply@'
            ]):
                continue
        else:
            # Skip ONLY obvious fake emails (Allow Gmail/Yahoo for startups)
            if any(x in email for x in [
                'example.com', 'test.com', 'sample.com', 'domain.com',
                'noreply@', 'donotreply@', 'no-reply@',
                'placeholder', 'yourcompany', 'company.com', 'yourdomain',
                '@sentry.', 'wixpress.com', 'gravatar.com'
            ]):
                continue
        
        # Must be unique
        if email not in seen:
            seen.add(email)
            valid.append(email)
    
    return valid[:5]  # Return max 5 emails


if __name__ == "__main__":
    company = input("Enter company name: ")
    company_url = input("Enter company URL (optional, press Enter to skip): ").strip()
    
    if not company_url:
        company_url = None
    
    emails = find_company_email(company, company_url=company_url)
    
    if emails:
        print(f"\n✅ Found {len(emails)} REAL email(s):")
        for email in emails:
            print(f"  - {email}")
    else:
        print(f"\n❌ No emails found")
        print("   The company may not have publicly listed emails.")