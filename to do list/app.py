import streamlit as st
import json
import os

# -------------------------------
# Page Config & Theme
# -------------------------------
st.set_page_config(
    page_title="TaskMind AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.task-card {
    padding: 15px;
    border-radius: 10px;
    background-color: #1e1e1e;
    margin-bottom: 10px;
}
.small-text {
    font-size: 13px;
    color: #bbbbbb;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 TaskMind AI")
st.caption("An Agentic AI Task Planner with Smart Prioritization & Analytics")

USERS_FILE = "users.json"

# -------------------------------
# Persistence Helpers
# -------------------------------
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def task_file(user):
    return f"tasks_{user}.json"

def load_tasks(user):
    if os.path.exists(task_file(user)):
        with open(task_file(user), "r") as f:
            return json.load(f)
    return []

def save_tasks(user, tasks):
    with open(task_file(user), "w") as f:
        json.dump(tasks, f, indent=4)

# -------------------------------
# Agent Logic
# -------------------------------
def category_agent(task):
    t = task.lower()
    if "exam" in t or "study" in t:
        return "Education"
    elif "project" in t or "assignment" in t:
        return "Work"
    elif "gym" in t or "health" in t:
        return "Health"
    return "General"

def breakdown_agent(task):
    t = task.lower()
    if "exam" in t:
        return ["Revise syllabus", "Practice questions", "Mock test"]
    elif "project" in t:
        return ["Plan solution", "Develop", "Test", "Submit"]
    else:
        return ["Break task", "Execute", "Review"]

def progress_calc(subtasks):
    if not subtasks:
        return 0
    done = sum(1 for s in subtasks if s["done"])
    return int((done / len(subtasks)) * 100)

def auto_priority(progress):
    if progress == 100:
        return "Completed"
    elif progress < 30:
        return "High"
    elif progress < 70:
        return "Medium"
    else:
        return "Low"

# -------------------------------
# Session
# -------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

# -------------------------------
# LOGIN / REGISTER
# -------------------------------
if st.session_state.user is None:
    st.subheader("🔐 Login to TaskMind AI")

    tab1, tab2 = st.tabs(["Login", "Register"])
    users = load_users()

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            if u in users and users[u] == p:
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        nu = st.text_input("New Username")
        np = st.text_input("New Password", type="password")
        if st.button("Register"):
            if nu in users:
                st.warning("User already exists")
            else:
                users[nu] = np
                save_users(users)
                st.success("Registered successfully! Login now.")

    st.stop()

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("🎛 Control Panel")
st.sidebar.markdown(f"👤 **User:** `{st.session_state.user}`")

if st.sidebar.button("🚪 Logout"):
    st.session_state.user = None
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info(
    "🧠 **TaskMind AI**\n\n"
    "• Agentic Planning\n"
    "• Smart Priority\n"
    "• Progress Tracking\n"
    "• Persistent Storage"
)

# -------------------------------
# MAIN CONTENT
# -------------------------------
tasks = load_tasks(st.session_state.user)

# Add Task
st.subheader("➕ Add a New Task")
task_input = st.text_input("Describe your task in natural language")

if st.button("Add Task"):
    if task_input.strip():
        tasks.append({
            "task": task_input,
            "category": category_agent(task_input),
            "priority": "High",
            "completed": False,
            "subtasks": [
                {"title": s, "done": False}
                for s in breakdown_agent(task_input)
            ]
        })
        save_tasks(st.session_state.user, tasks)
        st.success("Task added successfully")
    else:
        st.warning("Task cannot be empty")

# Dashboard
st.subheader("📊 Productivity Overview")

total = len(tasks)
completed = sum(1 for t in tasks if t["completed"])
productivity = int((completed / total) * 100) if total else 0

c1, c2, c3 = st.columns(3)
c1.metric("📌 Total Tasks", total)
c2.metric("✅ Completed", completed)
c3.metric("📈 Productivity", f"{productivity}%")

st.progress(productivity)

# Task List
st.subheader("📋 Your Tasks")

if not tasks:
    st.info("No tasks yet. Add one above 👆")

for i, task in enumerate(tasks):
    progress = progress_calc(task["subtasks"])
    task["priority"] = auto_priority(progress)
    task["completed"] = progress == 100

    with st.expander(f"📝 {task['task']} ({task['priority']})"):
        st.markdown(
            f"<div class='task-card'>"
            f"<span class='small-text'>Category: {task['category']}</span>",
            unsafe_allow_html=True
        )

        st.progress(progress)
        st.caption(f"Progress: {progress}%")

        for si, sub in enumerate(task["subtasks"]):
            sub["done"] = st.checkbox(
                sub["title"],
                value=sub["done"],
                key=f"{i}_{si}"
            )

        if st.button("❌ Delete Task", key=f"del_{i}"):
            tasks.pop(i)
            save_tasks(st.session_state.user, tasks)
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    save_tasks(st.session_state.user, tasks)
