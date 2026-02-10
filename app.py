import streamlit as st
import pandas as pd
from pathlib import Path
from coordinator import Coordinator, REPORT_PATH

st.set_page_config(
    page_title="Drone Operations Coordinator",
    layout="wide"
)

st.title("🚁 Drone Operations Coordinator")
st.markdown(
    "Use the controls below to analyze missions and generate the operations report."
)

# Initialize Coordinator
if "coord" not in st.session_state:
    st.session_state.coord = Coordinator()

coord = st.session_state.coord

col1, col2 = st.columns([1, 3])

with col1:
    if st.button("Analyze Missions"):
        with st.spinner("Assigning missions..."):
            coord.assign_missions()
            report_path = coord.generate_report()
            st.success(f"Analysis complete — report written to {report_path}")

    if Path(REPORT_PATH).exists():
        with open(REPORT_PATH, "rb") as f:
            st.download_button(
                "Download Report",
                f,
                file_name=Path(REPORT_PATH).name
            )

with col2:
    st.header("Assignments")
    if coord.assignments:
        df = pd.DataFrame(coord.assignments)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No assignments yet. Click 'Analyze Missions' to run assignment logic.")

st.header("Decision Notes")
if coord.decision_notes:
    for note in coord.decision_notes:
        st.write("•", note)
else:
    st.write("No decision notes recorded.")