import io
import json
import os

import streamlit as st
from google import genai
from google.genai import types
from docx import Document


APP_TITLE = "Resume ATS Analyzer"
MODEL_NAME = "gemini-3.6-flash"


# -----------------------------
# API KEY
# -----------------------------

def get_api_key():
    """Get Gemini API key from Streamlit Secrets or environment variables."""
    try:
        key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        key = None

    return key or os.getenv("GEMINI_API_KEY")


# -----------------------------
# DOCX TEXT EXTRACTION
# -----------------------------

def extract_docx_text(file_bytes):
    """Extract text from a DOCX resume."""
    document = Document(io.BytesIO(file_bytes))

    parts = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            parts.append(text)

    for table in document.tables:
        for row in table.rows:
            cells = []

            for cell in row.cells:
                text = cell.text.strip()

                if text:
                    cells.append(text)

            if cells:
                parts.append(" | ".join(cells))

    return "\n".join(parts)


# -----------------------------
# RESUME ANALYSIS
# -----------------------------

def analyze_resume(uploaded_file, job_description, api_key):

    client = genai.Client(api_key=api_key)

    file_bytes = uploaded_file.getvalue()
    mime_type = uploaded_file.type or "application/octet-stream"

    prompt = """
You are an expert ATS resume analyzer and career-document reviewer.

Analyze the candidate's resume against the provided job description.

IMPORTANT:
- This is an estimated ATS-readiness score, NOT an official score from any
  commercial ATS.
- Do not invent experience, skills, education, certifications, employers,
  dates, achievements, or technologies.
- Only identify a skill as "matched" if it is actually present in the resume.
- Missing keywords should come from the job description.
- Recommendations must be realistic and based on the provided resume.
- Do not tell the candidate to add a skill they do not actually have.
- If a job requirement is not supported by the resume, describe it as a gap.
- Evaluate ATS formatting risks such as columns, tables, graphics, icons,
  unusual symbols, headers/footers, and complicated layouts when they are
  visible or inferable from the document.
- Give practical, specific improvements instead of generic advice.

Analyze these areas:

1. Overall ATS readiness
2. Job-description keyword match
3. Skills match
4. Experience relevance
5. Resume structure
6. Formatting and ATS readability
7. Quantifiable achievements
8. Education and certifications
9. Professional summary
10. Grammar and consistency

Return ONLY valid JSON matching the requested schema.
"""

    schema = {
        "type": "OBJECT",
        "properties": {
            "ats_score": {
                "type": "INTEGER"
            },
            "keyword_match_score": {
                "type": "INTEGER"
            },
            "skills_match_score": {
                "type": "INTEGER"
            },
            "experience_score": {
                "type": "INTEGER"
            },
            "formatting_score": {
                "type": "INTEGER"
            },
            "structure_score": {
                "type": "INTEGER"
            },
            "summary": {
                "type": "STRING"
            },
            "matched_keywords": {
                "type": "ARRAY",
                "items": {
                    "type": "STRING"
                }
            },
            "missing_keywords": {
                "type": "ARRAY",
                "items": {
                    "type": "STRING"
                }
            },
            "strengths": {
                "type": "ARRAY",
                "items": {
                    "type": "STRING"
                }
            },
            "ats_risks": {
                "type": "ARRAY",
                "items": {
                    "type": "STRING"
                }
            },
            "improvements": {
                "type": "ARRAY",
                "items": {
                    "type": "STRING"
                }
            },
            "priority_actions": {
                "type": "ARRAY",
                "items": {
                    "type": "STRING"
                }
            }
        },
        "required": [
            "ats_score",
            "keyword_match_score",
            "skills_match_score",
            "experience_score",
            "formatting_score",
            "structure_score",
            "summary",
            "matched_keywords",
            "missing_keywords",
            "strengths",
            "ats_risks",
            "improvements",
            "priority_actions"
        ]
    }

    config = types.GenerateContentConfig(
        temperature=0.2,
        response_mime_type="application/json",
        response_schema=schema
    )

    # PDF
    if mime_type == "application/pdf":

        uploaded = client.files.upload(
            file=io.BytesIO(file_bytes),
            config={"mime_type": "application/pdf"}
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                prompt,
                f"\nJOB DESCRIPTION:\n{job_description}",
                uploaded
            ],
            config=config
        )

    # DOCX
    elif (
        mime_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):

        resume_text = extract_docx_text(file_bytes)

        if not resume_text.strip():
            raise ValueError(
                "The DOCX file does not contain readable text."
            )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                prompt,
                f"\nJOB DESCRIPTION:\n{job_description}",
                f"\nRESUME:\n{resume_text}"
            ],
            config=config
        )

    else:
        raise ValueError(
            "Unsupported file type. Please upload a PDF or DOCX."
        )

    if not response.text:
        raise ValueError(
            "Gemini returned an empty response."
        )

    return json.loads(response.text)


# -----------------------------
# SCORE LABEL
# -----------------------------

def score_label(score):

    if score >= 85:
        return "Strong ATS readiness"

    if score >= 70:
        return "Good ATS readiness"

    if score >= 50:
        return "Needs improvement"

    return "Major improvements recommended"


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📄",
    layout="wide"
)


# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.title("📄 Resume ATS")

    st.caption("AI-powered resume analysis")

    st.divider()

    st.subheader("⚙️ Settings")

    st.write("**AI Model**")
    st.info("Gemini Flash")

    st.write("**Supported Formats**")
    st.write("📄 PDF")
    st.write("📝 DOCX")

    st.divider()

    st.subheader("ℹ️ About")

    st.write(
        "Analyze your resume against a specific job description "
        "and identify ATS-related improvements."
    )

    st.divider()

    st.caption(
        "ATS score is an AI-generated estimate and may differ "
        "from scores produced by individual ATS platforms."
    )


# -----------------------------
# MAIN PAGE
# -----------------------------

st.title("📄 Resume ATS Analyzer")

st.write(
    "Check how well your resume matches a job description "
    "and discover specific improvements."
)


# -----------------------------
# RESUME UPLOAD
# -----------------------------

st.subheader("📎 Upload Your Resume")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf", "docx"],
    help="Upload a PDF or DOCX resume."
)

if uploaded_file:

    st.success(
        f"Resume uploaded: {uploaded_file.name}"
    )


# -----------------------------
# JOB DESCRIPTION
# -----------------------------

st.subheader("💼 Job Description")

job_description = st.text_area(
    "Paste the job description here",
    placeholder=(
        "Paste the complete job description here...\n\n"
        "Example:\n"
        "We are looking for a Python Developer with experience "
        "in Python, FastAPI, REST APIs, SQL, Git and Docker."
    ),
    height=220
)


# -----------------------------
# ANALYZE BUTTON
# -----------------------------

if uploaded_file and job_description.strip():

    analyze_button = st.button(
        "🔍 Analyze Resume",
        type="primary",
        use_container_width=True
    )

    if analyze_button:

        api_key = get_api_key()

        if not api_key:

            st.error(
                "Gemini API key was not found. "
                "Please add GEMINI_API_KEY in Streamlit Secrets."
            )

            st.stop()

        with st.spinner(
            "Analyzing your resume with Gemini Flash..."
        ):

            try:

                result = analyze_resume(
                    uploaded_file,
                    job_description,
                    api_key
                )

                score = max(
                    0,
                    min(100, int(result["ats_score"]))
                )

                st.divider()

                # -----------------------------
                # ATS SCORE
                # -----------------------------

                st.subheader("🎯 ATS Score")

                score_col1, score_col2 = st.columns(
                    [1, 2]
                )

                with score_col1:

                    st.metric(
                        "Estimated ATS Score",
                        f"{score}/100"
                    )

                with score_col2:

                    st.progress(score / 100)

                    st.write(
                        f"**{score_label(score)}**"
                    )

                st.write(
                    result["summary"]
                )

                # -----------------------------
                # CATEGORY SCORES
                # -----------------------------

                st.subheader("📊 Resume Analysis")

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Keyword Match",
                        f"{result['keyword_match_score']}/100"
                    )

                    st.metric(
                        "Skills Match",
                        f"{result['skills_match_score']}/100"
                    )

                with col2:

                    st.metric(
                        "Experience",
                        f"{result['experience_score']}/100"
                    )

                    st.metric(
                        "Formatting",
                        f"{result['formatting_score']}/100"
                    )

                with col3:

                    st.metric(
                        "Structure",
                        f"{result['structure_score']}/100"
                    )

                # -----------------------------
                # KEYWORDS
                # -----------------------------

                st.divider()

                keyword_col1, keyword_col2 = st.columns(2)

                with keyword_col1:

                    st.subheader("✅ Matched Keywords")

                    if result["matched_keywords"]:

                        for keyword in result["matched_keywords"]:

                            st.write(
                                f"✓ {keyword}"
                            )

                    else:

                        st.write(
                            "No strong keyword matches were identified."
                        )

                with keyword_col2:

                    st.subheader("⚠️ Missing Keywords")

                    if result["missing_keywords"]:

                        for keyword in result["missing_keywords"]:

                            st.write(
                                f"• {keyword}"
                            )

                    else:

                        st.write(
                            "No major missing keywords identified."
                        )

                # -----------------------------
                # STRENGTHS / RISKS
                # -----------------------------

                st.divider()

                left_col, right_col = st.columns(2)

                with left_col:

                    st.subheader("✅ Resume Strengths")

                    for item in result["strengths"]:

                        st.write(
                            f"• {item}"
                        )

                with right_col:

                    st.subheader("⚠️ ATS Risks")

                    for item in result["ats_risks"]:

                        st.write(
                            f"• {item}"
                        )

                # -----------------------------
                # IMPROVEMENTS
                # -----------------------------

                st.divider()

                st.subheader("🛠️ Recommended Improvements")

                for index, item in enumerate(
                    result["improvements"],
                    start=1
                ):

                    st.write(
                        f"**{index}.** {item}"
                    )

                # -----------------------------
                # PRIORITY ACTIONS
                # -----------------------------

                st.divider()

                st.subheader("🎯 Priority Actions")

                for index, item in enumerate(
                    result["priority_actions"],
                    start=1
                ):

                    st.write(
                        f"**{index}.** {item}"
                    )

            except json.JSONDecodeError:

                st.error(
                    "Gemini returned an invalid analysis. "
                    "Please try again."
                )

            except Exception as exc:

                st.error(
                    f"Analysis failed: {exc}"
                )

else:

    if uploaded_file and not job_description.strip():

        st.warning(
            "Please paste the job description before analyzing."
        )

    else:

        st.info(
            "Upload your resume and paste a job description "
            "to begin the analysis."
        )
