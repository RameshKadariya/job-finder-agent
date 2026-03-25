import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor


def generate_cover_letter(output_path, company, role, email_body):
    """Generate PDF using ReportLab"""
    
    email_body = email_body.strip()
    if email_body.startswith("Dear Hiring Manager"):
        email_body = email_body.replace("Dear Hiring Manager,", "").replace("Dear Hiring Manager", "").strip()
    
    if "\n\n" in email_body:
        paragraphs = [p.strip() for p in email_body.split("\n\n") if p.strip()]
    else:
        sentences = email_body.split(". ")
        if len(sentences) > 6:
            third = len(sentences) // 3
            paragraphs = [". ".join(sentences[:third]) + ".", ". ".join(sentences[third:third*2]) + ".", ". ".join(sentences[third*2:])]
        else:
            paragraphs = [email_body]
    
    clean_paragraphs = []
    for para in paragraphs:
        para = para.strip()
        if not para or para in ["Best regards,", "Sincerely,", "Warm regards,", "Ramesh Kadariya", "Yours sincerely,"]:
            continue
        if para.startswith("Dear "):
            continue
        clean_paragraphs.append(para)
    
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    green = HexColor('#059669')
    light_green = HexColor('#d1fae5')
    light_green_bg = HexColor('#f0fdf4')
    dark_text = HexColor('#111111')
    gray_text = HexColor('#555555')
    
    c.setFillColor(green)
    c.rect(0, height - 80, width, 80, fill=True, stroke=False)
    c.setFillColor(HexColor('#FFFFFF'))
    c.setFont("Helvetica-Bold", 28)
    c.drawString(30, height - 45, "RAMESH KADARIYA")
    c.setFillColor(light_green)
    c.setFont("Helvetica", 9)
    c.drawString(30, height - 65, "COMPUTER SYSTEMS ENGINEER · DATA & DATABASE SPECIALIST")
    
    today = datetime.date.today().strftime("%B %d, %Y")
    c.setFillColor(gray_text)
    c.setFont("Helvetica", 10)
    c.drawString(30, height - 110, today)
    
    y_pos = height - 150
    c.setFillColor(light_green_bg)
    c.rect(30, y_pos - 50, width - 60, 55, fill=True, stroke=False)
    c.setFillColor(green)
    c.rect(30, y_pos - 50, 5, 55, fill=True, stroke=False)
    c.setFillColor(green)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(45, y_pos - 15, "RE: APPLICATION FOR")
    c.setFillColor(dark_text)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(45, y_pos - 32, role)
    c.setFillColor(green)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(45, y_pos - 47, company)
    
    y_pos -= 85
    c.setFillColor(dark_text)
    c.setFont("Times-Italic", 12)
    c.drawString(30, y_pos, "Dear Hiring Manager,")
    
    y_pos -= 25
    c.setFont("Helvetica", 11)
    c.setFillColor(HexColor('#333333'))
    
    for para in clean_paragraphs:
        words = para.split()
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            if c.stringWidth(test_line, "Helvetica", 11) < (width - 60):
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        for line in lines:
            if y_pos < 100:
                break
            c.drawString(30, y_pos, line)
            y_pos -= 15
        y_pos -= 10
    
    y_pos -= 10
    if y_pos > 100:
        c.setFont("Times-Italic", 11)
        c.setFillColor(gray_text)
        c.drawString(30, y_pos, "Sincerely,")
        y_pos -= 20
        c.setFont("Times-Bold", 16)
        c.setFillColor(dark_text)
        c.drawString(30, y_pos, "Ramesh Kadariya")
        y_pos -= 18
        c.setFont("Helvetica", 9)
        c.setFillColor(gray_text)
        c.drawString(30, y_pos, "BSc (Hons) Computer System Engineering")
    
    c.setFillColor(green)
    c.rect(0, 0, width, 40, fill=True, stroke=False)
    c.setFillColor(light_green)
    c.setFont("Helvetica", 8)
    footer_text = "linkedin.com/in/ramesh-kadariya-638979280 | github.com/rameshkadariya | rameshkadariya.com.np"
    text_width = c.stringWidth(footer_text, "Helvetica", 8)
    c.drawString((width - text_width) / 2, 15, footer_text)
    
    c.save()
    print(f"✅ Cover Letter saved: {output_path}")
