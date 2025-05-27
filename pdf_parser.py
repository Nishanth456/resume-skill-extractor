"""
Module for parsing PDF documents
"""
import pdfplumber
import io

def extract_text_from_pdf(pdf_input):
    """
    Extract text from a PDF file.
    
    Args:
        pdf_input: Either a file path (string) or a file-like object
        
    Returns:
        str: The extracted text from all pages of the PDF
        
    Raises:
        ValueError: If the input is neither a string nor a file-like object
        FileNotFoundError: If the file path does not exist
        Exception: If there's an error opening or reading the PDF
    """
    try:
        # If input is a file path (string)
        if isinstance(pdf_input, str):
            with pdfplumber.open(pdf_input) as pdf:
                text = extract_text_from_pdf_pages(pdf)
        # If input is a file-like object
        elif hasattr(pdf_input, 'read'):
            with pdfplumber.open(io.BytesIO(pdf_input.read())) as pdf:
                text = extract_text_from_pdf_pages(pdf)
        else:
            raise ValueError("Input must be either a file path (string) or a file-like object")
        
        return text
    
    except FileNotFoundError:
        raise FileNotFoundError("The specified PDF file could not be found")
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")

def extract_text_from_pdf_pages(pdf):
    """
    Helper function to extract text from all pages of a PDF
    """
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip().encode('utf-8', 'ignore').decode('utf-8')


'''
# Using a file path
text = extract_text_from_pdf("path/to/file.pdf")

# Using a file-like object (e.g., from Streamlit file uploader)
text = extract_text_from_pdf(uploaded_file)
'''