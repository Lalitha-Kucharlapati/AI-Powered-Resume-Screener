import google.generativeai as genai
import streamlit as st
import fitz  # PyMuPDF for PDF text extraction
import spacy
from fpdf import FPDF

# Configure Google Gemini API Key
genai.configure(api_key="AIzaSyBvnLOoxE1fRANbCd_b3Zt-1_rkPPv4hJ8")  # Replace with your actual API key

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from a PDF
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text

# Extract skills from text
def extract_skills(text):
    doc = nlp(text)
    skills = set()
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:  # Capture relevant skill-related words
            skills.add(token.text)
    return skills

# Function to send resume & job description to Google Gemini for ranking
def evaluate_resume(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    prompt = f"""
    You are an AI hiring assistant. Evaluate the following resume against this job description.

    **Job Description:**
    {job_description}

    **Resume:**
    {resume_text}

    **Extracted Skills from Resume:** {', '.join(resume_skills)}
    **Extracted Skills from Job Description:** {', '.join(job_skills)}

    - Rate the resume **from 0 to 100**.
    - Identify **matched and missing skills**.
    - Provide a **short explanation** on why this candidate is a good/bad fit.
    - Suggest **improvements** to make the resume stronger.
    """

    model = genai.GenerativeModel("models/gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text

# Function to generate a PDF report

def generate_pdf_report(resume_text, job_description, ai_feedback):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ✅ Use built-in font instead of DejaVuSans.ttf
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "AI Resume Screening Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, "Job Description:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, job_description)
    pdf.ln(5)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, "AI Resume Analysis:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, ai_feedback)

    pdf.output("resume_report.pdf")

# Streamlit UI
st.title("📄 AI-Powered Resume Screening System (Gemini)")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Enter Job Description")

if uploaded_file and job_description:
    st.write("🔍 **Processing resume... Please wait!**")
    resume_text = extract_text_from_pdf(uploaded_file)
    ai_feedback = evaluate_resume(resume_text, job_description)

    st.subheader("💡 AI-Generated Resume Feedback")
    st.write(ai_feedback)

    if st.button("📥 Download Report as PDF"):
        generate_pdf_report(resume_text, job_description, ai_feedback)
        with open("resume_report.pdf", "rb") as file:
            st.download_button(
                label="Download AI Report",
                data=file,
                file_name="AI_Resume_Report.pdf",
                mime="application/pdf",
            )
