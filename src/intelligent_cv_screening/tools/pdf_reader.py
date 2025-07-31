from pathlib import Path

import pymupdf
from crewai.tools import tool


@tool("PDF Reader")
def pdf_reader(file_path: str) -> str:
    """
    Reads a single PDF file and returns its text content.
    
    Args:
        file_path (str): Path to the PDF file to read
        
    Returns:
        str: Extracted text content from the PDF, or error message if failed
        
    Raises:
        Returns error messages as strings instead of raising exceptions
    """
    # Convert to Path object for better path handling
    pdf_path = Path(file_path)

    # Validate file exists and is a PDF
    if not pdf_path.exists():
        return f"Error: File not found at '{file_path}'"

    if not pdf_path.suffix.lower() == '.pdf':
        return f"Error: File '{file_path}' is not a PDF file"

    try:
        # Use context manager to ensure proper resource cleanup
        doc = pymupdf.open(str(pdf_path))

        try:
            # Check if document has pages
            if len(doc) == 0:
                return "Error: PDF document contains no pages"

            # Use list comprehension for better performance
            pages_text = [page.get_text() for page in doc]

            # Join all pages with newlines
            text = "\n".join(pages_text)

            # Return stripped text or indicate if empty
            extracted_text = text.strip()
            if not extracted_text:
                return "Warning: No text content found in PDF"

            return f"-----------Begin the profile of file: {pdf_path}----------\n" + extracted_text + "\n-----------End the profile----------"

        finally:
            # Ensure document is always closed
            doc.close()

    except pymupdf.FileDataError:
        return f"Error: '{file_path}' is not a valid PDF file or is corrupted"
    except pymupdf.EmptyFileError:
        return f"Error: PDF file '{file_path}' is empty"
    except PermissionError:
        return f"Error: Permission denied accessing '{file_path}'"
    except Exception as e:
        return f"Error reading PDF '{file_path}': {str(e)}"
