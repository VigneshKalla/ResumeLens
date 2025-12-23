## 1.Imports
import os, zipfile, tempfile, csv ,fitz  # PyMuPDF 
import streamlit as st, pandas as pd
from docx import Document
from typing import TypedDict, Optional, List, Annotated

from langchain_google_genai import ChatGoogleGenerativeAI 

## 2.Load .env
from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("Gemini")

## 3.Page Cofig
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")
### Title & Subtitle
st.markdown("""<div style="text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        <h1 style="color: #1E3A8A; font-size: 3rem; margin-bottom: 0;">ResumeLens</h1>
        <p style="color: #000000; font-size: 1.1rem;">Automated AI Extraction & CSV Intelligence</p>
        <hr style="border: 0.6px solid #f0f2f6;"></div>""", unsafe_allow_html=True)  #6B7280

## 4.File Uploader
files = st.file_uploader(label="Feed ResumeLens", type=["zip", "pdf", "docx"], accept_multiple_files=True,
    help="Supported formats: ZIP (containing multiple resumes), PDF, or DOCX. The AI will extract data into a CSV.")

## 5.Initialize Gemini LLM        # model="gemini-2.5-flash"
llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0.2)

## 6.Structured Resume Schema
class ResumeSchema(TypedDict):
    # Core Identity 
    fullname: Optional[str]; email: Optional[str]; phone: Optional[str]; location: Optional[str]
    # Professional Summary
    summary: str; current_role: Optional[str]; experience: Optional[int]
    # Skills 
    skills: List[str]; programming_languages: List[str]; frameworks_tools: List[str]; databases: List[str]
    # Experience 
    companies: List[str]; job_titles: List[str]; responsibilities: List[str]
    # Education
    highest_education: Optional[str]; degree: Optional[str];institution: Optional[str]; graduation_year: Optional[int]
    # Projects
    projects: List[str]; project_domains: List[str]
    # Certifications
    certifications: List[str]
    # Online Presence
    links: Annotated[List[str],
    """Extract and return all URLs and link-like text found in the resume, including 
    LinkedIn, GitHub, Kaggle, portfolio websites, personal domains,
    and any visible http/https or www links. Return only valid link strings."""]
    # ATS Intelligence 
    keywords: List[str]; role_fit: Optional[str]  # ex: DA,DS, AI Engineer etc...
    ats_score: Optional[int]  # 0–100 score

structured_llm = llm.with_structured_output(ResumeSchema)

# 7.Helper functions (Read files)
def pdf_text(path): # Read text from pdf
    text = ""
    pdf = fitz.open(path)
    for page in pdf:
        text += page.get_text()
    pdf.close()
    return text

def docx_text(path): # Read textfrom docx
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def analyze(text): # Send resume text to AI and get structured data
    return structured_llm.invoke(text)

## 8. Process uploaded resumes
results = []
if files:
    with st.spinner("Analyzing resumes..."):
        for file in files:
           # ZIP FILE 
            if file.name.lower().endswith(".zip"):
                with tempfile.TemporaryDirectory() as temp_dir:
                    zip_path = os.path.join(temp_dir, file.name)
                    with open(zip_path, "wb") as f:
                        f.write(file.read())

                    zipfile.ZipFile(zip_path).extractall(temp_dir)

                    for name in os.listdir(temp_dir):
                        path = os.path.join(temp_dir, name)
                        if name.endswith(".pdf"):
                            text = pdf_text(path)
                        elif name.endswith(".docx"):
                            text = docx_text(path)
                        else:
                            continue
                        data = analyze(text); data["file_name"] = name
                        results.append(data)

            # PDF / DOCX FILE 
            else:
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(file.read());path = tmp.name

                if file.name.endswith(".pdf"):
                    text = pdf_text(path)
                elif file.name.endswith(".docx"):
                    text = docx_text(path)
                else:
                    continue
                data = analyze(text)
                data["file_name"] = file.name; results.append(data)
                os.remove(path)

# 9. Show results & create CSV
if results:
    st.success("Done ✓")
    
    df = pd.DataFrame(results)
    for col in df.columns:
        df[col] = df[col].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)

    csv_path = tempfile.NamedTemporaryFile(delete=False, suffix=".csv").name
    df.to_csv(csv_path, index=False)

    st.download_button(
        "🡻 Download Resume Intelligence CSV", open(csv_path, "rb"), "ResumeLens.csv",mime="text/csv")
else:
    st.info("🗁 Upload resumes to begin")

## 10.Footer
st.markdown("---"); st.markdown("<p style='text-align:center;color:black;'>" 
"© 2025 ResumeLens • AI Resume Intelligence | Built with Streamlit + Gemini</p>",unsafe_allow_html=True)

