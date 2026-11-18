"""
Generate realistic sample PDF documents for FormPilot AI demonstration and testing.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

SAMPLE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_blank_scholarship_form():
    path = os.path.join(SAMPLE_DIR, "blank_scholarship_application.pdf")
    doc = SimpleDocTemplate(path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle("T", parent=styles["Heading1"], fontSize=14, alignment=1, textColor=colors.HexColor("#1E3A8A"))
    sub_style = ParagraphStyle("S", parent=styles["Normal"], fontSize=9, alignment=1, textColor=colors.HexColor("#475569"))
    sec_style = ParagraphStyle("Sec", parent=styles["Heading2"], fontSize=10, textColor=colors.HexColor("#0F172A"), spaceBefore=8, spaceAfter=4)
    cell_style = ParagraphStyle("C", parent=styles["Normal"], fontSize=8, leading=10)

    story.append(Paragraph("MINISTRY OF SOCIAL JUSTICE AND EMPOWERMENT", title_style))
    story.append(Paragraph("NATIONAL SCHOLARSHIP PORTAL — POST-MATRIC SCHOLARSHIP APPLICATION FORM (BLANK)", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2563EB"), spaceAfter=10))

    story.append(Paragraph("SECTION 1: APPLICANT PERSONAL PARTICULARS", sec_style))
    data1 = [
        [Paragraph("1. Full Name of Applicant:", cell_style), Paragraph("[                                                            ]", cell_style)],
        [Paragraph("2. Father's / Guardian's Name:", cell_style), Paragraph("[                                                            ]", cell_style)],
        [Paragraph("3. Date of Birth (DD-MM-YYYY):", cell_style), Paragraph("[      -      -            ]", cell_style)],
        [Paragraph("4. Gender (Male/Female/Trans):", cell_style), Paragraph("[                            ]", cell_style)],
        [Paragraph("5. Community / Caste Category:", cell_style), Paragraph("[ SC / ST / OBC / General ]", cell_style)],
        [Paragraph("6. Aadhaar Number (12 digits):", cell_style), Paragraph("[            -            -            ]", cell_style)]
    ]
    t1 = Table(data1, colWidths=[200, 340])
    t1.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")), ('PADDING', (0,0), (-1,-1), 4)]))
    story.append(t1)

    story.append(Paragraph("SECTION 2: SOCIO-ECONOMIC & CONTACT DETAILS", sec_style))
    data2 = [
        [Paragraph("7. Annual Family Income (Rs):", cell_style), Paragraph("[ Rs.                                                      ]", cell_style)],
        [Paragraph("8. Primary Mobile Number:", cell_style), Paragraph("[ +91 -                                                  ]", cell_style)],
        [Paragraph("9. Active Email Address:", cell_style), Paragraph("[                                                            ]", cell_style)],
        [Paragraph("10. Permanent Address & PIN:", cell_style), Paragraph("[                                                            ]", cell_style)]
    ]
    t2 = Table(data2, colWidths=[200, 340])
    t2.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")), ('PADDING', (0,0), (-1,-1), 4)]))
    story.append(t2)

    story.append(Paragraph("SECTION 3: ACADEMIC & BANK ACCOUNT DETAILS", sec_style))
    data3 = [
        [Paragraph("11. College / Institution Name:", cell_style), Paragraph("[                                                            ]", cell_style)],
        [Paragraph("12. Enrolled Course / Degree:", cell_style), Paragraph("[                                                            ]", cell_style)],
        [Paragraph("13. Qualifying Exam Percentage:", cell_style), Paragraph("[              %                                            ]", cell_style)],
        [Paragraph("14. Bank Account Number (DBT):", cell_style), Paragraph("[                                                            ]", cell_style)],
        [Paragraph("15. Bank IFSC Code:", cell_style), Paragraph("[                                                            ]", cell_style)]
    ]
    t3 = Table(data3, colWidths=[200, 340])
    t3.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")), ('PADDING', (0,0), (-1,-1), 4)]))
    story.append(t3)

    story.append(Spacer(1, 10))
    story.append(Paragraph("APPLICANT DECLARATION & UNDERTAKING", sec_style))
    story.append(Paragraph("I hereby declare that all entries made above are authentic, complete and verified with original certificates.", cell_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Signature of Student: _______________________      Date: ______________", cell_style))

    doc.build(story)
    print(f"Created: {path}")

def create_filled_job_application():
    path = os.path.join(SAMPLE_DIR, "filled_job_application.pdf")
    doc = SimpleDocTemplate(path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle("T", parent=styles["Heading1"], fontSize=14, alignment=1, textColor=colors.HexColor("#0F172A"))
    sub_style = ParagraphStyle("S", parent=styles["Normal"], fontSize=9, alignment=1, textColor=colors.HexColor("#475569"))
    sec_style = ParagraphStyle("Sec", parent=styles["Heading2"], fontSize=10, textColor=colors.HexColor("#0F172A"), spaceBefore=8, spaceAfter=4)
    cell_style = ParagraphStyle("C", parent=styles["Normal"], fontSize=8, leading=10)

    story.append(Paragraph("GLOBAL TECH INNOVATIONS CORP", title_style))
    story.append(Paragraph("GRADUATE ENGINEER TRAINEE (GET) 2026 RECRUITMENT APPLICATION — SUBMITTED DRAFT", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#10B981"), spaceAfter=10))

    story.append(Paragraph("CANDIDATE PARTICULARS", sec_style))
    data = [
        [Paragraph("Candidate Full Name:", cell_style), Paragraph("ARUN KUMAR S", cell_style)],
        [Paragraph("Applied Role:", cell_style), Paragraph("Graduate Engineer Trainee — Full Stack AI", cell_style)],
        [Paragraph("Date of Birth:", cell_style), Paragraph("15-08-2003", cell_style)],
        [Paragraph("Email Address:", cell_style), Paragraph("arun.student@gmail.com", cell_style)],
        [Paragraph("Mobile Number:", cell_style), Paragraph("9876543210", cell_style)],
        [Paragraph("College / University:", cell_style), Paragraph("Government College of Technology, Coimbatore", cell_style)],
        [Paragraph("Degree Program:", cell_style), Paragraph("B.E. Computer Science and Engineering", cell_style)],
        [Paragraph("Graduation Marks / CGPA:", cell_style), Paragraph("8.62 CGPA (84.5%)", cell_style)],
        [Paragraph("Aadhaar Verification ID:", cell_style), Paragraph("4839 2048 1092", cell_style)],
        [Paragraph("Current Residential Address:", cell_style), Paragraph("12, Bharathi Street, Madurai, TN - 625020", cell_style)],
        [Paragraph("Legal Undertaking Consent:", cell_style), Paragraph("Agreed and Verified", cell_style)]
    ]
    t = Table(data, colWidths=[200, 340])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t)
    doc.build(story)
    print(f"Created: {path}")

def create_guideline_document():
    path = os.path.join(SAMPLE_DIR, "government_scheme_guidelines.pdf")
    doc = SimpleDocTemplate(path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle("T", parent=styles["Heading1"], fontSize=13, alignment=1, textColor=colors.HexColor("#7C3AED"))
    sub_style = ParagraphStyle("S", parent=styles["Normal"], fontSize=9, alignment=1, textColor=colors.HexColor("#475569"))
    sec_style = ParagraphStyle("Sec", parent=styles["Heading2"], fontSize=10, textColor=colors.HexColor("#0F172A"), spaceBefore=8, spaceAfter=4)
    cell_style = ParagraphStyle("C", parent=styles["Normal"], fontSize=8, leading=11)

    story.append(Paragraph("MINISTRY OF EDUCATION — HIGHER EDUCATION DEPARTMENT", title_style))
    story.append(Paragraph("OFFICIAL NOTIFICATION: CENTRAL SECTOR SCHEME OF SCHOLARSHIPS 2026-27", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#7C3AED"), spaceAfter=10))

    story.append(Paragraph("1. OBJECTIVE & SCHEME OVERVIEW", sec_style))
    story.append(Paragraph("The Central Sector Scheme of Scholarship for College and University Students provides financial support to meritorious students from low-income families to meet day-to-day educational expenses.", cell_style))

    story.append(Paragraph("2. ELIGIBILITY CRITERIA", sec_style))
    story.append(Paragraph("• Students must have scored above the 80th percentile in the relevant stream in Class XII examination.<br/>• Annual family income from all sources must not exceed Rs. 4,50,000 per annum.<br/>• Student must be pursuing regular full-time undergraduate courses.", cell_style))

    story.append(Paragraph("3. IMPORTANT DATES & ONLINE PORTAL", sec_style))
    story.append(Paragraph("• Opening Date for Online Applications: 01-10-2026<br/>• Last Date for Submission: 30-11-2026<br/>• Last Date for Nodal Institutional Verification: 15-12-2026<br/>• Official National Scholarship Portal: https://scholarships.gov.in", cell_style))

    story.append(Paragraph("4. MANDATORY SUPPORTING CERTIFICATES", sec_style))
    story.append(Paragraph("1. Income Certificate issued by Tahsildar / competent authority.<br/>2. Community / Caste certificate for SC/ST/OBC applicants.<br/>3. Bonafide student certificate issued by the Head of Institution.<br/>4. Bank account passbook copy seeded with Aadhaar for DBT.<br/>5. Class 10 and Class 12 official marksheets.", cell_style))

    doc.build(story)
    print(f"Created: {path}")

if __name__ == "__main__":
    create_blank_scholarship_form()
    create_filled_job_application()
    create_guideline_document()
