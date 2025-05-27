"""
Main Streamlit application file for Resume Skill Extractor
"""
import streamlit as st
from pdf_parser import extract_text_from_pdf
from llm_extractor import extract_structured_data, extract_contact_info, is_valid_resume
import json
import os
import io
import uuid
import re

DATA_DIR = "resumes_data"

# Create data directory if it doesn't exist
os.makedirs('resumes_data', exist_ok=True)

def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing special characters and replacing spaces with underscores"""
    # Remove special characters, keep only alphanumeric, dots, and underscores
    sanitized = re.sub(r'[^a-zA-Z0-9._]', '', filename)
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    return sanitized

def save_extracted_data(data_to_save: dict, original_pdf_filename: str, raw_text: str) -> bool:
    """Save extracted resume data to JSON file"""
    try:
        # Add raw text to the data
        data_with_text = data_to_save.copy()
        data_with_text['raw_text'] = raw_text
        
        # Generate sanitized filename
        sanitized_name = sanitize_filename(original_pdf_filename)
        json_filename = f"{sanitized_name}_{uuid.uuid4()}.json"
        full_path = os.path.join(DATA_DIR, json_filename)
        
        # Write JSON file
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data_with_text, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error saving data: {str(e)}")
        return False

def load_all_saved_resumes() -> list:
    """Load all saved resume data from JSON files"""
    try:
        resumes = []
        # Get all JSON files in the directory
        json_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
        
        for filename in json_files:
            try:
                filepath = os.path.join(DATA_DIR, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    resume_data = json.load(f)
                    # Add filename for identification
                    resume_data['__filename'] = filename
                    resumes.append(resume_data)
            except Exception as e:
                print(f"Warning: Failed to load {filename}: {str(e)}")
                continue
        
        return resumes
    except Exception as e:
        print(f"Error loading resumes: {str(e)}")
        return []

def display_structured_data(data):
    """Display the structured data in a nice format"""
    # Create a copy of data without raw_text if it exists
    display_data = {k: v for k, v in data.items() if k != 'raw_text'}
    
    st.subheader("Structured Information")
    
    st.markdown("""
    <style>
    .section-header {
        font-size: 1.2em;
        color: #f1c40f; /* bright yellow for good contrast */
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .entry-header {
        font-size: 1.1em;
        color: #1abc9c; /* light teal for variety and contrast */
        margin-bottom: 5px;
    }

    .field-label {
        font-weight: bold;
        color: #ecf0f1; /* very light gray for readability */
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Personal Info
    st.markdown("""
    <div class='section-header'>Personal Information</div>
    """, unsafe_allow_html=True)
    st.write(f"Name: {display_data['name']}")
    st.write(f"Email: {display_data['email']}")
    st.write(f"Phone: {display_data['phone']}")
    st.markdown("---")
    
    # Skills
    st.markdown("""
    <div class='section-header'>Skills</div>
    """, unsafe_allow_html=True)
    skills = display_data.get('skills', [])
    if skills:
        st.markdown("""
        <ul class='skills-list'>
            {skills_list}
        </ul>
        """.format(
            skills_list="\n".join([f"<li>{skill}</li>" for skill in skills])
        ), unsafe_allow_html=True)
    st.markdown("---")
    
    # Work Experience
    st.markdown("""
    <div class='section-header'>Work Experience</div>
    """, unsafe_allow_html=True)
    work_experience = display_data.get('work_experience', [])
    for exp in work_experience:
        try:
            st.markdown("""
            <div class='entry-header'>
                {company} - {role}
            </div>
            """.format(company=exp.get('company', 'N/A'), role=exp.get('role', 'N/A')), unsafe_allow_html=True)
            st.write(f"<div class='field-label'>Dates:</div> {exp.get('dates', 'N/A')}", unsafe_allow_html=True)
            st.markdown("""
            <div class='field-label'>Description:</div>
            """, unsafe_allow_html=True)
            st.write(exp.get('description', 'N/A'))
            st.markdown("---")
        except KeyError as e:
            st.error(f"Error displaying work experience: Missing field {str(e)}")
    
    # Education
    st.markdown("""
    <div class='section-header'>Education</div>
    """, unsafe_allow_html=True)
    education = display_data.get('education', [])
    for edu in education:
        try:
            st.markdown("""
            <div class='entry-header'>
                {degree} from {institution}
            </div>
            """.format(degree=edu.get('degree', 'N/A'), institution=edu.get('institution', 'N/A')), unsafe_allow_html=True)
            st.write(f"<div class='field-label'>Dates:</div> {edu.get('graduation_date', 'N/A')}", unsafe_allow_html=True)
            if edu.get('details'):
                st.markdown("""
                <div class='field-label'>Details:</div>
                """, unsafe_allow_html=True)
                st.write(edu['details'])
            st.markdown("---")
        except KeyError as e:
            st.error(f"Error displaying education: Missing field {str(e)}")
    
    # Certifications (if any)
    certifications = display_data.get('certifications', [])
    if certifications:
        st.markdown("""
        <div class='section-header'>Certifications</div>
        """, unsafe_allow_html=True)
        for cert in certifications:
            try:
                st.markdown("""
                <div class='entry-header'>
                    {name}
                </div>
                """.format(name=cert.get('name', 'N/A')), unsafe_allow_html=True)
                st.write(f"<div class='field-label'>Issued by:</div> {cert.get('issuing_organization', 'N/A')}", unsafe_allow_html=True)
                st.write(f"<div class='field-label'>Date:</div> {cert.get('date_obtained', 'N/A')}", unsafe_allow_html=True)
                if cert.get('details'):
                    st.markdown("""
                    <div class='field-label'>Details:</div>
                    """, unsafe_allow_html=True)
                    st.write(cert['details'])
                st.markdown("---")
            except KeyError as e:
                st.error(f"Error displaying certification: Missing field {str(e)}")

def main():
    # Sidebar navigation
    page = st.sidebar.radio(
        "Navigation",
        ["📝 Extract New Resume", "📂 View & Filter Saved Resumes"],
        key="page_selector"
    )

    if page == "📝 Extract New Resume":
        st.title("📝 Extract New Resume")
        
        # File uploader
        uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=['pdf'])
        
        if uploaded_file is not None:
            # Clear previous session state when new file is uploaded
            if 'extracted_data' in st.session_state:
                del st.session_state['extracted_data']
            
            # Convert uploaded file to BytesIO for pdfplumber
            pdf_file = io.BytesIO(uploaded_file.getvalue())
            
            # Extract text from PDF
            extracted_text = extract_text_from_pdf(pdf_file)
            
            if not extracted_text:
                st.error("Failed to extract text from PDF.")
                return
            
            # Show preview of extracted text
            st.subheader("Raw Extracted Text (Preview)")
            st.text(extracted_text[:500])
            
            # Step 1: Extract contact info first
            contact_info = extract_contact_info(extracted_text)
            
            # Step 2: Primary validation - check for name and email
            if not contact_info or not contact_info.get('name') or not contact_info.get('email'):
                st.warning("The uploaded document does not appear to be a valid resume. Could not find a recognizable name or email address.")
                return  # Stop further processing
            
            # Step 3: Secondary validation - check for resume sections
            if not is_valid_resume(extracted_text):
                st.warning("Found contact info, but the document seems to be missing typical resume sections (e.g., Experience, Skills).")
                return  # Stop further processing
            
            # If we reach here, both validations passed
            st.success("Resume validated successfully! Proceeding with full data extraction and saving.")
            
            # Extract structured data using the existing function
            extracted_data = extract_structured_data(extracted_text)
            
            # Save to session state
            if extracted_data:
                st.session_state['extracted_data'] = extracted_data
                st.session_state['raw_text'] = extracted_text
                
                # Save to file and display data
                if extracted_data:
                    success = save_extracted_data(extracted_data, uploaded_file.name, extracted_text)
                    if success:
                        display_structured_data(extracted_data)
                    else:
                        st.error("Failed to save data.")
                else:
                    st.error("Failed to extract data from the resume. Please try again with a different file.")
            if success:
                st.success("Data saved successfully!")
            else:
                st.error("Failed to save data.")
                    
    elif page == "📂 View & Filter Saved Resumes":
        st.title("📂 View & Filter Saved Resumes")
        display_saved_resumes()
    

def display_saved_resumes():
    """Display section for viewing saved resumes"""
    st.subheader("View Saved Resumes")
    
    # Load all saved resumes
    all_resumes = load_all_saved_resumes()
    
    if not all_resumes:
        st.info("No resumes saved yet.")
        return
    
    # Extract unique skills
    all_skills = set()
    for resume in all_resumes:
        all_skills.update(resume.get('skills', []))
    
    # Sort skills alphabetically
    sorted_skills = sorted(all_skills)
    
    # Skill filter
    selected_skills = st.multiselect(
        "Filter by Skills:",
        sorted_skills,
        key="skills_filter"
    )
    
    # Filter resumes based on selected skills
    filtered_resumes = [
        r for r in all_resumes
        if not selected_skills or all(skill in r.get('skills', []) for skill in selected_skills)
    ]
    
    if not filtered_resumes:
        st.info("No resumes match the current filter.")
        return
    
    # Add a blank option at the start
    display_names = ["Select a resume..."] + [
        f"{r.get('name', 'Unknown Name')} ({r.get('__filename')})"
        for r in filtered_resumes
    ]
    
    # Selectbox for viewing resumes
    selected_index = st.selectbox(
        "Select a Resume to View:",
        display_names,
        key="resume_selector",
        index=0  # Default to first option (blank)
    )
    
    # Only display resume details if a resume is actually selected
    if selected_index != "Select a resume...":
        # Get the corresponding resume data
        selected_resume = filtered_resumes[display_names.index(selected_index) - 1]  # -1 because of the added blank option
        
        # Create a copy of data without raw_text if it exists
        display_resume = {k: v for k, v in selected_resume.items() if k != 'raw_text'}
        
        # Display the selected resume
        st.subheader(f"Resume Details: {display_resume.get('name', 'Unknown Name')}")
        display_structured_data(display_resume)

if __name__ == "__main__":
    main()