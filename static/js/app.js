let currentJobs = [];
let currentJobForEmail = null;

async function searchJobs() {
    const keywords = document.getElementById('keywords').value;
    const location = document.getElementById('location').value;
    const jobType = document.getElementById('job-type').value;
    
    if (!keywords) {
        alert('Please enter job keywords');
        return;
    }
    
    const btn = document.querySelector('.btn-primary');
    btn.querySelector('.btn-text').style.display = 'none';
    btn.querySelector('.btn-loader').style.display = 'inline';
    btn.disabled = true;
    
    try {
        const response = await fetch('/api/search-jobs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keywords, location, job_type: jobType })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentJobs = data.jobs;
            displayJobs(data.jobs);
            document.getElementById('jobs-found').textContent = data.jobs.length;
        }
    } catch (error) {
        alert('Error searching jobs: ' + error.message);
    } finally {
        btn.querySelector('.btn-text').style.display = 'inline';
        btn.querySelector('.btn-loader').style.display = 'none';
        btn.disabled = false;
    }
}

function displayJobs(jobs) {
    const container = document.getElementById('jobs-container');
    const resultsSection = document.getElementById('results-section');
    
    if (jobs.length === 0) {
        container.innerHTML = '<p class="alert alert-error">No jobs found. Try different keywords.</p>';
        resultsSection.style.display = 'block';
        return;
    }
    
    container.innerHTML = jobs.map((job, index) => `
        <div class="job-card" id="job-${index}">
            <div class="job-header">
                <div>
                    <div class="job-title">${job.title}</div>
                    <div class="job-company">🏢 ${job.company}</div>
                    <div class="job-location">📍 ${job.location}</div>
                    <div class="job-location">🔗 ${job.source}</div>
                </div>
            </div>
            <div class="job-actions">
                <button class="btn btn-success" onclick="applyWithManualEmail(${index})">
                    📝 Apply with Manual Email
                </button>
                <button class="btn btn-primary" onclick="applyWithSystemSearch(${index})">
                    🔍 Apply with System Search
                </button>
                <button class="btn btn-secondary" onclick="skipJob(${index})">
                    Skip
                </button>
            </div>
            <div id="status-${index}"></div>
        </div>
    `).join('');
    
    resultsSection.style.display = 'block';
}

function applyWithManualEmail(index) {
    console.log("applyWithManualEmail called for index:", index);
    const job = currentJobs[index];
    console.log("Job:", job);
    const statusDiv = document.getElementById(`status-${index}`);
    console.log("Status div:", statusDiv);
    
    currentJobForEmail = { job, index };
    console.log("Set currentJobForEmail:", currentJobForEmail);
    
    document.getElementById('modal-company').textContent = job.company;
    document.getElementById('modal-message').textContent = 'Enter email address for application:';
    document.getElementById('email-modal').style.display = 'flex';
    document.getElementById('manual-email').focus();
    
    statusDiv.innerHTML = '<div class="alert">📝 Enter email address to continue...</div>';
    console.log("Modal should be visible now");
}

async function applyWithSystemSearch(index) {
    const job = currentJobs[index];
    const statusDiv = document.getElementById(`status-${index}`);
    
    statusDiv.innerHTML = '<div class="loader">🔍 Searching for email using Hunter.io...</div>';
    
    try {
        const emailResponse = await fetch('/api/find-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                company_name: job.company,
                company_url: job.company_url
            })
        });
        
        const emailData = await emailResponse.json();
        const emails = emailData.emails || [];
        
        if (emails.length === 0) {
            // No email found, ask for manual entry
            currentJobForEmail = { job, index };
            document.getElementById('modal-company').textContent = job.company;
            document.getElementById('modal-message').textContent = 'No email found. Please enter manually:';
            document.getElementById('email-modal').style.display = 'flex';
            document.getElementById('manual-email').focus();
            statusDiv.innerHTML = '<div class="alert alert-error">❌ No email found. Please enter manually.</div>';
        } else {
            // Email found, proceed to create application
            await createApplication(job, index, emails[0]);
        }
    } catch (error) {
        console.error('Error finding email:', error);
        statusDiv.innerHTML = `<div class="alert alert-error">❌ Error searching for email: ${error.message}</div>`;
    }
}

