# CAP 931 - Automated Document Processing Tests

import io
from unittest.mock import Mock

import pytest
import pymupdf
from docx import Document

from document_processor import extract_document_text


def make_upload(name, content):
    uploaded = Mock()
    uploaded.name = name
    uploaded.getvalue.return_value = content
    return uploaded


# TEST 1 - TXT extraction
def test_txt_extraction():
    upload = make_upload("sample.txt", b"CAP 931 Sales Intelligence")

    result = extract_document_text(upload)

    assert result == "CAP 931 Sales Intelligence"


# TEST 2 - DOCX extraction
def test_docx_extraction():
    document = Document()
    document.add_paragraph("CAP 931 Word Document")

    buffer = io.BytesIO()
    document.save(buffer)

    upload = make_upload("sample.docx", buffer.getvalue())

    result = extract_document_text(upload)

    assert "CAP 931 Word Document" in result


# TEST 3 - PDF extraction
def test_pdf_extraction():
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), "CAP 931 PDF Document")

    pdf_bytes = document.tobytes()
    document.close()

    upload = make_upload("sample.pdf", pdf_bytes)

    result = extract_document_text(upload)

    assert "CAP 931 PDF Document" in result


# TEST 4 - Unsupported format
def test_unsupported_format():
    upload = make_upload("sample.exe", b"Invalid content")

    with pytest.raises(ValueError, match="Unsupported"):
        extract_document_text(upload)


# TEST 5 - Empty TXT document
def test_empty_document():
    upload = make_upload("empty.txt", b"")

    with pytest.raises(ValueError, match="No readable text"):
        extract_document_text(upload)


# TEST 6 - Upload size limit
def test_upload_size_limit():
    upload = make_upload("large.txt", b"A" * (5 * 1024 * 1024 + 1))

    with pytest.raises(ValueError, match="5 MB"):
        extract_document_text(upload)


# TEST 7 - AI input length limit
def test_ai_input_limit():
    upload = make_upload("long.txt", b"A" * 20000)

    result = extract_document_text(upload)

    assert len(result) == 15000


# TEST 8 - Missing uploaded file
def test_missing_file():
    result = extract_document_text(None)

    assert result == ""


# TEST 9 - DOCX table extraction
def test_docx_table_extraction():
    document = Document()

    table = document.add_table(rows=1, cols=1)
    table.cell(0, 0).text = "Sales Revenue Data"

    buffer = io.BytesIO()
    document.save(buffer)

    upload = make_upload("table.docx", buffer.getvalue())

    result = extract_document_text(upload)

    assert "Sales Revenue Data" in result