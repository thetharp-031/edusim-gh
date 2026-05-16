import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import json
from datetime import datetime

st.set_page_config(page_title="EduSim GH", page_icon="🧪", layout="wide")

# Theme
if "theme" not in st.session_state:
    st.session_state.theme = "light"

theme = st.sidebar.toggle("🌙 Dark Mode", value=st.session_state.theme == "dark")
st.session_state.theme = "dark" if theme else "light"

# Main Title
st.title("🧪 EduSim GH")
st.subheader("Advanced Interactive Science Simulator for African Classrooms")
st.caption("Built by Isaac Thetharp (thetharp-031) | Open Source for Ghana & Africa")

# Sidebar
st.sidebar.title("📚 Navigation")
page = st.sidebar.radio("Go to", 
    ["Home", "Chemistry Lab", "Biology Lab", "Physics Lab", 
     "Lesson Planner", "Progress Tracker", "Quizzes", "About"])

# ====================== SESSION STATE ======================
if "lesson_plans" not in st.session_state:
    st.session_state.lesson_plans = {}
if "progress" not in st.session_state:
    st.session_state.progress = {"lessons_completed": 0, "quizzes_passed": 0}

# ====================== HOME ======================
if page == "Home":
    st.write("### Welcome to EduSim GH 2.0")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Modules", "5+")
    with col2: st.metric("Lessons", "20+")
    with col3: st.metric("Students Reached", "Target: 10,000+")
    with col4: st.metric("Ghana Focused", "✅")

    st.info("**New in this version**: Save lesson plans, take quizzes, track progress, and export PDFs.")

# ====================== CHEMISTRY ======================
elif page == "Chemistry Lab":
    st.header("🧪 Chemistry Virtual Lab")
    exp = st.selectbox("Experiment", ["pH Scale Explorer", "Acid-Base Titration"])
    
    if exp == "pH Scale Explorer":
        ph = st.slider("pH Value", 0.0, 14.0, 7.0, 0.1)
        st.markdown(f"<h1 style='text-align:center; color:{'red' if ph<7 else 'blue' if ph>7 else 'green'}'>{ph}</h1>", unsafe_allow_html=True)
        st.write("**Type:**", "Acidic" if ph < 7 else "Neutral" if ph == 7 else "Basic")

# ====================== BIOLOGY ======================
elif page == "Biology Lab":
    st.header("🧬 Biology Virtual Lab")
    light = st.slider("Light Intensity (%)", 0, 100, 70)
    water = st.slider("Water (%)", 0, 100, 65)
    nutrients = st.slider("Nutrients (%)", 0, 100, 80)
    
    growth_rate = (light * water * nutrients) / 10000
    st.progress(growth_rate)
    st.success(f"**Plant Growth Rate: {growth_rate:.1f}% per day**")
    st.line_chart(pd.DataFrame({"Day": range(10), "Growth": [growth_rate * i for i in range(10)]}))

# ====================== LESSON PLANNER ======================
elif page == "Lesson Planner":
    st.header("📝 Smart Lesson Planner")
    
    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("Topic", "Photosynthesis")
        grade = st.selectbox("Grade", ["JHS 1", "JHS 2", "SHS 1", "SHS 2"])
    with col2:
        duration = st.number_input("Duration (minutes)", 30, 120, 60)
    
    if st.button("Generate & Save Lesson Plan"):
        plan = {
            "topic": topic,
            "grade": grade,
            "duration": duration,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "objectives": ["Understand key concepts", "Use virtual lab", "Apply knowledge"],
            "activities": "Use EduSim virtual lab + discussion"
        }
        st.session_state.lesson_plans[topic] = plan
        st.success("Lesson Plan Saved!")
        
        # PDF Export
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, f"Lesson Plan: {topic} ({grade})")
        c.drawString(100, 700, f"Date: {plan['date']}")
        c.drawString(100, 650, f"Duration: {duration} minutes")
        c.save()
        buffer.seek(0)
        
        st.download_button("📥 Download as PDF", buffer, f"{topic}_lesson.pdf", "application/pdf")

# ====================== PROGRESS TRACKER ======================
elif page == "Progress Tracker":
    st.header("📊 My Learning Progress")
    st.metric("Lessons Completed", st.session_state.progress["lessons_completed"])
    st.metric("Quizzes Passed", st.session_state.progress["quizzes_passed"])
    
    if st.button("Mark Lesson Complete"):
        st.session_state.progress["lessons_completed"] += 1
        st.success("Progress Updated!")

# ====================== QUIZZES ======================
elif page == "Quizzes":
    st.header("🧠 Science Quiz")
    q_topic = st.selectbox("Quiz Topic", ["Photosynthesis", "pH Scale"])
    
    if q_topic == "pH Scale":
        q1 = st.radio("What does pH 7 mean?", ["Acidic", "Neutral", "Basic"])
        if st.button("Submit Quiz"):
            if q1 == "Neutral":
                st.success("Correct! +1 point")
                st.session_state.progress["quizzes_passed"] += 1
            else:
                st.error("Wrong. Correct answer: Neutral")

# ====================== ABOUT ======================
else:
    st.header("About EduSim GH")
    st.write("Built by **Isaac Thetharp** from Ghana.")
    st.write("**Goal**: Make high-quality science education tools freely available.")
    st.markdown("**[Sponsor this Project](https://github.com/sponsors/thetharp-031)**")

st.markdown("---")
st.caption("© 2026 Isaac Thetharp | thetharp-031 | Support via GitHub Sponsors")
