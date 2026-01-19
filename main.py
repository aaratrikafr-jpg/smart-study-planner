import streamlit as st
import os
import csv
from datetime import date, datetime
import random
stickers = {
    "Happy": [
        "https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif",  # cat
        "https://media.giphy.com/media/3oriO0O7FZq0W1z8J6/giphy.gif" # dog
    ],
    "Tired": [
        "https://media.giphy.com/media/l0HlNQ03J5JxX6lva/giphy.gif", # sleepy cat
        "https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif"  # panda
    ],
    "Stressed": [
        "https://media.giphy.com/media/13borq7Zo2kulO/giphy.gif",  # hug cat
        "https://media.giphy.com/media/5GoVLqeAOo6PK/giphy.gif"    # frog
    ]
 }
if "plans" not in st.session_state:
    st.session_state.plans = []
if "reminder" not in st.session_state:
    st.session_state.reminder = ""
if "schedule" not in st.session_state:
    st.session_state.schedule = []

def update_streak():
    today = date.today()

    if "last_study_date" not in st.session_state:
        st.session_state.last_study_date = today
        st.session_state.streak = 1
        return 1

    last_date = st.session_state.last_study_date

    if isinstance(last_date, str):
        last_date = date.fromisoformat(last_date)

    if last_date == today:
        return st.session_state.streak

    if (today - last_date).days == 1:
        st.session_state.streak += 1
    else:
        st.session_state.streak = 1

    st.session_state.last_study_date = today
    return st.session_state.streak


st.title("Smart Study Planner")

streak_count = update_streak()
st.write(f"🔥 Current streak: {streak_count}")
st.set_page_config(page_title="Smart Study Planner", layout="centered")

st.title("📚 Smart Study Planner")
st.write("Plan your study time smartly. Built by Aaratrika 💙")

st.subheader("Enter your details")

subject = st.text_input("Subject name")
hours = st.number_input("Hours you can study today", min_value=0, max_value=24)
goal = st.text_area("Your goal for this subject")

if st.button("Generate Study Plan"):
    if subject and hours > 0:
        st.success("✅ Your Study Plan")
        st.write(f"📌 Subject: *{subject}*")
        st.write(f"⏰ Study Time: *{hours} hours*")
        st.write("📝 Suggested Plan:")
        st.write(f"- Revise basics of {subject}")
        st.write(f"- Practice key problems for {hours//2} hours")
        st.write(f"- Review mistakes and summarize notes")
        st.write(f"🎯 Goal: {goal}")
    else:
        st.warning("Please enter subject and study hours.")
import streamlit as st

st.set_page_config(
    page_title="Smart Study Planner",
    page_icon="📚",
    layout="centered"
)
st.markdown("<div class='big-title'>📚 Smart Study Planner</div>", unsafe_allow_html=True)
st.markdown("<p class='small'>Plan smarter. Study better. Built by Aaratrika 💙</p>", unsafe_allow_html=True)
st.markdown("""
<style>
.big-title {font-size:42px; color:#6C63FF; font-weight:800;}
.card {background:#F5F7FF; padding:18px; border-radius:14px; 
       box-shadow: 0 4px 10px rgba(0,0,0,0.08); margin-bottom:15px;}if "schedule" not in st.session_state:
.small {color:gray;}
</style>
""", unsafe_allow_html=True)
st.subheader("🔔 Daily Study Reminder")
st.session_state.reminder = st.text_input("Set your reminder message:")

if st.session_state.reminder:
    st.info(f"Reminder saved: {st.session_state.reminder}")
   
    if "schedule" not in st.session_state:
        st.session_state.schedule = []
   
    st.subheader("📅 Build Your Study Schedule")

col1, col2 = st.columns(2)
start_time = col1.time_input("Start Time")
end_time = col2.time_input("End Time")

subject = st.text_input("Subject")
topic = st.text_input("Chapter / Topic")

stype = st.selectbox("Type", ["Study", "Revision", "Break"])

if st.button("➕ Add to Schedule"):
    st.session_state.schedule.append({
        "Start": start_time.strftime("%H:%M"),
        "End": end_time.strftime("%H:%M"),
        "Subject": subject,
        "Topic": topic,
        "Type": stype
    })
    st.success("Added to your plan!")
import pandas as pd

if st.session_state.schedule:
    df = pd.DataFrame(st.session_state.schedule)

    def highlight(row):
        if row["Type"] == "Study":
            return ["background-color:#d0f0fd"] * len(row)
        elif row["Type"] == "Revision":
            return ["background-color:#d8f5d8"] * len(row)
        else:
            return ["background-color:#fff3cd"] * len(row)

    st.dataframe(df.style.apply(highlight, axis=1), use_container_width=True)

else:
    st.warning("No study sessions added yet!")
    st.dataframe(df.style.apply(highlight, axis=1), use_container_width=True)
    st.info("📌 Tip: Revise each chapter within 24 hours and again after 7 days for better retention.")  
# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.main {
    background-color: #0f172a;
    color: white;
}
h1, h2, h3 {
    color: #38bdf8;
}
</style>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.title("📚 Smart Study Planner")
st.caption("Study smarter, not longer. Built by Aaratrika 💙")

st.divider()

# ---------- SIDEBAR ----------
st.sidebar.header("🧠 Your Study Inputs")

