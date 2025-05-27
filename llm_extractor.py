"""
Module for extracting information using LLM (Gemini) integration
"""
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

def extract_contact_info(resume_text: str) -> dict | None:
    """
    Extract basic contact information from resume text using Gemini AI.

    Args:
        resume_text: String containing the resume text

    Returns:
        dict: Contact information (name, email, phone), or None if extraction fails
    """
    try:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash-latest")

        prompt = f"""Extract ONLY the following contact information from the text and return as JSON:
        - "name": string (Full name of the candidate)
        - "email": string (Primary email address)
        - "phone": string (Primary phone number)

        Text:
        {resume_text}

        Return ONLY the JSON object with these three fields, no additional text.
        """

        response = model.generate_content(prompt)
        clean_response = response.text.strip().replace('```json', '').replace('```', '').strip()
        return json.loads(clean_response)
    except Exception as e:
        print(f"Error extracting contact info: {str(e)}")
        return None

def is_valid_resume(resume_text: str) -> bool:
    """
    Check if the resume text contains typical resume sections.

    Args:
        resume_text: String containing the resume text

    Returns:
        bool: True if the text contains typical resume sections, False otherwise
    """
    try:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash-latest")

        prompt = f"""Analyze the following text and determine if it appears to be a valid resume.
        A valid resume should contain at least one of these sections:
        - Work experience
        - Education
        - Skills
        - Projects
        - Certifications

        Return ONLY true or false.

        Text:
        {resume_text}
        """

        response = model.generate_content(prompt)
        clean_response = response.text.strip().lower()
        return clean_response in ['true', 'yes', 'valid']
    except Exception as e:
        print(f"Error validating resume: {str(e)}")
        return False

def extract_structured_data(resume_text: str) -> dict | None:
    """
    Extract structured data from resume text using Gemini AI.

    Args:
        resume_text: String containing the resume text

    Returns:
        dict: Structured data extracted from the resume, or None if extraction fails
    """
    try:
        # Load environment variables and configure Gemini
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash-latest")

        # Construct the prompt for Gemini
        prompt = f"""Extract the following information from the resume text and return it as a JSON object:

        - "name": string (Full name of the candidate)
        - "email": string (Primary email address)
        - "phone": string (Primary phone number)
        - "skills": list of strings (Technical and soft skills mentioned)
        - "work_experience": list of objects. Each object must have:
            - "company": string
            - "role": string (Job title)
            - "dates": string (e.g., "Jan 2020 - Present")
            - "description": string (Key responsibilities and achievements)
        - "education": list of objects (for formal academic degrees from universities or colleges). Each object must have:
            - "institution": string (Name of the university/college)
            - "degree": string (Formal degree title, e.g., "Bachelor of Science in Computer Science")
            - "graduation_date": string (e.g., "May 2020" or "2020-2024")
            - "details": string (Optional - additional details about the degree)
        - "certifications": list of objects (for professional certifications, online courses, and other learning). Each object must have:
            - "name": string (Name of the certification/course)
            - "issuing_organization": string (Organization that issued the certification)
            - "date_obtained": string (e.g., "Jan 2023" or "2023")
            - "details": string (Optional - additional details about the certification)

        Important notes:
        - Only include formal academic degrees (Bachelors, Masters, PhDs, etc.) in the 'education' field
        - Include all other learning achievements (certifications, online courses, professional training) in the 'certifications' field
        - If a certification is part of a formal degree program, include it in the degree's 'details' field instead of the certifications list
        - If a certification has multiple parts or levels, create separate entries in the certifications list for each part

        Resume text:
        {resume_text}

        Return ONLY the JSON object, no additional text.
        """

        # Make the API call
        try:
            response = model.generate_content(prompt)
            print(f"\nResponse content: {response.text}")
            
            if not response.text.strip():
                raise ValueError("Empty response from Gemini API")
            
            # Clean up the response text by removing markdown formatting
            clean_response = response.text.strip().replace('```json', '').replace('```', '').strip()
            
            # Parse the JSON response
            structured_data = json.loads(clean_response)
            return structured_data
            
        except Exception as e:
            print(f"\nError details: {str(e)}")
            print(f"\nRaw response: {response.text}")
            raise ValueError(f"Failed to process Gemini response: {str(e)}")

    except ValueError as e:
        print(f"Configuration error: {str(e)}")
        return None
    except Exception as e:
        print(f"Error during API call: {str(e)}")
        return None

if __name__ == "__main__":
    # Test the function
    try:
        load_dotenv()
        # Read resume text from extracted_text.txt
        with open('extracted_text.txt', 'r', encoding='utf-8') as f:
            resume_text = f.read()

        print("\nExtracting structured data from resume...")
        result = extract_structured_data(resume_text)
        
        if result:
            print("\nStructured Data:")
            print(json.dumps(result, indent=2))
        else:
            print("\nFailed to extract structured data")

    except FileNotFoundError:
        print("\nError: extracted_text.txt not found. Please make sure the file exists.")
    except Exception as e:
        print(f"\nError in test: {str(e)}")