async function createApplication(job, index, email) {
    const statusDiv = document.getElementById(`status-${index}`);
    
    // Step 1: Create application documents
    statusDiv.innerHTML = '<div class="loader">📝 Creating CV and Cover Letter...</div>';
    
    try {
        const response = await fetch('/api/apply-job', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                job: job,
                manual_email: email
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Step 2: Show send email option
            const emailData = {
                recipient: email,
                subject: data.email_subject,
                body: data.email_body,
                cv_path: data.cv_path,
                cl_path: data.cl_path,
                index: index
            };
            
            statusDiv.innerHTML = `
                <div class="alert alert-success">
                    ✅ Application documents created!<br>
                    📁 Folder: ${data.folder}<br>
                    📧 Email: ${email}<br>
                    📄 CV Type: ${data.cv_type}<br><br>
                    <strong>Ready to send email</strong>
                    <div style="margin-top: 15px;">
                        <button class="btn btn-primary" id="send-email-btn-${index}">
                            📤 Send Email Now
                        </button>
                        <button class="btn btn-secondary" onclick="skipEmail(${index})">
                            Skip Sending
                        </button>
                    </div>
                </div>
            `;
            
            // Add event listener after the HTML is inserted
            setTimeout(() => {
                const sendBtn = document.getElementById(`send-email-btn-${index}`);
                console.log(`Setting up send button for job ${index}:`, sendBtn);
                if (sendBtn) {
                    sendBtn.addEventListener('click', () => {
                        console.log(`Send button clicked for job ${index}`);
                        sendEmail(emailData);
                    });
                } else {
                    console.error(`Send button not found: send-email-btn-${index}`);
                }
            }, 10);
            
            updateStats();
        } else {
            statusDiv.innerHTML = `<div class="alert alert-error">❌ Error: ${data.error}</div>`;
        }
    } catch (error) {
        statusDiv.innerHTML = `<div class="alert alert-error">❌ Error: ${error.message}</div>`;
    }
}

async function sendEmail(emailData) {
    console.log("sendEmail called with:", emailData);
    const statusDiv = document.getElementById(`status-${emailData.index}`);
    const btn = document.getElementById(`send-email-btn-${emailData.index}`);
    
    if (btn) {
        btn.disabled = true;
        btn.textContent = '⏳ Sending email...';
    }
    
    try {
        console.log("Sending email to:", emailData.recipient);
        
        const response = await fetch('/api/send-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                recipient: emailData.recipient,
                subject: emailData.subject,
                body: emailData.body,
                cv_path: emailData.cv_path,
                cl_path: emailData.cl_path
            })
        });
        
        console.log("Response status:", response.status);
        const data = await response.json();
        console.log("Response data:", data);
        
        if (data.success) {
            statusDiv.innerHTML = `
                <div class="alert alert-success">
                    ✅ SUCCESS! Email sent to ${emailData.recipient}<br>
                    ✉️ Check your Gmail sent folder to confirm!
                </div>
            `;
        } else {
            statusDiv.innerHTML = `<div class="alert alert-error">❌ Failed to send: ${data.error || data.message}</div>`;
            if (btn) {
                btn.disabled = false;
                btn.textContent = '📤 Retry Send Email';
            }
        }
    } catch (error) {
        console.error("Error in sendEmail:", error);
        statusDiv.innerHTML = `<div class="alert alert-error">❌ Error: ${error.message}</div>`;
        if (btn) {
            btn.disabled = false;
            btn.textContent = '📤 Retry Send Email';
        }
    }
}

function skipEmail(index) {
    const statusDiv = document.getElementById(`status-${index}`);
    statusDiv.innerHTML = '<div class="alert">ℹ️ Application saved. Email not sent.</div>';
}

function skipJob(index) {
    const jobCard = document.getElementById(`job-${index}`);
    jobCard.style.opacity = '0.5';
    jobCard.style.pointerEvents = 'none';
}

function closeEmailModal() {
    document.getElementById('email-modal').style.display = 'none';
    document.getElementById('manual-email').value = '';
    document.getElementById('modal-message').textContent = 'Enter email address for application:';
    currentJobForEmail = null;
}

async function submitManualEmail() {
    const email = document.getElementById('manual-email').value.trim();
    console.log("submitManualEmail called, email:", email);
    
    // Better email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !emailRegex.test(email)) {
        alert('Please enter a valid email address (e.g., name@company.com)');
        return;
    }
    
    console.log("Manual email submitted:", email);
    
    // Save currentJobForEmail BEFORE closing modal
    const jobData = currentJobForEmail;
    
    closeEmailModal();
    
    if (jobData) {
        console.log("Creating application for job:", jobData);
        await createApplication(
            jobData.job,
            jobData.index,
            email
        );
    } else {
        console.error("No current job for email");
    }
}

async function updateStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        document.getElementById('total-apps').textContent = data.total_applications;
    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

updateStats();

document.getElementById('keywords').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchJobs();
});

document.getElementById('location').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchJobs();
});

document.getElementById('manual-email').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') submitManualEmail();
});