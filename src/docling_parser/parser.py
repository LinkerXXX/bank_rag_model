from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PipelineOptions
import os

def parser_pdf(pdf_to_txt):
    # os.environ["DOCLING_OCR_ENABLED"] = "false"
    # os.environ["DOCLING_DO_OCR"] = "false"
    converter = DocumentConverter()
    result = converter.convert(pdf_to_txt)
    markdown = result.document.export_to_markdown()
    return markdown