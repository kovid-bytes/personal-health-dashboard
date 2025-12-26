import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Personal Health Dashboard", page_icon="💪", layout="centered")

# ---------- STYLING ----------
st.markdown("""
<style>

body {
    background: radial-gradient(circle at top, #0a1535, #020710);
}

.main {
    padding-top: 5px;
}

/* GLASS CARD */
.card {
    background: rgba(255, 255, 255, 0.08);
    padding: 25px;
    border-radius: 22px;
    backdrop-filter: blur(14px);
    box-shadow: 0 0 35px rgba(0,0,0,0.4);
    border: 1px solid rgba(255,255,255,0.2);
}

/* TITLE */
.title {
    font-size: 34px;
    font-weight: 900;
    color: #a3ffd9;
    text-align:center;
    letter-spacing: .7px;
}

.sub {
    font-size: 15px;
    color: #c7d4ff;
    text-align:center;
}

/* BUTTON */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    padding: 10px;
    font-size: 17px;
    background: linear-gradient(135deg,#4dffda,#00ffa6);
    color: black;
    font-weight: bold;
    border: none;
}

/* SECTION TITLES */
h2,h3 {
    color:#afffff;
}

/* PROGRESS BADGE */
.badge {
    padding:6px 12px;
    border-radius:12px;
    background:#131c33;
    border:1px solid rgba(255,255,255,0.25);
    color:#8fffea;
    display:inline-block;
}

</style>
""", unsafe_allow_html=True)


# ---------- SESSION ----------
if "page" not in st.session_state:
    st.session_state.page = "welcome"

for k in ["name","gender","age","height","weight","bmi",
          "water_liters","sleep_hours","screen_hours",
          "sleep_suggestion","screen_status"]:
    if k not in st.session_state:
        st.session_state[k] = None


# ---------- UTIL ----------
def step(status):
    steps = ["Welcome","Basic","BMI","Water","Sleep","Screen","Done"]
    out=""
    for s in steps:
        if s==status: out+=f"🔹 **{s}**  ➤  "
        else: out+=f"▫️ *{s}*  ➤  "
    st.markdown(out[:-4])


