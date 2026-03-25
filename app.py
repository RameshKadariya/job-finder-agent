from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from src.job_search import search_all_jobs
from src.email_finder import find_company_email
from src.agent import select_best_cv, generate_cover_letter_content, parse_json, CV_VERSIONS
from src.generate_pdf import generate_cover_letter_pdf
from src.gmail_sender import send_application_email_with_bytes
import os
import shutil
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search-jobs', methods=['POST'])
def search_jobs():
    data = request.json
    keywords = data.get('keywords', '')
    location = data.get('location', 'Remote')
    job_type = data.get('job_type', '')
    
    jobs = search_all_jobs(keywords, location, job_type)
    
    return jsonify({
        'success': True,
        'jobs': jobs[:20]
    })

@app.route('/api/find-email', methods=['POST'])
def find_email():
    data = request.json
    company_name = data.get('company_name')
    company_url = data.get('company_url')
    
    emails = find_company_email(company_name, company_url)
    
    return jsonify({
        'success': True,
        'emails': emails
    })

@app.route('/api/apply-job', methods=['POST'])
def apply_job():
    try:
        data = request.json
        job = data.get('job')
        manual_email = data.get('manual_email')
        
        if not job:
            return jsonify({
                'success': False,
                'error': 'Job data is missing'
            }), 400
        
        company = job.get('company', 'Unknown Company')
        title = job.get('title', 'Unknown Position')
        description = job.get('description', title)
        
        if not company or not title:
            return jsonify({
                'success': False,
                'error': 'Company and title are required'
            }), 400
        
        print(f"\n📝 APPLY JOB REQUEST:")
        print(f"  Company: {company}")
        print(f"  Title: {title}")
        print(f"  Manual email: {manual_email}")
        
        # Select best CV
        cv_raw = select_best_cv(description, company, title)
        if not cv_raw:
            return jsonify({
                'success': False,
                'error': 'Failed to select CV'
            }), 500
        
        cv_data = parse_json(cv_raw)
        selected_cv_key = cv_data.get('selected_cv', 'data_analyst')
        
        if selected_cv_key not in CV_VERSIONS:
            selected_cv_key = "data_analyst"
        
        cv_path = CV_VERSIONS[selected_cv_key]
        
        # Generate cover letter
        cl_raw = generate_cover_letter_content(description, company, title)
        if not cl_raw:
            return jsonify({
                'success': False,
                'error': 'Failed to generate cover letter'
            }), 500
        
        cl_data = parse_json(cl_raw)
        
        if not cl_data.get('email_body'):
            return jsonify({
                'success': False,
                'error': 'Email body generation failed'
            }), 500
        
        email_subject = cl_data.get('email_subject', f'Application for {title} - Ramesh Kadariya')
        
        # Generate cover letter PDF in memory
        cl_pdf_bytes = generate_cover_letter_pdf(company, title, cl_data["cover_letter_content"])
        
        # Get email
        emails = job.get('emails_in_post', [])
        if manual_email:
            emails = [manual_email]
        elif not emails:
            emails = find_company_email(company, job.get('company_url'))
        
        # Log the generated email body
        print(f"  Generated email body preview: {cl_data['email_body'][:150]}...")
        
        return jsonify({
            'success': True,
            'message': 'Application created successfully',
            'emails': emails,
            'cv_type': selected_cv_key.replace('_', ' ').title(),
            'email_subject': email_subject,
            'email_body': cl_data["email_body"],
            'cv_bytes': None,  # Will be handled in send_email
            'cl_bytes': None   # Will be handled in send_email
        })
        
    except Exception as e:
        print(f"  ❌ Exception in apply_job: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/send-email', methods=['POST'])
def send_email():
    try:
        data = request.json
        recipient = data.get('recipient')
        subject = data.get('subject')
        body = data.get('body')
        cv_path = data.get('cv_path')
        
        # Validate inputs
        if not recipient:
            return jsonify({
                'success': False,
                'error': 'Recipient email is required'
            }), 400
        
        if not subject:
            return jsonify({
                'success': False,
                'error': 'Email subject is required'
            }), 400
        
        if not body:
            return jsonify({
                'success': False,
                'error': 'Email body is empty'
            }), 400
        
        # Add greeting and closing if not present
        body_stripped = body.strip()
        if not body_stripped.startswith('Dear'):
            body = f"Dear Hiring Manager,\n\n{body_stripped}\n\nSincerely,\nRamesh Kadariya"
        
        print(f"\n📧 SEND EMAIL REQUEST:")
        print(f"  Recipient: {recipient}")
        print(f"  Subject: {subject}")
        print(f"  Body length: {len(body) if body else 0} chars")
        
        # Read CV file if it exists
        cv_bytes = None
        if cv_path and os.path.exists(cv_path):
            try:
                with open(cv_path, 'rb') as f:
                    cv_bytes = f.read()
                print(f"  ✅ Read CV from disk: {cv_path}")
            except Exception as e:
                print(f"  ⚠️ Could not read CV: {e}")
        
        # Send email with attachments
        success = send_application_email_with_bytes(
            recipient, 
            subject, 
            body, 
            cv_bytes,
            "CV_Application.pdf"
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Email sent successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to send email. Check server logs for details.'
            }), 500
        
    except Exception as e:
        print(f"  ❌ Exception in send_email: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        applications_dir = 'applications'
        if not os.path.exists(applications_dir):
            return jsonify({
                'total_applications': 0,
                'companies': []
            })
        
        companies = [d for d in os.listdir(applications_dir) if os.path.isdir(os.path.join(applications_dir, d))]
        
        return jsonify({
            'total_applications': len(companies),
            'companies': companies
        })
        
    except Exception as e:
        return jsonify({
            'total_applications': 0,
            'companies': []
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
