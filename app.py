import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier


# ---------- Professional UI Theme ----------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #141E30, #243B55);
    font-family: 'Segoe UI', sans-serif;
}

.main-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(10px);
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

.stButton>button {
    background: linear-gradient(90deg, #00C9FF, #92FE9D);
    color: black;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-weight: 600;
    border: none;
}

h1, h2, h3 {
    color: #ffffff;
    text-align: center;
}

p, label, span {
    color: #e0e0e0;
}

</style>
""", unsafe_allow_html=True)


# ---------- Title ----------
st.markdown("""
<div class="main-card">
<h1>🎓 Job Readiness Prediction System</h1>
<p style="text-align:center;">Analyze Skills • Improve Yourself • Get Placed</p>
</div>
""", unsafe_allow_html=True)


# ---------- Load Dataset ----------
data = pd.read_csv("placement_data.csv")

X = data.drop("Job_Level", axis=1)
y = data["Job_Level"]

model = RandomForestClassifier(random_state=42)
model.fit(X, y)


# ---------- Sidebar ----------
st.sidebar.header("Enter Your Details")

cgpa = st.sidebar.slider("CGPA", 5.0, 10.0, 7.0)
apt = st.sidebar.slider("Aptitude (1-10)", 1, 10, 6)
projects = st.sidebar.slider("Projects", 0, 5, 1)
attendance = st.sidebar.slider("Attendance (%)", 50, 100, 80)
internship = st.sidebar.selectbox("Internship", ["No", "Yes"])

st.sidebar.subheader("Programming Skills (0-10)")

python_skill = st.sidebar.slider("Python", 0, 10, 0)
java_skill = st.sidebar.slider("Java", 0, 10, 0)
c_skill = st.sidebar.slider("C", 0, 10, 0)
cpp_skill = st.sidebar.slider("C++", 0, 10, 0)
javascript_skill = st.sidebar.slider("JavaScript", 0, 10, 0)

internship_val = 1 if internship == "Yes" else 0


# ---------- Prediction ----------
if st.button("Check My Level"):

    # Calculate Dynamic Skill Average
    skills = [python_skill, java_skill, c_skill, cpp_skill, javascript_skill]
    selected_skills = [s for s in skills if s > 0]

    if len(selected_skills) > 0:
        avg_skill = sum(selected_skills) / len(selected_skills)
    else:
        avg_skill = 0


    # Create DataFrame for Prediction (No Warning)
    user_df = pd.DataFrame([{
        "CGPA": cgpa,
        "Tech_Skill": avg_skill,
        "Aptitude": apt,
        "Projects": projects,
        "Attendance": attendance,
        "Internship": internship_val
    }])

    result = model.predict(user_df)


    # ---------- Result Card ----------
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    if result[0] == 0:
        st.error("❌ Not Ready for Interviews")
    elif result[0] == 1:
        st.warning("⚠️ Moderately Ready")
    else:
        st.success("✅ Job Ready")


    # ---------- Profile ----------
    st.write("## 📊 Your Profile")

    st.write("🎓 CGPA:", cgpa)
    st.write("📚 Aptitude:", apt)
    st.write("📂 Projects:", projects)
    st.write("📅 Attendance:", attendance, "%")
    st.write("💼 Internship:", internship)

    st.write("### 💻 Programming Skills")

    st.write("Python:", python_skill)
    st.write("Java:", java_skill)
    st.write("C:", c_skill)
    st.write("C++:", cpp_skill)
    st.write("JavaScript:", javascript_skill)

    st.write("⭐ Average Skill:", round(avg_skill, 2))


    # ---------- Radar Chart ----------
    st.write("## 📈 Skill Radar Chart")

    labels = ["Python", "Java", "C", "C++", "JavaScript"]
    values = [python_skill, java_skill, c_skill, cpp_skill, javascript_skill]

    if sum(values) > 0:

        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)

        values = np.concatenate((values, [values[0]]))
        angles = np.concatenate((angles, [angles[0]]))

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        ax.plot(angles, values, marker='o')
        ax.fill(angles, values, alpha=0.3)

        ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
        ax.set_ylim(0, 10)

        ax.set_title("Programming Skill Analysis", pad=20)

        st.pyplot(fig)

    else:
        st.info("Please enter at least one skill to view chart.")


    # ---------- Recommendation System ----------
    st.write("## 📚 Personalized Improvement Plan")

    rec = []

    if cgpa < 7:
        rec.append("📌 Improve core subjects to increase CGPA above 7.5")

    if apt < 6:
        rec.append("📌 Practice aptitude daily (Quant + Reasoning + Verbal)")

    if projects < 2:
        rec.append("📌 Build more real-world projects (Web / ML / Apps)")

    if attendance < 75:
        rec.append("📌 Improve attendance for placement eligibility")

    if internship_val == 0:
        rec.append("📌 Try to get an internship for industry exposure")


    # Skill-based (only selected skills)
    if python_skill > 0 and python_skill < 6:
        rec.append("📌 Improve Python (DSA, OOP, Pandas, ML basics)")

    if java_skill > 0 and java_skill < 6:
        rec.append("📌 Strengthen Java (OOP, DSA, Collections)")

    if c_skill > 0 and c_skill < 6:
        rec.append("📌 Revise C fundamentals")

    if cpp_skill > 0 and cpp_skill < 6:
        rec.append("📌 Practice C++ with STL and DSA")

    if javascript_skill > 0 and javascript_skill < 6:
        rec.append("📌 Learn JavaScript (DOM, React basics)")


    if len(rec) == 0:
        st.success("🎉 Excellent! You are well prepared. Keep practicing!")
    else:
        for r in rec:
            st.write(r)

    st.markdown("</div>", unsafe_allow_html=True)


# ---------- Footer ----------
st.write("Developed by Machavarapu Abhiram 🚀")
