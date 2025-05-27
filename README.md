# Resume Skill Extractor

## 📝 Project Overview

The Resume Skill Extractor is a Streamlit-based web application designed to efficiently extract and organize key information from PDF resumes. Leveraging advanced text parsing and Large Language Models (LLMs) via the Google Gemini API, it automates the tedious process of manually sifting through resumes to find relevant details like contact information, skills, work experience, and education.

### ✨ Key Features:
- **PDF Text Extraction**: Extracts raw text content from uploaded PDF resume files.
- **Intelligent Validation**: Validates resumes by checking for essential contact information (name, email) and common resume sections (e.g., 'Experience', 'Skills') using heuristic methods.
- **Structured Data Extraction**: Utilizes the Gemini API to parse raw resume text into structured JSON data, including:
  - Personal Information (Name, Email, Phone)
  - Skills
  - Work Experience (Company, Role, Dates, Description)
  - Education (Degree, Institution, Dates, Details)
  - Certifications
- **Data Persistence**: Automatically saves extracted resume data as JSON files within a dedicated `resumes_data` directory.
- **Browse & Filter**: Allows users to view previously extracted resumes and filter them by specific skills.
- **User-Friendly Interface**: Provides a clean and intuitive web interface built with Streamlit for seamless interaction.
- **Dockerized Deployment**: Packaged as a Docker image for easy and consistent deployment across various environments.

## 🚀 How It Works

1. **Upload PDF**: Users upload a PDF resume via the Streamlit interface.
2. **Text Extraction**: The `pdf_parser.py` module extracts all readable text from the PDF.
3. **Validation**: `llm_extractor.py` performs two-stage validation:
   - **Contact Info Check**: Ensures a name and email are present.
   - **Resume Section Check**: Verifies the presence of common resume keywords.
4. **LLM Processing**: If validated, the extracted raw text is sent to the Google Gemini API (via `llm_extractor.py`) to extract structured data.
5. **Save Data**: The structured data is saved as a unique JSON file in the `resumes_data` folder.
6. **View & Filter**: Users can navigate to the "View & Filter Saved Resumes" section to browse, select, and display saved resumes, with filtering options based on skills.

## 🛠️ Setup and Installation

This project is designed to be run using Docker for ease of setup and consistent environment.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running on your machine.
- A Google Gemini API key.

### 1. Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone https://github.com/Nishanth456/resume-skill-extractor.git
cd resume-skill-extractor
```

### 2. Set up Google Gemini API Key

Your project uses the Google Gemini API for structured data extraction. You need to obtain an API key and set it up:

- Go to the [Google AI Studio](https://studio.google.com/) to generate an API key.
- Create a file named `.env` in the root directory of your project (where `app.py` is located).
- Add your Gemini API key to this file in the following format:

```env
GEMINI_API_KEY=YOUR_API_KEY_HERE  (no quotes for api key)
```
Replace YOUR_API_KEY_HERE with your actual Gemini API key.


### 3. Build the Docker Image

Navigate to the project's root directory in your terminal and build the Docker image. This process downloads the necessary base image, installs dependencies, and sets up your application environment.

```bash
docker build -t resume-skill-extractor .
```
This command might take a few minutes, especially during the first run as it downloads base images and installs all Python and system dependencies (including a spaCy model).


### 4. Run the Docker Container

Once the image is built, you can run your application in a Docker container:

```bash
docker run -d -p 8501:8501 --env-file ./.env resume-skill-extractor
```

  -d: Runs the container in detached mode (in the background).
  -p 8501:8501: Maps port 8501 on your local machine to port 8501 inside the container.
  --env-file ./.env: Passes your .env file (containing your Gemini API key) into the Docker container, making it accessible to your application.


### 5. Access the Application

Open your web browser and navigate to:

```
http://localhost:8501
```

Your Resume Skill Extractor application should now be running!

### 6. Conclusion

That's it! 🎉 You're all set to start extracting structured data from resumes using the Resume Skill Extractor.

---

### 📄 License

This project is licensed under the [[MIT License](https://github.com/Nishanth456/resume-skill-extractor/blob/main/LICENSE)](LICENSE)