subject = st.sidebar.text_input("📘 Subject")
hours = st.sidebar.slider("⏰ Hours available today", 1, 12, 3)
goal = st.sidebar.text_area("🎯 Goal for today")

priority = st.sidebar.selectbox(
    "Priority level",
    ["Low","Medium","High"]
)
strength = st.sidebar.selectbox(
    "How strong are you in this subject?",
    ["Weak","Average","Strong"]
)
mood = st.sidebar.selectbox(
    "😊 How are you feeling today?",
    ["Tired", "Normal", "Energetic"]
)

streak_count = update_streak()
st.markdown(f"### Your Current Study Streak: {streak_count} day(s)")
if streak_count >= 3:
    st.balloons()  # fun celebration effect

streak_count = update_streak()
if mood in stickers:
    st.image(random.choice(stickers[mood]), width=250)
if streak_count >= 7:
    st.success("🚀 7-day streak! You're unstoppable.")
elif streak_count >= 3:
    st.info("🔥 Keep going! Momentum is building.")

import time

st.subheader("⏱ Study Timer (Pomodoro)")

focus_time = st.number_input("Focus minutes:", 10, 60, 25)
break_time = st.number_input("Break minutes:", 5, 20, 5)

if st.button("▶ Start Timer"):
    st.info("Stay focused! 💪")
    for i in range(focus_time * 60):
        mins, secs = divmod(focus_time*60 - i, 60)
        st.write(f"⏳ {mins:02d}:{secs:02d}")
        time.sleep(1)
        st.empty()

    st.success("Break time! ☕")
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("⏱ Focus Timer")
# timer code here
st.markdown("</div>", unsafe_allow_html=True)
# ---------- MAIN ----------
st.subheader("✨ Your Personalized Plan")

if st.sidebar.button("🚀 Generate Plan"):
    st.session_state.plans.append({
        "subject": subject,
        "hours": hours,
        "goal": goal
    })

    st.write("📚 Your Study Plan Saved!")
    priority = st.sidebar.selectbox(
        "📊 How strong are you in this subject?",
        ["Very Weak", "Weak", "Average", "Strong"]
    )

    mood = st.sidebar.selectbox(
        "🙂 How are you feeling today?",
        ["Tired", "Normal", "Energetic"]
    )
    # 🎯 Personalization Logic
st.subheader("🧠 Smart Suggestions")

if mood == "Tired":
    st.info("😴 You're feeling tired. Try light study sessions with breaks.")
elif mood == "Normal":
    st.success("🙂 Balanced mood detected. A steady study pace works best.")
elif mood == "Energetic":
    st.success("⚡ High energy! Perfect time for deep focus and tough subjects.")
    if subject and goal:
        st.success("Your plan is ready!")

        st.markdown(f"""
        ### 📘 Subject: {subject}
        ⏰ *Study Time:* {hours} hours  
        🎯 *Goal:* {goal}
        """)

        st.markdown("### 📝 Suggested Plan")
        st.write("• Revise core concepts")
        st.write("• Practice important questions")
        st.write("• Review mistakes")
        st.write("• Quick recap + notes")

    else:
        st.warning("Please fill all the details 👀")
        # ---------- STUDY SCORE ----------
        score = 50

        # hours impact
        score += hours * 5

        # priority impact
        if priority in ["Very Weak", "Weak"]:
            score += 15
        elif priority == "Average":
            score += 10
        else:
            score += 5

        # mood impact
        if mood == "Energetic":
            score += 10
        elif mood == "Tired":
            score -= 5

        # cap score
        score = min(score, 100)
        st.markdown("### 📊 Study Score")
        st.progress(score)
        st.write(f"*Your study effectiveness score: {score}/100*")
        def update_streak():
            streak_file = "streak.txt"
            today = datetime.date.today().isoformat()

            # if file exists
            if os.path.exists(streak_file):
                with open(streak_file, "r") as f:
                    last_date, streak_count = f.read().split(",")
                    streak_count = int(streak_count)

                if last_date == today:
                    return streak_count  # already counted today
                elif datetime.date.fromisoformat(last_date) == datetime.date.today() - datetime.timedelta(days=1):
                    streak_count += 1  # consecutive day
                else:
                    streak_count = 1  # streak reset
            else:
                streak_count = 1  # first time using

            # save updated streak
            with open(streak_file, "w") as f:
                f.write(f"{today},{streak_count}")

            return streak_count
reflection = st.text_area("📝 What did you learn today?")

if st.button("Save Reflection"):
    st.session_state.plans.append({
        "reflection": reflection,
        "date": str(date.today())
    })
    st.success("Reflection saved!")
st.subheader("📝 Your Feedback")

name = st.text_input("Your Name")
comment = st.text_area("Your Feedback")

if st.button("Submit Feedback"):
    if name and comment:
        file_exists = os.path.isfile("feedback.csv")
        with open("feedback.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Name", "Comment", "Time"])
            writer.writerow([name, comment, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        st.success("Thank you for your feedback! ❤️")
    else:
        st.warning("Please fill all fields.")
        st.subheader("🗂 All Feedbacks")

if os.path.isfile("feedback.csv"):
    import pandas as pd
    df = pd.read_csv("feedback.csv")
    st.dataframe(df)
else:
    st.info("No feedback yet!")
