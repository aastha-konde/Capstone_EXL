"""PDF report generation using ReportLab"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def generate_pdf_report(
    question: str,
    executive_summary: dict,
    kpis: dict,
    recommendations: list,
    forecasts: dict = None,
    output_path: str = "/tmp/report.pdf",
) -> str:
    """
    Generate a PDF report with executive summary, KPIs, and recommendations.
    """
    try:
        # Create document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.75*inch,
            bottomMargin=0.5*inch,
        )

        # Container for document elements
        elements = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4e78'),
            spaceAfter=30,
            alignment=1,  # Center
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2e5c8a'),
            spaceAfter=12,
        )

        # Title
        elements.append(Paragraph("DecisionLens AI Executive Report", title_style))
        elements.append(Spacer(1, 0.3*inch))

        # Metadata
        metadata_style = styles['Normal']
        elements.append(Paragraph(f"<b>Question:</b> {question}", metadata_style))
        elements.append(Paragraph(f"<b>Generated:</b> {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", metadata_style))
        elements.append(Spacer(1, 0.3*inch))

        # Executive Summary
        if executive_summary:
            elements.append(Paragraph("Executive Summary", heading_style))

            if isinstance(executive_summary, dict) and "narrative" in executive_summary:
                elements.append(Paragraph(executive_summary["narrative"], styles['Normal']))

            if isinstance(executive_summary, dict) and "key_findings" in executive_summary:
                elements.append(Spacer(1, 0.2*inch))
                elements.append(Paragraph("<b>Key Findings:</b>", styles['Normal']))
                for finding in executive_summary["key_findings"][:5]:
                    elements.append(Paragraph(f"• {finding}", styles['Normal']))

            elements.append(Spacer(1, 0.3*inch))

        # KPIs Table
        if kpis:
            elements.append(Paragraph("Key Performance Indicators", heading_style))

            kpi_data = [["Metric", "Value", "Unit"]]
            for metric, info in list(kpis.items())[:10]:
                if isinstance(info, dict):
                    kpi_data.append([
                        metric,
                        f"{info.get('value', 'N/A'):.2f}" if isinstance(info.get('value'), (int, float)) else str(info.get('value', 'N/A')),
                        info.get('unit', ''),
                    ])

            kpi_table = Table(kpi_data)
            kpi_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(kpi_table)
            elements.append(Spacer(1, 0.3*inch))

        # Recommendations
        if recommendations:
            elements.append(PageBreak())
            elements.append(Paragraph("Recommended Actions", heading_style))

            for i, rec in enumerate(recommendations[:5], 1):
                priority = rec.get("priority", "Medium") if isinstance(rec, dict) else ""
                title = rec.get("title", "Action") if isinstance(rec, dict) else ""
                impact = rec.get("expected_impact", "") if isinstance(rec, dict) else ""

                elements.append(Paragraph(f"<b>{i}. {title}</b> [{priority}]", styles['Normal']))
                elements.append(Paragraph(f"Impact: {impact}", styles['Normal']))
                elements.append(Spacer(1, 0.15*inch))

        # Forecasts
        if forecasts:
            elements.append(PageBreak())
            elements.append(Paragraph("Forecasts", heading_style))

            for metric, forecast_data in list(forecasts.items())[:3]:
                elements.append(Paragraph(f"<b>{metric}</b>", styles['Normal']))
                if isinstance(forecast_data, list) and len(forecast_data) > 0:
                    for f in forecast_data[:3]:
                        if isinstance(f, dict):
                            elements.append(Paragraph(
                                f"Period: {f.get('period', 'N/A')} - Value: {f.get('value', 0):.2f}",
                                styles['Normal']
                            ))
                elements.append(Spacer(1, 0.15*inch))

        # Footer
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph(
            "<i>Prepared by DecisionLens AI | Confidential</i>",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey)
        ))

        # Build PDF
        doc.build(elements)

        logger.info(f"PDF report generated: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"PDF generation failed: {e}")
        raise
