
import hashlib
import secrets
from datetime import date, timedelta

import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="Smart Study Planner",
    page_icon="📚",
    layout="centered",
)

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at 8% 5%, #c8d8ff 0%, transparent 48%),
        radial-gradient(ellipse at 95% 12%, #f7c9e8 0%, transparent 48%),
        radial-gradient(ellipse at 48% 52%, #fff8f0 0%, transparent 60%),
        radial-gradient(ellipse at 8% 95%, #ffe4b9 0%, transparent 48%),
        radial-gradient(ellipse at 95% 95%, #f6d0e5 0%, transparent 50%),
        #f5efff;
    background-attachment: fixed;
    color: #34304a;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
}

h1, h2, h3, p, label {
    color: #34304a !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px;
}

div[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.58);
    border-radius: 14px;
}

div.stButton > button[kind="primary"] {
    background: #a995e8;
    color: #ffffff;
    border-radius: 14px;
    border: none;
}

div.stButton > button:hover {
    border-color: #a995e8;
    color: #69529c;
}

section[data-testid="stSidebar"] {
    background: rgba(244, 235, 255, 0.95);
}
</style>
""", unsafe_allow_html=True)


st.title("📚 Smart Study Planner")
st.caption("Plan smarter, study better ✨ Built by Aaratrika")


@st.cache_resource
def get_db():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_SERVICE_ROLE_KEY"],
    )


def hash_code(code):
    return hashlib.sha256(code.strip().encode()).hexdigest()


def empty_data():
    return {
        "plans": [],
        "schedule": [],
        "reflections": [],
        "reminder": "",
        "completed_dates": [],
        "skips": 0,
    }


def save_data():
    get_db().table("planner_profiles").update({
        "data": st.session_state.planner_data
    }).eq("id", st.session_state.planner_id).execute()


if "planner_id" not in st.session_state:
    st.session_state.planner_id = None


# CREATE OR RECOVER A PLANNER

if st.session_state.planner_id is None:
    st.info(
        "Your planner is saved online. Keep your private recovery "
        "code so you can reopen it on another visit or device."
    )

    new_tab, existing_tab = st.tabs(
        ["🌸 Create planner", "🔑 Open saved planner"]
    )

    with new_tab:
        if st.button("Create my planner", type="primary"):
            recovery_code = secrets.token_urlsafe(32)
            data = empty_data()

            result = get_db().table("planner_profiles").insert({
                "recovery_hash": hash_code(recovery_code),
                "data": data,
            }).execute()

            st.session_state.planner_id = result.data[0]["id"]
            st.session_state.planner_data = data
            st.session_state.new_recovery_code = recovery_code
            st.rerun()

    with existing_tab:
        with st.form("recover_planner"):
            entered_code = st.text_input(
                "Your recovery code",
                type="password",
            )
            recover = st.form_submit_button("Open my planner")

        if recover:
            if not entered_code.strip():
                st.warning("Enter your recovery code.")
            else:
                result = (
                    get_db()
                    .table("planner_profiles")
                    .select("id,data")
                    .eq("recovery_hash", hash_code(entered_code))
                    .limit(1)
                    .execute()
                )

                if result.data:
                    profile = result.data[0]
                    st.session_state.planner_id = profile["id"]
                    st.session_state.planner_data = {
                        **empty_data(),
                        **profile["data"],
                    }
                    st.rerun()
                else:
                    st.error("Recovery code not found.")

    st.stop()


# SHOW NEW RECOVERY CODE ONCE

if "new_recovery_code" in st.session_state:
    st.success("Your planner has been created!")

    st.warning(
        "IMPORTANT: Copy this recovery code and store it privately. "
        "It will not be displayed again."
    )

    st.code(st.session_state.new_recovery_code)

    if st.button("I have saved my recovery code"):
        del st.session_state.new_recovery_code
        st.rerun()

    st.stop()


data = st.session_state.planner_data

if st.sidebar.button("🔒 Close planner / switch profile"):
    st.session_state.planner_id = None
    st.session_state.pop("planner_data", None)
    st.rerun()


# STUDY STREAK

st.header("🔥 Your study streak")

completed_days = set(data["completed_dates"])
today = date.today()

cursor = (
    today
    if today.isoformat() in completed_days
    else today - timedelta(days=1)
)

streak = 0

while cursor.isoformat() in completed_days:
    streak += 1
    cursor -= timedelta(days=1)

st.metric("Current streak", f"{streak} days")

if today.isoformat() in completed_days:
    st.success("You have completed a study session today! 🌟")
else:
    if st.button("I completed a study session today"):
        data["completed_dates"].append(today.isoformat())
        save_data()
        st.rerun()


# STUDY PLAN

st.header("✨ Create your study plan")

with st.form("create_plan"):
    subject = st.text_input("Subject", max_chars=100)
    goal = st.text_area("What do you want to complete?", max_chars=500)

    hours = st.slider("Available study hours", 1, 12, 2)

    priority = st.selectbox(
        "Priority",
        ["High", "Medium", "Low"],
    )

    confidence = st.selectbox(
        "Your confidence",
        ["Weak", "Average", "Strong"],
    )

    mood = st.selectbox(
        "How are you feeling?",
        ["😴 Tired", "🌷 Normal", "⚡ Energetic"],
    )

    generate = st.form_submit_button(
        "Generate and save plan",
        type="primary",
    )

if generate:
    if not subject.strip() or not goal.strip():
        st.warning("Please enter both a subject and a goal.")
    else:
        focus_minutes = (
            20 if mood == "😴 Tired"
            else 25 if mood == "🌷 Normal"
            else 30
        )

        new_plan = {
            "date": today.isoformat(),
            "subject": subject.strip(),
            "goal": goal.strip(),
            "hours": hours,
            "priority": priority,
            "confidence": confidence,
            "mood": mood,
            "focus": focus_minutes,
        }

        data["plans"].insert(0, new_plan)
        save_data()
        st.success("Your plan has been saved permanently! 💜")

st.subheader("📖 Saved study plans")

if not data["plans"]:
    st.caption("Your saved plans will appear here.")

for i, plan in enumerate(data["plans"]):
    with st.expander(
        f"{plan['subject']} · {plan['date']}",
        expanded=(i == 0),
    ):
        st.write(f"**Goal:** {plan['goal']}")
        st.write(f"**Available time:** {plan['hours']} hours")
        st.write(f"**Priority:** {plan['priority']}")
        st.write(f"**Confidence:** {plan['confidence']}")
        st.write(f"**Mood:** {plan['mood']}")

        focus = plan["focus"]

        st.markdown(
            f"""
**Suggested approach**

1. Review important concepts for {focus} minutes.
2. Practise questions in {focus}-minute focus blocks.
3. Take short breaks between blocks.
4. Review mistakes and summarise what you learned.
"""
        )

        if st.button("Delete this plan", key=f"delete_plan_{i}"):
            data["plans"].pop(i)
            save_data()
            st.rerun()


# REMINDER

st.header("🔔 My reminder")

reminder = st.text_input(
    "What should you remember?",
    value=data["reminder"],
    max_chars=300,
)

if st.button("Save reminder"):
    data["reminder"] = reminder
    save_data()
    st.success("Reminder saved!")

st.caption(
    "This is a saved in-app reminder, not a phone notification."
)


# DAILY SCHEDULE

st.header("📅 Study schedule")

with st.form("add_schedule"):
    col1, col2 = st.columns(2)

    with col1:
        start = st.time_input("Start time")

    with col2:
        end = st.time_input("End time")

    topic = st.text_input("Subject or topic", max_chars=200)

    session_type = st.selectbox(
        "Session type",
        ["Study", "Revision", "Break"],
    )

    add_session = st.form_submit_button("Add to schedule")

if add_session:
    if not topic.strip():
        st.warning("Please enter a topic.")
    elif start >= end:
        st.warning("End time must be after start time.")
    else:
        data["schedule"].append({
            "start": start.strftime("%H:%M"),
            "end": end.strftime("%H:%M"),
            "topic": topic.strip(),
            "type": session_type,
        })

        save_data()
        st.rerun()

if not data["schedule"]:
    st.caption("Your schedule will appear here.")

for i, session in enumerate(data["schedule"]):
    left, right = st.columns([5, 1])

    left.write(
        f"**{session['start']}–{session['end']}** · "
        f"{session['topic']} ({session['type']})"
    )

    if right.button("✕", key=f"delete_session_{i}"):
        data["schedule"].pop(i)
        save_data()
        st.rerun()


# STUDY REFLECTIONS

st.header("🧠 Before & after study reflection")

with st.form("reflection_form"):
    learned = st.text_area(
        "What did you study or learn today?",
        max_chars=2000,
    )

    distraction = st.text_input(
        "What distracted you?",
        max_chars=300,
    )

    realistic = st.selectbox(
        "Was your study plan realistic?",
        ["Yes", "Somewhat", "No"],
    )

    tomorrow = st.text_input(
        "One improvement for tomorrow",
        max_chars=300,
    )

    submit_reflection = st.form_submit_button(
        "Save my reflection",
        type="primary",
    )

if submit_reflection:
    if not learned.strip():
        st.warning("Write something about what you learned.")
    else:
        data["reflections"].insert(0, {
            "date": today.isoformat(),
            "learned": learned.strip(),
            "distraction": distraction.strip(),
            "realistic": realistic,
            "change": tomorrow.strip(),
        })

        save_data()
        st.success("Your reflection has been saved! 🌷")

st.subheader("💭 Previous reflections")

if not data["reflections"]:
    st.caption("Your reflections will appear here.")

for i, reflection in enumerate(data["reflections"]):
    with st.expander(
        f"Reflection · {reflection['date']} · #{i + 1}"
    ):
        st.write(reflection["learned"])

        st.caption(
            "Distraction: "
            + (reflection["distraction"] or "Not recorded")
        )

        st.caption(
            f"Was the plan realistic? {reflection['realistic']}"
        )

        st.caption(
            "Improvement: "
            + (reflection["change"] or "Not recorded")
        )


# ADAPTIVE STUDY CHECK

st.header("🌱 Small steps matter")

st.write(
    f"Main task skipped: {data['skips']} time(s)"
)

if st.button("I skipped my main task"):
    data["skips"] += 1
    save_data()
    st.rerun()

if data["skips"] >= 2:
    st.info(
        "Try breaking your main task into one smaller, "
        "more manageable step."
    )


# PRIVATE FEEDBACK

st.header("💌 Feedback box")

st.write(
    "Share suggestions, problems or feedback about "
    "the Smart Study Planner."
)

with st.form("feedback_form", clear_on_submit=True):
    comment = st.text_area(
        "Your feedback",
        max_chars=2000,
        placeholder="What worked? What could be improved?",
    )

    send_feedback = st.form_submit_button("Submit feedback")

if send_feedback:
    if not comment.strip():
        st.warning("Please write your feedback first.")
    else:
        get_db().table("planner_feedback").insert({
            "planner_id": st.session_state.planner_id,
            "comment": comment.strip(),
        }).execute()

        st.success(
            "Thank you! Your feedback has been saved privately. 💜"
        )

st.divider()
st.caption("Made with curiosity, consistency and a little magic ✨")
