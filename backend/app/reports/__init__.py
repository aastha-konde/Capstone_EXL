"""Report generation (PDF and PPTX)"""

from .pdf_builder import generate_pdf_report
from .pptx_builder import generate_pptx_report

__all__ = ["generate_pdf_report", "generate_pptx_report"]