# ---------- PAGES ----------
def welcome():
    step("Welcome")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">🌿 Personal Health Companion</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub">Smart • Smooth • Actually fun to use 😉</div>', unsafe_allow_html=True)
    st.write("")
    st.write("💧 Water • 😴 Sleep • 📱 Screen Time • 🧮 BMI")
    st.caption("Built like a premium app, not a class assignment.")
    if st.button("Begin Journey ➜"):
        st.session_state.page="basic"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def basic():
    step("Basic")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">🧍 Your Profile</div>', unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        st.session_state.name = st.text_input("Your Name")
        st.session_state.gender = st.selectbox("Gender",["Male","Female","Prefer not to say"])
    with col2:
        st.session_state.age = st.slider("Age",10,80,18)

    st.info("This helps personalize your experience 🌟")
    if st.button("Continue ➜ BMI"):
        st.session_state.page="bmi"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def bmi():
    step("BMI")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">🏋️ BMI Analysis</div>', unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        st.session_state.height = st.number_input("Height (cm)",100,250,170)
    with col2:
        st.session_state.weight = st.number_input("Weight (kg)",20,200,60)

    h = st.session_state.height / 100
    bmi = round(st.session_state.weight/(h*h),2)
    st.session_state.bmi = bmi
    st.write(f"### 📊 BMI Score: **{bmi}**")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi,
        gauge={'axis': {'range': [0,40]},
               'bar': {'color': "#00ffaa"},
               'steps': [
                   {'range': [0,18.5],'color':'#3a6bff'},
                   {'range': [18.5,25],'color':'#00ffb3'},
                   {'range': [25,30],'color':'orange'},
                   {'range': [30,40],'color':'red'}]},
        title={'text': "BMI Meter"}))
    st.plotly_chart(fig,use_container_width=True)

    if bmi<18.5: st.warning("Underweight 😥")
    elif bmi<24.9: st.success("Healthy & Balanced 👍")
    elif bmi<29.9: st.info("Overweight — improve slowly 🙂")
    else: st.error("Obese ⚠️ Health care needed")

    if st.button("Continue ➜ Water"):
        st.session_state.page="water"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def water():
    step("Water")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">💧 Hydration Goal</div>', unsafe_allow_html=True)

    water_ml = st.session_state.weight * 35
    st.session_state.water_liters = round(water_ml/1000,2)

    st.write(f"### You need ~ **{st.session_state.water_liters} Liters** daily")

    fig = go.Figure(go.Pie(values=[2,3], hole=0.6,
        marker_colors=["#00ffaa","#34404b"], textinfo="none"))
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig,use_container_width=True)

    st.caption("Hydrate like the main character you are 🌟")
    if st.button("Continue ➜ Sleep"):
        st.session_state.page="sleep"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def sleep():
    step("Sleep")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">😴 Sleep Tracking</div>', unsafe_allow_html=True)

    sleep_time = st.time_input("Sleep Time")
    wake_time = st.time_input("Wake Time")

    hrs = abs((wake_time.hour + wake_time.minute/60) - (sleep_time.hour + sleep_time.minute/60))
    if hrs>12: hrs=24-hrs
    hrs = round(hrs,2)
    st.session_state.sleep_hours = hrs

    st.write(f"### Slept: **{hrs} hrs**")

    fig = go.Figure(data=[
        go.Bar(name="You", x=["Sleep"], y=[hrs], marker_color="#33ffb5"),
        go.Bar(name="Ideal 8h", x=["Sleep"], y=[8], marker_color="#5e7bff")
    ])
    fig.update_layout(barmode='group')
    st.plotly_chart(fig,use_container_width=True)

    if hrs<7:
        st.session_state.sleep_suggestion="Sleep Earlier 😴"
        st.warning("Your brain wants rest")
    elif hrs<=9:
        st.session_state.sleep_suggestion="Perfect Sleep 😎"
        st.success("Healthy sleep routine!")
    else:
        st.session_state.sleep_suggestion="Too Much 🥱"
        st.info("Slept a bit too long")

    if st.button("Continue ➜ Screen Time"):
        st.session_state.page="screen"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def screen():
    step("Screen")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">📱 Screen Control</div>', unsafe_allow_html=True)

    st.session_state.screen_hours = st.slider("Phone Usage Today (hours)",0,12,3)

    safe = 3
    used = st.session_state.screen_hours

    fig = go.Figure(go.Pie(values=[used,max(0,safe-used)], hole=0.6,
        marker_colors=["red","#00ffb3"],
        labels=["Used","Safe Left"],
        textinfo="label+value"))
    st.plotly_chart(fig,use_container_width=True)

    if used<=3:
        st.session_state.screen_status="Healthy 👍"
        st.success("Good balance!")
    elif used<=5:
        st.session_state.screen_status="Careful 😬"
        st.warning("Reduce a bit")
    else:
        st.session_state.screen_status="Too much 😵"
        st.error("Touch the outside world occasionally")

    if st.button("Finish ➜ Dashboard"):
        st.session_state.page="done"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def done():
    step("Done")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="title">🎉 Final Health Dashboard — {st.session_state.name}</div>', unsafe_allow_html=True)

    st.write(f"**Age:** {st.session_state.age}")
    st.write(f"**Gender:** {st.session_state.gender}")
    st.write("---")
    st.write(f"🏋️ BMI → {st.session_state.bmi}")
    st.write(f"💧 Water → {st.session_state.water_liters} L daily")
    st.write(f"😴 Sleep → {st.session_state.sleep_hours} hrs → {st.session_state.sleep_suggestion}")
    st.write(f"📱 Screen Time → {st.session_state.screen_hours} hrs → {st.session_state.screen_status}")
    st.write("---")
    st.success("Looks premium. Feels premium. IS premium 😎")
    st.caption("You actually built something awesome. Nice work.")

    st.markdown('</div>', unsafe_allow_html=True)


# ---------- CONTROLLER ----------
pages = {
    "welcome": welcome,
    "basic": basic,
    "bmi": bmi,
    "water": water,
    "sleep": sleep,
    "screen": screen,
    "done": done
}

pages[st.session_state.page]()
