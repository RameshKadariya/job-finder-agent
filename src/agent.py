from groq import Groq
from dotenv import load_dotenv
from generate_pdf import generate_cover_letter
import os
import json
import shutil

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Available CV versions
CV_VERSIONS = {
    "data_analyst": "cv_versions/CV_Data_Analyst.pdf",
    "data_engineer": "cv_versions/CV_Data_Engineer.pdf",
    "product_support": "cv_versions/CV_Product_Support.pdf"
}

def select_best_cv(job_description, company_name, role_name):
    """Use AI to select the most appropriate CV based on job requirements"""
    prompt = f"""
Analyze this job and select the best CV:

Company: {company_name}
Role: {role_name}
Description: {job_description}

Available CVs:
1. data_analyst - For Data Analyst, Business Analyst, SQL roles
2. data_engineer - For Data Engineer, ETL, Database roles
3. product_support - For Support, Technical Support roles

Return ONLY valid JSON (no markdown, no explanations):
{{
  "selected_cv": "data_analyst",
  "reason": "Best match for this role"
}}
"""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"⚠️ AI API Error: {e}")
        return '{"selected_cv": "data_analyst", "reason": "Default selection"}'

def generate_cover_letter_content(job_description, company_name, role_name):
    """Generate truly customized cover letter based on actual job requirements"""
    prompt = f"""
You are writing a FORMAL, PROFESSIONAL job application for Ramesh Kadariya.

CANDIDATE PROFILE:
- Name: Ramesh Kadariya
- Education: BSc (Hons) Computer System Engineering
- Skills: Data Analysis, SQL, Python, Database Management, Problem-solving
- Email: hello.contactramesh@gmail.com
- Phone: +977 9847249971

JOB DETAILS:
Company: {company_name}
Position: {role_name}
Job Description: {job_description}

TASK:
1. Write a FORMAL, PROFESSIONAL cover letter (2-3 paragraphs) that:
   - Is SPECIFIC to this company and role
   - References specific requirements from the job description
   - Highlights relevant skills and experience
   - Shows genuine interest in THIS company and role
   - Uses formal business language

2. Write a COMPLETE FORMAL EMAIL BODY with proper structure:
   - GREETING: "Dear Hiring Manager," or appropriate formal greeting
   - BODY: 2-3 sentences mentioning the attached CV and cover letter, expressing interest
   - CLOSING: "Sincerely," or appropriate formal closing
   - SIGNATURE: "Ramesh Kadariya"

Return ONLY valid JSON (no markdown):
{{
  "email_subject": "Application for {role_name} Position - Ramesh Kadariya",
  "email_body": "COMPLETE EMAIL WITH GREETING, BODY, AND CLOSING:\\n\\nDear Hiring Manager,\\n\\n[2-3 sentences about the application, mentioning attached CV and cover letter, expressing interest in the specific role at {company_name}]\\n\\nSincerely,\\nRamesh Kadariya",
  "cover_letter_content": "Write 2-3 FORMAL, PROFESSIONAL paragraphs that are SPECIFIC to this job and company. Mention actual requirements from the job description. Use formal business language."
}}

CRITICAL REQUIREMENTS:
- Email body MUST have: GREETING + BODY + CLOSING + SIGNATURE
- Use FORMAL, PROFESSIONAL business language
- NO casual language or slang
- Reference ACTUAL details from the job description
- Make it sound like a professional business communication
- Tailor content to this specific company and role
- Return ONLY the JSON object
"""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a professional career advisor who writes formal, professional job application materials. You always use formal business language, avoid casual expressions, and tailor content to specific job descriptions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1200
        )
    except Exception as e:
        print(f"⚠️ AI API Error: {e}")
        return f'''{{
  "email_subject": "Application for {role_name} Position - Ramesh Kadariya",
  "email_body": "Dear Hiring Manager,\\n\\nI am writing to formally express my interest in the {role_name} position at {company_name}. Please find attached my curriculum vitae and cover letter for your consideration.\\n\\nI would welcome the opportunity to discuss how my qualifications align with your team's requirements.\\n\\nSincerely,\\nRamesh Kadariya",
  "cover_letter_content": "I am writing to formally apply for the {role_name} position at {company_name}. With my academic background in Computer Systems Engineering and practical experience in data analysis, SQL, Python, and database management, I am confident in my ability to make meaningful contributions to your organization.\\n\\nMy academic projects and professional experience have provided me with strong analytical and problem-solving capabilities. This opportunity is particularly appealing as it aligns with both my technical expertise and professional aspirations.\\n\\nI am enthusiastic about the prospect of contributing to {company_name}'s continued success and would appreciate the opportunity to discuss how my qualifications correspond with your requirements. Thank you for your time and consideration."
}}'''ver_letter_content": "I am writing to formally apply for the {role_name} position at {company_name}. With my academic background in Computer Systems Engineering and practical experience in data analysis, SQL, Python, and database management, I am confident in my ability to make meaningful contributions to your organization.\\n\\nMy academic projects and professional experience have provided me with strong analytical and problem-solving capabilities. This opportunity is particularly appealing as it aligns with both my technical expertise and professional aspirations.\\n\\nI am enthusiastic about the prospect of contributing to {company_name}'s continued success and would appreciate the opportunity to discuss how my qualifications correspond with your requirements. Thank you for your time and consideration."
}}'''

def parse_json(raw):
    """Parse JSON from AI response, handling markdown code blocks and cleaning"""
    raw = raw.strip()
    
    # Remove markdown code blocks
    if raw.startswith("```"):
        lines = raw.split("\n")
        # Remove first line (```json or ```)
        lines = lines[1:]
        # Remove last line if it's ```
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines)
    
    # Try to find JSON object in the text
    import re
    json_match = re.search(r'\{.*\}', raw, re.DOTALL)
    if json_match:
        raw = json_match.group(0)
    
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON Parse Error: {e}")
        print(f"Raw response (first 500 chars):\n{raw[:500]}")
        raise


def run_agent():
    print("=" * 45)
    print("   JOB APPLICATION AGENT 🤖")
    print("=" * 45 + "\n")

    company = input("Company name: ").strip()
    role    = input("Role/Position: ").strip()
    print("Paste job description (press Enter twice when done):\n")

    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    job = "\n".join(lines)

    print("\n⏳ Step 1: Selecting best CV...\n")
    
    # Select best CV
    cv_raw = select_best_cv(job, company, role)
    try:
        cv_data = parse_json(cv_raw)
        selected_cv_key = cv_data['selected_cv']
        cv_reason = cv_data['reason']
        
        if selected_cv_key not in CV_VERSIONS:
            print(f"⚠️ Invalid CV selection: {selected_cv_key}, defaulting to data_analyst")
            selected_cv_key = "data_analyst"
        
        cv_path = CV_VERSIONS[selected_cv_key]
        print(f"✅ Selected: {selected_cv_key.replace('_', ' ').title()}")
        print(f"   Reason: {cv_reason}\n")
        
    except Exception as e:
        print(f"⚠️ CV selection error: {e}, using data_analyst as default")
        cv_path = CV_VERSIONS["data_analyst"]

    print("⏳ Step 2: Generating cover letter...\n")
    
    # Generate cover letter
    cl_raw = generate_cover_letter_content(job, company, role)
    try:
        cl_data = parse_json(cl_raw)
    except Exception as e:
        print(f"⚠️ Cover letter generation error: {e}\nRaw:\n{cl_raw}")
        return

    print(f"✅ Cover letter generated\n")

    # Create output folder
    safe_company = company.replace(" ", "_").replace("/", "_")
    safe_role    = role.replace(" ", "_").replace("/", "_")
    folder = f"applications/{safe_company}"
    os.makedirs(folder, exist_ok=True)

    # Copy selected CV
    cv_output = f"{folder}/CV_{safe_role}.pdf"
    shutil.copy2(cv_path, cv_output)
    print(f"✅ CV copied: {cv_output}")

    # Generate cover letter PDF
    generate_cover_letter(
        output_path=f"{folder}/CoverLetter_{safe_role}.pdf",
        company=company,
        role=role,
        email_body=cl_data["cover_letter_content"]
    )

    # Save email draft
    with open(f"{folder}/email_draft.txt", "w", encoding="utf-8") as f:
        f.write(f"To: [HR Email]\nSubject: {cl_data['email_subject']}\n\n{cl_data['email_body']}")

    print(f"\n📁 Saved in: {folder}/")
    print(f"   CV_{safe_role}.pdf")
    print(f"   CoverLetter_{safe_role}.pdf")
    print(f"   email_draft.txt\n")

if __name__ == "__main__":
    run_agent()