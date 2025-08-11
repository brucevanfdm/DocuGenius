@echo off
REM DocuGenius CLI for Windows
REM This batch file provides document conversion functionality

setlocal enabledelayedexpansion

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    exit /b 1
)

REM Check if file argument is provided
if "%~1"=="" (
    echo DocuGenius CLI - Document to Markdown Converter
    echo Usage: docugenius-cli ^<file^>
    echo.
    echo Supported formats:
    echo   - Text files: .txt, .md, .markdown
    echo   - Data files: .json, .csv, .xml, .html
    echo   - Documents: .docx, .xlsx, .pptx, .pdf
    echo.
    echo Note: For document conversion, you may need to install:
    echo   pip install python-docx python-pptx openpyxl PyPDF2
    exit /b 1
)

REM Check if file exists
if not exist "%~1" (
    echo Error: File not found: %~1
    exit /b 1
)

REM Create temporary Python script
set TEMP_SCRIPT=%TEMP%\docugenius_temp_%RANDOM%.py

(
echo import sys
echo import os
echo import json
echo import csv
echo from pathlib import Path
echo.
echo def convert_text_file^(file_path^):
echo     try:
echo         with open^(file_path, 'r', encoding='utf-8'^) as f:
echo             content = f.read^(^)
echo         return content
echo     except UnicodeDecodeError:
echo         for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
echo             try:
echo                 with open^(file_path, 'r', encoding=encoding^) as f:
echo                     content = f.read^(^)
echo                 return content
echo             except UnicodeDecodeError:
echo                 continue
echo         return f"# {Path^(file_path^).name}\n\nError: Could not decode file content."
echo.
echo def convert_json_file^(file_path^):
echo     try:
echo         with open^(file_path, 'r', encoding='utf-8'^) as f:
echo             data = json.load^(f^)
echo         markdown = f"# {Path^(file_path^).name}\n\n"
echo         markdown += "```json\n"
echo         markdown += json.dumps^(data, indent=2, ensure_ascii=False^)
echo         markdown += "\n```\n"
echo         return markdown
echo     except Exception as e:
echo         return f"# {Path^(file_path^).name}\n\nError converting JSON: {str^(e^)}"
echo.
echo def convert_csv_file^(file_path^):
echo     try:
echo         markdown = f"# {Path^(file_path^).name}\n\n"
echo         with open^(file_path, 'r', encoding='utf-8'^) as f:
echo             reader = csv.reader^(f^)
echo             rows = list^(reader^)
echo         if not rows:
echo             return markdown + "Empty CSV file."
echo         if rows:
echo             markdown += "| " + " | ".join^(rows[0]^) + " |\n"
echo             markdown += "| " + " | ".join^(["---"] * len^(rows[0]^)^) + " |\n"
echo             for row in rows[1:]:
echo                 padded_row = row + [""] * ^(len^(rows[0]^) - len^(row^)^)
echo                 markdown += "| " + " | ".join^(padded_row[:len^(rows[0]^)]^) + " |\n"
echo         return markdown
echo     except Exception as e:
echo         return f"# {Path^(file_path^).name}\n\nError converting CSV: {str^(e^)}"
echo.
echo def convert_docx_file^(file_path^):
echo     try:
echo         from docx import Document
echo         doc = Document^(file_path^)
echo         file_name = Path^(file_path^).name
echo         markdown = f"# {file_name}\n\n"
echo         for paragraph in doc.paragraphs:
echo             text = paragraph.text.strip^(^)
echo             if text:
echo                 style_name = paragraph.style.name.lower^(^) if paragraph.style else ""
echo                 if "heading 1" in style_name:
echo                     markdown += f"# {text}\n\n"
echo                 elif "heading 2" in style_name:
echo                     markdown += f"## {text}\n\n"
echo                 elif "heading 3" in style_name:
echo                     markdown += f"### {text}\n\n"
echo                 elif "heading 4" in style_name:
echo                     markdown += f"#### {text}\n\n"
echo                 elif "heading 5" in style_name:
echo                     markdown += f"##### {text}\n\n"
echo                 elif "heading 6" in style_name:
echo                     markdown += f"###### {text}\n\n"
echo                 else:
echo                     markdown += f"{text}\n\n"
echo         for table in doc.tables:
echo             markdown += "\n"
echo             for i, row in enumerate^(table.rows^):
echo                 row_data = []
echo                 for cell in row.cells:
echo                     cell_text = cell.text.strip^(^).replace^('\n', ' '^)
echo                     row_data.append^(cell_text^)
echo                 if i == 0:
echo                     markdown += "| " + " | ".join^(row_data^) + " |\n"
echo                     markdown += "| " + " | ".join^(["---"] * len^(row_data^)^) + " |\n"
echo                 else:
echo                     markdown += "| " + " | ".join^(row_data^) + " |\n"
echo             markdown += "\n"
echo         return markdown
echo     except ImportError:
echo         return f"# {Path^(file_path^).name}\n\nError: python-docx library not available"
echo     except Exception as e:
echo         return f"# {Path^(file_path^).name}\n\nError converting DOCX: {str^(e^)}"
echo.
echo def convert_excel_file^(file_path^):
echo     try:
echo         from openpyxl import load_workbook
echo         workbook = load_workbook^(file_path, data_only=True^)
echo         file_name = Path^(file_path^).name
echo         markdown = f"# {file_name}\n\n"
echo         for sheet_name in workbook.sheetnames:
echo             worksheet = workbook[sheet_name]
echo             markdown += f"## {sheet_name}\n\n"
echo             rows = list^(worksheet.iter_rows^(values_only=True^)^)
echo             if not rows:
echo                 markdown += "*Empty sheet*\n\n"
echo                 continue
echo             non_empty_rows = []
echo             for row in rows:
echo                 if any^(cell is not None and str^(cell^).strip^(^) for cell in row^):
echo                     non_empty_rows.append^(row^)
echo             if not non_empty_rows:
echo                 markdown += "*No data found*\n\n"
echo                 continue
echo             max_cols = max^(len^([cell for cell in row if cell is not None]^) for row in non_empty_rows^)
echo             for i, row in enumerate^(non_empty_rows^):
echo                 row_data = []
echo                 for j in range^(max_cols^):
echo                     if j ^< len^(row^) and row[j] is not None:
echo                         row_data.append^(str^(row[j]^).strip^(^)^)
echo                     else:
echo                         row_data.append^(""^)
echo                 if i == 0:
echo                     markdown += "| " + " | ".join^(row_data^) + " |\n"
echo                     markdown += "| " + " | ".join^(["---"] * len^(row_data^)^) + " |\n"
echo                 else:
echo                     markdown += "| " + " | ".join^(row_data^) + " |\n"
echo             markdown += "\n"
echo         return markdown
echo     except ImportError:
echo         return f"# {Path^(file_path^).name}\n\nError: openpyxl library not available"
echo     except Exception as e:
echo         return f"# {Path^(file_path^).name}\n\nError converting Excel: {str^(e^)}"
echo.
echo def convert_pptx_file^(file_path^):
echo     try:
echo         from pptx import Presentation
echo         prs = Presentation^(file_path^)
echo         file_name = Path^(file_path^).name
echo         markdown = f"# {file_name}\n\n"
echo         for i, slide in enumerate^(prs.slides, 1^):
echo             markdown += f"## Slide {i}\n\n"
echo             slide_text = []
echo             for shape in slide.shapes:
echo                 if hasattr^(shape, "text"^) and shape.text.strip^(^):
echo                     slide_text.append^(shape.text.strip^(^)^)
echo             if slide_text:
echo                 for text in slide_text:
echo                     lines = text.split^('\n'^)
echo                     for line in lines:
echo                         line = line.strip^(^)
echo                         if line:
echo                             markdown += f"{line}\n\n"
echo             else:
echo                 markdown += "*No text content found*\n\n"
echo             markdown += "---\n\n"
echo         return markdown
echo     except ImportError:
echo         return f"# {Path^(file_path^).name}\n\nError: python-pptx library not available"
echo     except Exception as e:
echo         return f"# {Path^(file_path^).name}\n\nError converting PowerPoint: {str^(e^)}"
echo.
echo def convert_pdf_file^(file_path^):
echo     try:
echo         import PyPDF2
echo         file_name = Path^(file_path^).name
echo         markdown = f"# {file_name}\n\n"
echo         with open^(file_path, 'rb'^) as file:
echo             pdf_reader = PyPDF2.PdfReader^(file^)
echo             markdown += f"**Total Pages:** {len^(pdf_reader.pages^)}\n\n"
echo             for i, page in enumerate^(pdf_reader.pages, 1^):
echo                 markdown += f"## Page {i}\n\n"
echo                 try:
echo                     text = page.extract_text^(^)
echo                     if text.strip^(^):
echo                         lines = text.split^('\n'^)
echo                         cleaned_lines = []
echo                         for line in lines:
echo                             line = line.strip^(^)
echo                             if line:
echo                                 cleaned_lines.append^(line^)
echo                         if cleaned_lines:
echo                             markdown += '\n\n'.join^(cleaned_lines^) + "\n\n"
echo                         else:
echo                             markdown += "*No text content found on this page*\n\n"
echo                     else:
echo                         markdown += "*No text content found on this page*\n\n"
echo                 except Exception as page_error:
echo                     markdown += f"*Error extracting text from page {i}: {str^(page_error^)}*\n\n"
echo                 markdown += "---\n\n"
echo         return markdown
echo     except ImportError:
echo         return f"# {Path^(file_path^).name}\n\nError: PyPDF2 library not available"
echo     except Exception as e:
echo         return f"# {Path^(file_path^).name}\n\nError converting PDF: {str^(e^)}"
echo.
echo def convert_document_file^(file_path^):
echo     file_name = Path^(file_path^).name
echo     file_ext = Path^(file_path^).suffix.lower^(^)
echo     try:
echo         if file_ext in ['.docx']:
echo             return convert_docx_file^(file_path^)
echo         elif file_ext in ['.xlsx', '.xls']:
echo             return convert_excel_file^(file_path^)
echo         elif file_ext in ['.pptx']:
echo             return convert_pptx_file^(file_path^)
echo         elif file_ext == '.pdf':
echo             return convert_pdf_file^(file_path^)
echo         else:
echo             markdown = f"# {file_name}\n\n"
echo             markdown += f"**Document Type:** {file_ext.upper^(^)} file\n\n"
echo             markdown += "This file type is not yet supported for full conversion.\n\n"
echo             markdown += f"- **File:** {file_name}\n"
echo             markdown += f"- **Size:** {os.path.getsize^(file_path^)} bytes\n\n"
echo             return markdown
echo     except Exception as e:
echo         markdown = f"# {file_name}\n\n"
echo         markdown += f"**Error converting {file_ext.upper^(^)} file**\n\n"
echo         markdown += f"Error: {str^(e^)}\n\n"
echo         markdown += f"- **File:** {file_name}\n"
echo         markdown += f"- **Size:** {os.path.getsize^(file_path^)} bytes\n"
echo         return markdown
echo.
echo file_path = sys.argv[1]
echo file_ext = Path^(file_path^).suffix.lower^(^)
echo.
echo if file_ext in ['.txt', '.md', '.markdown']:
echo     content = convert_text_file^(file_path^)
echo elif file_ext == '.json':
echo     content = convert_json_file^(file_path^)
echo elif file_ext == '.csv':
echo     content = convert_csv_file^(file_path^)
echo elif file_ext in ['.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt', '.pdf']:
echo     content = convert_document_file^(file_path^)
echo else:
echo     content = convert_text_file^(file_path^)
echo.
echo print^(content^)
) > "%TEMP_SCRIPT%"

REM Run the Python script
python "%TEMP_SCRIPT%" "%~1"
set RESULT=%ERRORLEVEL%

REM Clean up temporary script
del "%TEMP_SCRIPT%" >nul 2>&1

exit /b %RESULT%
