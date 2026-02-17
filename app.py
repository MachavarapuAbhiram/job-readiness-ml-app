import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# App title
st.title("🎓 Job Readiness Checker")

# Load dataset
data = pd.read_csv("placement_data.csv")

# Split data
X = data.drop("Job_Level", axis=1)
y = data["Job_Level"]

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Sidebar input
st.sidebar.header("Enter Your Details")

cgpa = st.sidebar.slider("CGPA", 5.0, 10.0, 7.0)
tech = st.sidebar.slider("Technical Skill (1-10)", 1, 10, 6)
apt = st.sidebar.slider("Aptitude (1-10)", 1, 10, 6)
projects = st.sidebar.slider("Projects", 0, 5, 1)
attendance = st.sidebar.slider("Attendance (%)", 50, 100, 80)
internship = st.sidebar.selectbox("Internship (0=No, 1=Yes)", [0, 1])

# Prediction
if st.button("Check My Level"):
    
    user = [[cgpa, tech, apt, projects, attendance, internship]]
    result = model.predict(user)

    if result[0] == 0:
        st.error("❌ Not Ready")
    elif result[0] == 1:
        st.warning("⚠️ Moderate Ready")
    else:
        st.success("✅ Job Ready")

st.write("Developed by Abhi 🚀")
