"""
PDF Generation Service for FormPilot AI.
Uses ReportLab to dynamically generate:
1. Formally formatted completed application forms with user answers.
2. Comprehensive Form Audit & Verification Reports.
"""
import os
import uuid
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from ..core.config import settings

class PDFGenerator:
    @staticmethod
    def generate_filled_form_pdf(
        doc_title: str,
        user_info: Dict[str, Any],
        fields: List[Dict[str, Any]],
        output_filename: str = None
    ) -> str:
        """Generate a clean, printable PDF of the completed form."""
        if not output_filename:
            output_filename = f"completed_form_{uuid.uuid4().hex[:8]}.pdf"
        output_path = os.path.join(settings.GENERATED_DIR, output_filename)

        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
        )
        story = []
        styles = getSampleStyleSheet()

        # Custom Styles
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#1E3A8A"),
            alignment=1, # Center
            spaceAfter=6
        )
        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#475569"),
            alignment=1,
            spaceAfter=15
        )
        section_style = ParagraphStyle(
            "SectionTitle",
            parent=styles["Heading2"],
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#0F172A"),
            spaceBefore=12,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#1E293B")
        )

        # Header Title
        story.append(Paragraph(doc_title.upper(), title_style))
        story.append(Paragraph("FormPilot AI Verified Application Document", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceAfter=15))

        # Personal / Applicant Details Table
        story.append(Paragraph("I. APPLICANT SUMMARY", section_style))
        applicant_data = [
            [
                Paragraph("<b>Applicant Name:</b>", body_style),
                Paragraph(str(user_info.get("full_name") or user_info.get("name") or "N/A"), body_style),
                Paragraph("<b>Email:</b>", body_style),
                Paragraph(str(user_info.get("email") or "N/A"), body_style)
            ],
            [
                Paragraph("<b>Mobile:</b>", body_style),
                Paragraph(str(user_info.get("mobile") or user_info.get("phone") or "N/A"), body_style),
                Paragraph("<b>Application ID:</b>", body_style),
                Paragraph(f"FP-{uuid.uuid4().hex[:6].upper()}", body_style)
            ]
        ]
        t_app = Table(applicant_data, colWidths=[110, 150, 100, 160])
        t_app.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_app)
        story.append(Spacer(1, 15))

        # Form Fields Table
        story.append(Paragraph("II. COMPLETED APPLICATION FIELDS", section_style))
        table_rows = [
            [
                Paragraph("<b>#</b>", body_style),
                Paragraph("<b>Field Name</b>", body_style),
                Paragraph("<b>Entered Information</b>", body_style),
                Paragraph("<b>Status</b>", body_style)
            ]
        ]

        for idx, f in enumerate(fields, 1):
            val = str(f.get("value") or "-")
            status = f.get("status", "Verified")
            status_color = "#10B981" if status.lower() in ["valid", "verified"] else "#F59E0B"
            table_rows.append([
                Paragraph(str(idx), body_style),
                Paragraph(f.get("label_en") or f.get("label", "Field"), body_style),
                Paragraph(val, body_style),
                Paragraph(f'<font color="{status_color}"><b>{status.upper()}</b></font>', body_style)
            ])

        t_fields = Table(table_rows, colWidths=[30, 200, 210, 80])
        t_fields.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('PADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ]))
        story.append(t_fields)
        story.append(Spacer(1, 20))

        # Declaration & Sign-off Block
        story.append(Paragraph("III. APPLICANT UNDERTAKING & DECLARATION", section_style))
        decl_text = (
            "I hereby declare that the particulars furnished above are true, complete, and correct to the best of my "
            "knowledge and belief. In the event of any information being found false or incorrect at any stage, my candidature "
            "is liable to be cancelled without any notice. Generated with FormPilot AI assistant."
        )
        story.append(Paragraph(decl_text, body_style))
        story.append(Spacer(1, 25))

        sign_table = Table([
            [
                Paragraph("Date: ____________________", body_style),
                Paragraph("Place: ____________________", body_style),
                Paragraph("Signature of Applicant: ____________________", body_style)
            ]
        ], colWidths=[150, 150, 220])
        story.append(sign_table)

        doc.build(story)
        return output_path

    @staticmethod
    def generate_audit_report_pdf(
        doc_title: str,
        analysis_data: Dict[str, Any],
        output_filename: str = None
    ) -> str:
        """Generate an annotated review and error detection report."""
        if not output_filename:
            output_filename = f"form_audit_report_{uuid.uuid4().hex[:8]}.pdf"
        output_path = os.path.join(settings.GENERATED_DIR, output_filename)

        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
        )
        story = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Heading1"],
            fontSize=16,
            textColor=colors.HexColor("#0F172A"),
            alignment=1,
            spaceAfter=4
        )
        body_style = ParagraphStyle(
            "ReportBody",
            parent=styles["Normal"],
            fontSize=9,
            leading=12
        )

        story.append(Paragraph("FORMPILOT AI — FORM VERIFICATION & AUDIT REPORT", title_style))
        story.append(Paragraph(f"Document Audited: {doc_title}", body_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#06B6D4"), spaceAfter=12))

        # Summary Metrics Table
        issues = analysis_data.get("issues_and_errors", [])
        total_fields = analysis_data.get("total_fields", 0)
        
        metrics_data = [
            [
                Paragraph(f"<b>Total Fields Detected:</b> {total_fields}", body_style),
                Paragraph(f"<b>Issues / Warnings:</b> {len(issues)}", body_style),
                Paragraph(f"<b>Readiness Score:</b> {'100%' if len(issues) == 0 else f'{max(0, 100 - len(issues)*12)}%'}", body_style)
            ]
        ]
        t_met = Table(metrics_data, colWidths=[170, 170, 180])
        t_met.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('PADDING', (0,0), (-1,-1), 6)
        ]))
        story.append(t_met)
        story.append(Spacer(1, 15))

        # Detected Issues List
        story.append(Paragraph("<b>Detected Inconsistencies & Required Corrections:</b>", body_style))
        if not issues:
            story.append(Paragraph("No critical errors or missing mandatory fields detected. Document is ready for submission.", body_style))
        else:
            for item in issues:
                story.append(Spacer(1, 4))
                issue_p = Paragraph(f"• <b>[{item.get('severity', 'WARNING').upper()}]</b> {item.get('field', 'Field')}: {item.get('error_en', item.get('issue_en', ''))}", body_style)
                story.append(issue_p)
                if item.get("suggested_correction"):
                    story.append(Paragraph(f"   <i>Action: {item.get('suggested_correction')}</i>", body_style))

        doc.build(story)
        return output_path
