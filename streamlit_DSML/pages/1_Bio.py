import streamlit as st
from pathlib import Path

st.title("👋 My Bio")

# ---------- TODO: Replace with your own info ----------
NAME = "Simon Sealey"
PROGRAM = "MSU Senior - Bachelors of Science in Data Science and Machine Learning"
INTRO = (
    "I work at the intersection of two worlds most people keep separate: behavioral health and data science.

By day, I'm a Lead BHT and Group Facilitator at a residential SUD treatment facility in Denver, where I run groups, supervise staff, manage medications for 50+ clients, and lead data analytics projects that help our team make better decisions. By night (and weekends), I'm finishing a B.S. in Data Science & Machine Learning, building skills in Python, R, machine learning, and cloud computing.

What drives me is using data to improve outcomes for people who are often underserved by systems that don't measure what matters. My background in Social Work grounds the "why" behind the analysis.

I'm building toward roles that blend clinical insight with analytical capability: behavioral health analytics, program evaluation, health tech, or data roles in human services organizations.

If you work at that intersection too, I'd love to connect."
)
FUN_FACTS = [
    "I play dodgeball competitively.",
    "I've seen every season of Survivor.",
    "I was in a flash mob once"
]


PHOTO_PATH = "your_photo.jpg"  # Put a file in repo root or set a URL


def find_photo(filename=PHOTO_PATH):
    # Try common locations for multipage apps
    try:
        script_dir = Path(__file__).resolve().parent
    except NameError:
        script_dir = Path.cwd()

    candidates = [
        script_dir / "assets" / filename,          # pages/assets/...
        script_dir.parent / "assets" / filename,   # root/assets/... (common)
        Path("assets") / filename,                 # cwd/assets/...
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    return None

photo_src = find_photo(PHOTO_PATH)

# ---------- Layout ----------
col1, col2 = st.columns([1, 2], vertical_alignment="center")

with col1:
    if photo_src:
        st.image(photo_src, caption=NAME, use_container_width=True)
    else:
        st.info(
            "📷 Place `Your_Photo.jpg` inside an `assets/` folder at the app root "
            "or update the path in `find_photo()`."
        )
        
with col2:
    st.subheader(NAME)
    st.write(PROGRAM)
    st.write(INTRO)

st.markdown("### Fun facts")
for i, f in enumerate(FUN_FACTS, start=1):
    st.write(f"- {f}")

st.divider()
st.caption("Edit `pages/1_Bio.py` to customize this page.")
