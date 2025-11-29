import streamlit as st
import pyttsx3   # <-- your TTS library

# ---------- TEXT TO SPEECH SETUP ----------
engine = pyttsx3.init()

def speak(text: str):
    """Speak the given text using pyttsx3."""
    engine.say(text)
    engine.runAndWait()


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="SukSham Predictor",
    page_icon="🎓",
    layout="wide",
)

# ---------- CUSTOM CSS ----------
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top, #1f2933 0, #020617 55%);
        color: #e5e7eb;
        font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }
    .glass-card {
        background: rgba(15, 23, 42, 0.85);
        border-radius: 18px;
        padding: 1.4rem 1.6rem;
        border: 1px solid rgba(148, 163, 184, 0.35);
        box-shadow: 0 18px 45px rgba(0,0,0,0.55);
        backdrop-filter: blur(18px);
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 750;
        letter-spacing: 0.03em;
        margin-bottom: 0.25rem;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: #cbd5f5;
        max-width: 460px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 999px;
        padding: 0.6rem 1.2rem;
        border: 1px solid rgba(191, 219, 254, 0.5);
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: #0b1120;
        font-weight: 650;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        box-shadow: 0 12px 30px rgba(34, 197, 94, 0.45);
    }
    .stButton>button:hover {
        filter: brightness(1.02);
        box-shadow: 0 16px 40px rgba(34, 197, 94, 0.7);
    }
    .stNumberInput>div>div>input, .stTextInput>div>div>input {
        background: rgba(15, 23, 42, 0.9);
        border-radius: 999px;
    }
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #9ca3af;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 0.4rem;
    }
    .footer {
        text-align: center;
        font-size: 0.75rem;
        color: #9ca3af;
        margin-top: 1.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    min_percent = st.slider(
        "Minimum required attendance (%)",
        50.0, 100.0, 75.0, 0.5,
        help="Change this according to your college rule.",
    )
    st.markdown("---")
    st.markdown(
        """
        **Tip**:  
        Use this for fun planning only.  
        Don't actually destroy your attendance 😄
        """
    )

# ---------- HERO SECTION ----------
st.markdown(
    """
    <div class="glass-card">
        <div class="hero-title">🎓 SukSham Predictor</div>
        <div class="hero-subtitle">
            The Fake Attendece checker.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")

# ---------- MAIN LAYOUT ----------
left, right = st.columns([1.05, 1.2])

with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Enter your details")
    st.caption("We only need a few numbers to predict your safe bunk limit.")

    bunked = st.number_input("Already bunked classes", min_value=0, step=1)
    total_days = st.number_input("Total working days in the semester", min_value=1, step=1)
    holidays = st.number_input("Upcoming holidays (no classes)", min_value=0, step=1)

    st.markdown(" ")
    calculate_pressed = st.button("Calculate my safe bunks")

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Result")

    if calculate_pressed:
        effective_total = total_days - holidays

        if effective_total <= 0:
            msg = (
                "Effective total classes became zero or negative. "
                "Please check total working days and upcoming holidays again."
            )
            st.error(
                "❗ Effective total classes became 0 or negative.\n"
                "Please re-check Total working days and Upcoming holidays."
            )
            speak(f"Hello Suket, {msg}")
        else:
            min_classes_to_attend = (min_percent / 100) * effective_total
            max_total_bunks_allowed = int(effective_total - min_classes_to_attend)

            if max_total_bunks_allowed < 0:
                msg = (
                    "Your attendance rule is too strict. "
                    "You cannot bunk any classes."
                )
                st.warning(
                    "Your attendance rule is too strict.\n"
                    "According to these numbers, you cannot bunk any classes."
                )
                speak(f"Hello Suket, {msg}")
            else:
                if bunked > max_total_bunks_allowed:
                    bunks_over = bunked - max_total_bunks_allowed

                    colA, colB, colC = st.columns(3)
                    with colA:
                        st.markdown('<div class="metric-label">Max bunks allowed</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="metric-value">{max_total_bunks_allowed}</div>', unsafe_allow_html=True)
                    with colB:
                        st.markdown('<div class="metric-label">You already bunked</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="metric-value">{bunked}</div>', unsafe_allow_html=True)
                    with colC:
                        st.markdown('<div class="metric-label">Extra bunks taken</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="metric-value">+{bunks_over}</div>', unsafe_allow_html=True)

                    st.error(
                        "⚠️ You are already in attendance shortage based on the current rule.\n"
                        "You need to start attending classes regularly to recover your percentage."
                    )
                    msg = (
                        f"Hello Suket, you are already in attendance shortage. "
                        f"Maximum bunks allowed are {max_total_bunks_allowed}, "
                        f"but you have already bunked {bunked} classes."
                    )
                    speak(msg)
                else:
                    bunks_left = max_total_bunks_allowed - bunked

                    colA, colB, colC = st.columns(3)
                    with colA:
                        st.markdown('<div class="metric-label">Safe bunks left</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="metric-value">{bunks_left}</div>', unsafe_allow_html=True)
                    with colB:
                        st.markdown('<div class="metric-label">Max bunks (total)</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="metric-value">{max_total_bunks_allowed}</div>', unsafe_allow_html=True)
                    with colC:
                        st.markdown('<div class="metric-label">Effective classes</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="metric-value">{effective_total}</div>', unsafe_allow_html=True)

                    st.success(
                        f"✅ You can still bunk {bunks_left} more class(es) "
                        f"without going below {min_percent:.1f}% attendance."
                    )
                    msg = (
                        f"Hello Suket, you can still bunk {bunks_left} more classes "
                        f"without going below {min_percent:.1f} percent attendance."
                    )
                    speak(msg)

                with st.expander("See detailed calculation breakdown"):
                    st.write(
                        f"""
                        - **Total working days**: `{total_days}`
                        - **Upcoming holidays**: `{holidays}`
                        - **Effective total classes**: `{effective_total}`  
                        - **Minimum required attendance**: `{min_percent:.1f}%`
                        - **Minimum classes to attend**  
                          = `{min_percent/100:.2f} × {effective_total}`  
                          ≈ `{int(min_classes_to_attend)}` classes
                        - **Maximum bunks allowed overall**  
                          = `Effective classes − Min classes to attend`  
                          = `{effective_total} − {int(min_classes_to_attend)}`  
                          = `{max_total_bunks_allowed}` classes
                        - **Your current bunks**: `{bunked}`
                        """
                    )
    else:
        st.info("Fill the details on the left and click **Calculate my safe bunks** to see the result.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown(
    """
    <div class="footer">
        Built with ❤️ using Streamlit • For academic fun only — please don't blame the app if you get detained.
    </div>
    """,
    unsafe_allow_html=True,
)
