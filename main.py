import streamlit as st
from datetime import date

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

# ---------- MAIN ----------
st.subheader("✨ Your Personalized Plan")

if st.sidebar.button("🚀 Generate Plan"):
    priority = st.sidebar.selectbox(
        "📊 How strong are you in this subject?",
        ["Very Weak", "Weak", "Average", "Strong"]
    )

    mood = st.sidebar.selectbox(
        "🙂 How are you feeling today?",
        ["Tired", "Normal", "Energetic"]
    )
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
