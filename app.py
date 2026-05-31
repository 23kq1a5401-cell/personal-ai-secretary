import streamlit as st
import json
from datetime import date, datetime

from database import (
    add_task,
    get_tasks,
    update_task,
    update_status,
    delete_task
)

from ai_assistant import ask_ai


# ======================
# PAGE CONFIG
# ======================
st.set_page_config(page_title="AI Secretary PRO", layout="centered")


# ======================
# SESSION STATE
# ======================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = []


# ======================
# LOGIN PAGE
# ======================
if not st.session_state.logged_in:

    st.title("🔐 AI Secretary Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user.strip() == "admin" and pwd.strip() == "admin":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Invalid Login")

    st.stop()   # VERY IMPORTANT


# ======================
# LOGOUT BUTTON
# ======================
if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()


# ======================
# MAIN APP
# ======================
st.title("🤖 Personal AI Secretary PRO MAX")


# ======================
# ADD TASK
# ======================
st.subheader("➕ Add Task")

task = st.text_input("Task Name")
priority = st.selectbox("Priority", ["High", "Medium", "Low"])
due_date = st.date_input("Due Date")

if st.button("Add Task"):
    if task.strip():
        add_task(task, priority, str(due_date))
        st.success("Task Added")
        st.rerun()
    else:
        st.warning("Enter task name")


# ======================
# TASK DASHBOARD
# ======================
st.subheader("📋 Task Dashboard")

tasks = get_tasks()
today = date.today()

search = st.text_input("🔍 Search Task")

total = len(tasks)
completed = len([t for t in tasks if t[4] == "Completed"])
pending = len([t for t in tasks if t[4] == "Pending"])

col1, col2, col3 = st.columns(3)
col1.metric("Total", total)
col2.metric("Completed", completed)
col3.metric("Pending", pending)


for t in tasks:

    task_id = t[0]
    task_name = t[1]
    task_priority = t[2]
    task_due = t[3]
    task_status = t[4]

    if search and search.lower() not in task_name.lower():
        continue

    try:
        due = datetime.strptime(task_due, "%Y-%m-%d").date()
    except:
        due = today

    st.write("---")

    if task_status == "Completed":
        st.success(f"✅ {task_name}")
    elif due < today:
        st.error(f"🚨 OVERDUE | {task_name}")
    elif due == today:
        st.warning(f"📅 DUE TODAY | {task_name}")
    else:
        st.info(task_name)

    st.write(f"Priority: {task_priority} | Due: {task_due} | Status: {task_status}")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Complete", key=f"c{task_id}"):
            update_status(task_id, "Completed")
            st.rerun()

    with col2:
        if st.button("Delete", key=f"d{task_id}"):
            delete_task(task_id)
            st.rerun()

    with col3:
        edited = st.text_input("", value=task_name, key=f"e{task_id}")
        if st.button("Update", key=f"u{task_id}"):
            update_task(task_id, edited)
            st.rerun()


# ======================
# AI CHAT (CHATGPT STYLE)
# ======================
st.write("---")
st.subheader("💬 AI Chat")

# show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# input bar
user_input = st.chat_input("Message AI Secretary...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    reply = ask_ai(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.write(reply)