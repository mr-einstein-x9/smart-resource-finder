import streamlit as st
from resource import resource_db

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Study Resource Finder",
    page_icon="📚",
    layout="centered"
)

# ---------------- SESSION STATE ----------------

if "history" not in st.session_state:
    st.session_state.history = []    


# ---------------- HEADER ----------------
st.title("📚 Smart Study Resource Finder")
st.caption("Find the best curated learning resources instantly.")

st.divider()


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Filters")

    subject = st.selectbox(
        "Choose Subject",
        list(resource_db.keys())
    )

    level = st.selectbox(
        "Choose Level",
        list(resource_db[subject].keys())
    )

    language_pref = st.selectbox(
        "Preferred Language",
        ["English", "Hindi", "Any"]
    )

    find_btn = st.button("🚀 Get Resources", use_container_width=True)



# ---------------- MAIN LOGIC ----------------
if find_btn:

    st.session_state.history.append({
    "subject": subject,
    "level": level,
    "language": language_pref
})

    all_resources = resource_db[subject][level]


    # ---- Language filter ----
    if language_pref == "Any":
        filtered = all_resources
    else:
        filtered = [
            r for r in all_resources
            if r["language"] == language_pref
        ]


    # ---------------- RESULTS ----------------
    st.subheader("🎯 Results")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Resources Found", len(filtered))

    with col2:
        st.metric(
        "Last Search",
        f"{subject} | {level} | {language_pref}"
        )

    st.divider()

    if filtered:
        for i, res in enumerate(filtered, start=1):
            with st.expander(f"📘 {i}. {res['name']}", expanded=False):
                st.markdown(f"**Language:** {res['language']}")

                if "desc" in res:
                    st.markdown(f"**Covers:** {res['desc']}")
                    
                st.markdown(f"[🔗 Open Resource]({res['link']})")
    else:
        st.warning("No matching resources found. Try changing filters.")

# ---------------- FOOTER ----------------
st.divider()
st.caption("Built by BrainBytes • Smart Resource Finder v1.0")
