# 📄 Resume ATS Analyzer

An AI-powered **Resume ATS Analyzer** built with **Streamlit** and **Google Gemini Flash**. Upload your resume, provide a target job description, and get an estimated ATS-readiness score along with keyword matching, ATS risks, strengths, and actionable improvements.

## 🚀 Live Demo

**Streamlit App:** Add your deployed Streamlit URL here

---

## ✨ Features

* 📄 Upload resumes in **PDF** or **DOCX** format
* 💼 Paste a target **job description**
* 🤖 Analyze resumes using **Google Gemini Flash**
* 🎯 Generate an estimated **ATS score out of 100**
* 📊 View category-based resume scores
* 🔎 Identify **matched keywords**
* ⚠️ Identify **missing job-description keywords**
* ✅ Highlight resume strengths
* 🚨 Detect potential ATS formatting risks
* 🛠️ Get specific resume improvement suggestions
* 🎯 Receive prioritized actions for improving the resume
* ⚙️ Simple settings and information sidebar
* 🔐 Gemini API key stored securely using **Streamlit Secrets**

---

## 🛠️ Tech Stack

| Technology                | Purpose                         |
| ------------------------- | ------------------------------- |
| Python                    | Application logic               |
| Streamlit                 | Web application UI              |
| Google Gemini Flash       | AI-powered resume analysis      |
| Google GenAI SDK          | Gemini API integration          |
| python-docx               | DOCX text extraction            |
| GitHub                    | Version control and source code |
| Streamlit Community Cloud | Deployment                      |

---

## 📁 Project Structure

```text
Resume-ATS-Analyzer/
│
├── app.py
├── requirements.txt
└── README.md
```

### `app.py`

Contains the complete Streamlit application, including:

* Resume upload
* PDF/DOCX processing
* Job description input
* Gemini API integration
* ATS analysis
* Keyword matching
* Score calculation
* Results display

### `requirements.txt`

Contains the Python dependencies required to run the application.

---

## ⚙️ How It Works

```text
User uploads resume
        ↓
User enters job description
        ↓
Resume + job description sent to Gemini
        ↓
Gemini analyzes resume
        ↓
ATS metrics and keyword matching
        ↓
Score + improvements displayed
```

---

## 📊 What the App Analyzes

The application evaluates several aspects of the resume:

### 🎯 ATS Readiness

Provides an estimated score from **0–100** based on the resume's compatibility with common ATS-friendly practices.

### 🔎 Keyword Match

Compares keywords and requirements from the job description against the resume.

### 🧠 Skills Match

Identifies relevant skills present in the resume and highlights skills mentioned in the job description that are not found in the resume.

### 💼 Experience Relevance

Evaluates how closely the candidate's documented experience relates to the target position.

### 📄 Formatting

Looks for potential ATS parsing problems such as:

* Complex layouts
* Tables
* Graphics
* Icons
* Unusual symbols
* Difficult-to-parse formatting

### 📝 Resume Structure

Reviews the organization and clarity of sections such as:

* Summary
* Experience
* Skills
* Education
* Certifications

---

## 🔐 API Key Setup

The Gemini API key should **not** be placed directly inside the source code or committed to GitHub.

For Streamlit deployment, add the key through **Streamlit Secrets**.

Use:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

The application reads the key using:

```python
st.secrets.get("GEMINI_API_KEY")
```

---

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

### 2. Open the project folder

```bash
cd YOUR_REPOSITORY
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create:

```text
.streamlit/
└── secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## ☁️ Deployment

This project can be deployed using **Streamlit Community Cloud**.

### Steps

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub account.
4. Select your repository.
5. Select the `main` branch.
6. Set `app.py` as the main file.
7. Add `GEMINI_API_KEY` under Streamlit Secrets.
8. Deploy the application.

---

## ⚠️ Important Note About the ATS Score

The score provided by this application is an **AI-generated ATS-readiness estimate**.

It is not an official score from a specific Applicant Tracking System.

Different ATS platforms can use different parsing, ranking, and screening methods. The purpose of this application is to provide practical guidance for improving resume structure, keyword alignment, readability, and job relevance.

---

## 🔒 Privacy

Resumes may contain sensitive personal information.

Users should avoid uploading information they do not want processed by an external AI service. Resume content is sent to the configured Gemini API for analysis.

---

## 🔮 Future Improvements

Possible future features include:

* [ ] Resume rewriting suggestions
* [ ] Downloadable analysis report
* [ ] Resume section-by-section analysis
* [ ] Job-description keyword heatmap
* [ ] Multiple resume comparison
* [ ] Resume version tracking
* [ ] LinkedIn profile optimization
* [ ] Support for additional document formats
* [ ] More detailed ATS formatting analysis
* [ ] Custom resume templates

---

## 👩‍💻 Author

**Kehkshan Hafiza**

Built as an AI-powered resume optimization project using Python, Streamlit, and Google Gemini.

---

## ⭐ If You Find This Project Useful

Consider giving the repository a ⭐ on GitHub!
