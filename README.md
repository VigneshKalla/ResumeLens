# 📄 ResumeLens – AI Resume Analyzer

ResumeLens is an **AI-powered resume intelligence system** that automatically reads resumes in **PDF, DOCX, or ZIP format**, extracts meaningful information using **Generative AI**, and exports the results into a **structured CSV file** for easy review and analysis.

This project is designed to solve the real-world problem of **manual resume screening**, which is time-consuming, inconsistent, and error-prone.

---

## 🚀 What ResumeLens Does

* Accepts resumes in **PDF, DOCX**, or **ZIP (multiple resumes)**
* Extracts resume text automatically
* Uses **Gemini LLM + LangChain structured output** to understand resumes
* Extracts key information such as:

  * Name, email, phone
  * Summary & experience
  * Skills & technologies
  * Projects & certifications
  * Professional links (LinkedIn, GitHub, portfolio, etc.)
  * ATS keywords and score
* Converts all extracted data into a **CSV file** using Pandas
* Provides a clean **Streamlit UI** with download support

---

## 🧠 How It Works (Step-by-Step)

1️⃣ **Upload resumes**
Users upload resumes as PDF, DOCX, or a ZIP containing multiple resumes.

2️⃣ **Text extraction**

* PDFs → extracted using **PyMuPDF (fitz)**
* DOCX → extracted using **python-docx**

3️⃣ **AI-based understanding**
The extracted text is sent to **Google Gemini (gemini-2.5-flash)** via **LangChain**, which converts unstructured text into **structured resume data** using a predefined schema.

4️⃣ **Data aggregation**
All resume outputs are collected and stored in memory using **Streamlit session state**, preventing unnecessary reprocessing.

5️⃣ **CSV pipeline**
The structured data is converted into a Pandas DataFrame and exported using **`pd.to_csv()`**.

6️⃣ **Download & reuse**
Users can download the CSV file instantly and upload new resumes when needed.

---

## 🛠️ Technologies & Libraries Used

### 🔹 Core Technologies

* **Python**
* **Streamlit** – Web UI and file handling
* **Google Gemini (LLM)** – Resume understanding
* **LangChain** – Structured output enforcement

### 🔹 Data & File Processing

* **Pandas** – CSV pipeline (`pd.to_csv`)
* **PyMuPDF (fitz)** – PDF text extraction
* **python-docx** – DOCX file parsing
* **zipfile & tempfile** – ZIP handling and safe file processing

### 🔹 Environment & Utilities

* **python-dotenv** – Secure API key management
* **TypedDict & Annotated** – Schema-based data extraction

---
## ⚙️ Installation & Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file:

```env
Gemini=YOUR_GEMINI_API_KEY
```

### 3. Run the application

```bash
streamlit run app.py
```

---

## 📊 Output Example

The generated CSV file includes columns like:

* fullname
* email
* experience
* skills
* projects
* certifications
* links
* role_fit
* ats_score

This makes the data **ATS-ready** and easy to filter or analyze.

---

## 🎯 Why ResumeLens Is Useful

* Saves **hours of manual resume screening**
* Produces **consistent, structured resume data**
* Suitable for **HR teams, recruiters, and data analysis**
* Demonstrates **real-world GenAI + LLM application**
* Portfolio-ready project for **Data Analyst / AI Engineer roles**

---

## 🔮 Future Enhancements

* Resume ↔ Job Description matching
* Skill gap analysis
* Resume ranking dashboards
* Export to Excel / Database
* Vector search using embeddings (RAG)
* Multi-user authentication

---

## 🙌 Acknowledgements

Built as part of hands-on learning and mentorship at **Innomatics Research Labs**, with guidance from **Saxon K Sha Sir** and **Lakshmi Vangapandhu Mam**.

---

## 📌 Tags

`#AI #GenerativeAI #LangChain #Streamlit #ResumeParsing #ATS #HRTech #Python`



