import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import fitz
import docx


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Job Readiness Prediction System",
    page_icon="💼",
    layout="wide"
)


# ---------------- THEME ----------------
st.markdown("""
<style>

.block-container {
    padding: 1.5rem 2.5rem;
}

.stApp {
    background: linear-gradient(180deg, #000000, #111111);
    font-family: 'Segoe UI', Arial, sans-serif;
}

header {
    background: #000000 !important;
    border-bottom: 4px solid #FFD700;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #000000;
    border-right: 4px solid #FFD700;
}

section[data-testid="stSidebar"] * {
    color: #FFD700 !important;
}

/* Cards */
.card {
    background: #0F0F0F !important;
    padding: 28px;
    border-radius: 15px;
    border: 3px solid #FFD700;
    box-shadow: 0 0 15px rgba(255,215,0,0.3);
    margin-bottom: 25px;
}

/* Header Card */
.header-card {
    background: #000000 !important;
    padding: 40px;
    border-radius: 18px;
    border: 4px solid #FFD700;
    box-shadow: 0 0 25px rgba(255,215,0,0.5);
    margin-bottom: 35px;
}

/* Title */
.main-title {
    font-size: 70px;
    font-weight: 900;
    color: #FFD700;
    text-align: center;
}

.sub-title {
    text-align: center;
    color: #FFFFFF;
    font-size: 22px;
}

.tag-line {
    text-align: center;
    color: #CCCCCC;
    font-size: 15px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #FFD700, #FFC107);
    color: #000000;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
    border: none;
    width: 100%;
}

/* Inputs */
input, select {
    border-radius: 6px !important;
    border: 1px solid #FFD700 !important;
    background: #111111 !important;
    color: #FFD700 !important;
}

/* Headings */
h2, h3 {
    color: #FFD700;
}

/* Text */
p, label, span {
    color: #FFFFFF;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown("""
<div class="header-card">

<div class="main-title">
JOB READINESS PREDICTION SYSTEM
</div>

<div class="sub-title">
AI-Based Career & Placement Analytics Portal
</div>

<div class="tag-line">
Skill Assessment • Resume Analysis • Career Guidance
</div>

</div>
""", unsafe_allow_html=True)


# ---------------- DATA ----------------
data = pd.read_csv("placement_data.csv")

X = data.drop("Job_Level", axis=1)
y = data["Job_Level"]

model = RandomForestClassifier(random_state=42)
model.fit(X, y)


# ---------------- SIDEBAR ----------------
st.sidebar.header("🎓 Student Profile")

name = st.sidebar.text_input("Student Name")

cgpa = st.sidebar.number_input("CGPA (Out of 10)", 0.0, 10.0, 7.0, 0.01)

apt = st.sidebar.slider("Aptitude (1-10)", 1, 10, 6)

projects = st.sidebar.slider("Projects", 0, 5, 1)

attendance = st.sidebar.slider("Attendance (%)", 50, 100, 80)

internship = st.sidebar.selectbox("Internship", ["No", "Yes"])
internship_val = 1 if internship == "Yes" else 0


st.sidebar.subheader("💻 Programming Skills")

python = st.sidebar.slider("Python", 0, 10, 0)
java = st.sidebar.slider("Java", 0, 10, 0)
c = st.sidebar.slider("C", 0, 10, 0)
cpp = st.sidebar.slider("C++", 0, 10, 0)
js = st.sidebar.slider("JavaScript", 0, 10, 0)


# ---------------- PREDICTION ----------------
if st.button("🚀 Evaluate Readiness"):

    skills = [python, java, c, cpp, js]
    active = [s for s in skills if s > 0]

    avg_skill = sum(active)/len(active) if active else 0


    user_df = pd.DataFrame([{
        "CGPA": cgpa,
        "Tech_Skill": avg_skill,
        "Aptitude": apt,
        "Projects": projects,
        "Attendance": attendance,
        "Internship": internship_val
    }])

    result = model.predict(user_df)


    # ---------------- RESULT ----------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if result[0] == 0:
        st.error("❌ Not Ready for Placement")
    elif result[0] == 1:
        st.warning("⚠️ Moderately Ready")
    else:
        st.success("✅ Job Ready")


    # ---------------- PROFILE ----------------
    st.subheader("📋 Student Profile")

    st.write("👤 Name:", name)
    st.write("🎓 CGPA:", cgpa)
    st.write("📚 Aptitude:", apt)
    st.write("📂 Projects:", projects)
    st.write("📅 Attendance:", attendance, "%")
    st.write("💼 Internship:", internship)


    # ---------------- SCORE ----------------
    st.subheader("📊 Readiness Score")

    score = int((cgpa*10 + avg_skill*10 + attendance)/3)
    score = min(score,100)

    st.progress(score)
    st.write("Score:", score,"/100")


    # ---------------- RADAR CHART ----------------
    st.subheader("📈 Skill Radar Chart")

    labels = ["Python","Java","C","C++","JS"]
    values = [python,java,c,cpp,js]

    if sum(values) > 0:

        angles = np.linspace(0,2*np.pi,len(labels),endpoint=False)

        values = np.concatenate((values,[values[0]]))
        angles = np.concatenate((angles,[angles[0]]))

        fig,ax = plt.subplots(figsize=(6,6),subplot_kw=dict(polar=True))

        ax.plot(angles,values,color="#FFD700",linewidth=2)
        ax.fill(angles,values,color="#FFD700",alpha=0.25)

        ax.set_thetagrids(angles[:-1]*180/np.pi,labels)
        ax.set_ylim(0,10)

        st.pyplot(fig)


    # ---------------- IMPROVEMENT ----------------
    st.subheader("📚 Personalized Improvement Plan")

    rec = []

    if cgpa < 7:
        rec.append("Improve CGPA above 7.5")

    if apt < 6:
        rec.append("Practice aptitude daily")

    if projects < 2:
        rec.append("Build more real-world projects")

    if internship_val == 0:
        rec.append("Apply for internships")

    if python > 0 and python < 6:
        rec.append("Strengthen Python skills")

    if java > 0 and java < 6:
        rec.append("Improve Java concepts")

    if c > 0 and c < 6:
        rec.append("Practice C programming")

    if cpp > 0 and cpp < 6:
        rec.append("Practice C++ STL & DSA")

    if js > 0 and js < 6:
        rec.append("Learn modern JavaScript")


    if rec:
        for r in rec:
            st.write("•", r)
    else:
        st.success("Excellent profile! Keep improving!")


    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- ATS RESUME ANALYZER ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.subheader("📄 ATS Resume Analyzer")

resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf","docx"])


def extract_text(file):

    text = ""

    if file.name.endswith(".pdf"):
        pdf = fitz.open(stream=file.read(), filetype="pdf")

        for page in pdf:
            text += page.get_text()

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)

        for p in doc.paragraphs:
            text += p.text

    return text.lower()


def ats_score(text):

    keywords = [
        "python","java","c","c++","machine learning","sql",
        "data","project","internship","github","api","cloud"
    ]

    found = sum([1 for k in keywords if k in text])

    score = int((found/len(keywords))*100)

    return score, keywords


if resume_file:

    text = extract_text(resume_file)

    score, keywords = ats_score(text)

    st.write("### ATS Score:", score,"/100")

    st.progress(score)


    if score >= 75:
        st.success("Excellent Resume")
    elif score >= 50:
        st.warning("Average Resume")
    else:
        st.error("Needs Improvement")


    st.write("### Missing Keywords:")

    for k in keywords:
        if k not in text:
            st.write("•", k)

st.markdown("</div>", unsafe_allow_html=True)


# ---------------- AI CAREER MENTOR ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.subheader("🤖 AI Career Mentor")

user_query = st.text_input("Ask your Career Question")


def career_bot(q):

    q = q.lower()

    if "python" in q:
        return "Focus on DSA, Pandas, Flask, and ML projects."

    if "job" in q:
        return "Improve skills, aptitude, and build strong projects."

    if "resume" in q:
        return "Add measurable achievements and relevant keywords."

    if "internship" in q:
        return "Apply on LinkedIn, Internshala, and company portals."

    if "c language" in q:
        return "Practice pointers, structures, and memory management."

    return "Stay consistent and improve your profile daily."


if user_query:
    st.info("🤖 AI Mentor: " + career_bot(user_query))

st.markdown("</div>", unsafe_allow_html=True)


# ---------------- FOOTER ----------------
st.markdown("""
<hr style="border:3px solid #FFD700;">

<p style="text-align:center; color:#FFD700; font-weight:500;">
Developed by Machavarapu Abhiram | Placement Intelligence System
</p>
""", unsafe_allow_html=True)