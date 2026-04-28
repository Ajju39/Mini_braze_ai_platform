from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

st.set_page_config(page_title="Mini Braze CRM Dashboard", layout="wide")

st.title("Mini Braze AI Platform 🚀")
st.markdown("""
AI-powered customer engagement and analytics platform inspired by Braze.

### What this does:
- 📊 Analyze customer behavior  
- 🎯 Segment users  
- 🤖 Generate AI insights  
- 🔁 Simulate campaign strategies  

Built using Azure-style data pipelines + AI integration.
""")
st.write(
    "A lightweight project that simulates event ingestion, identity resolution, "
    "SQL segmentation, reverse ETL, A/B testing, and personalized messaging."
)

segments_path = OUTPUT_DIR / "user_segments.csv"
events_path = OUTPUT_DIR / "unified_events.csv"
messages_path = OUTPUT_DIR / "personalized_messages.csv"

if not segments_path.exists():
    st.warning("Run `python pipeline.py` first to generate output files.")
    st.stop()

segments = pd.read_csv(segments_path)
events = pd.read_csv(events_path)
messages = pd.read_csv(messages_path)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Users", len(segments))
col2.metric("Events", len(events))
col3.metric("Purchasers", int(segments["purchase_count"].sum()))
col4.metric("Messageable Users", int((segments["segment"] != "do_not_message").sum()))

st.subheader("User Segments")
segment_counts = segments["segment"].value_counts().reset_index()
segment_counts.columns = ["segment", "count"]
st.bar_chart(segment_counts.set_index("segment"))

st.subheader("Segment Table")
st.dataframe(segments, use_container_width=True)

st.subheader("Personalized Messages")
selected_segment = st.selectbox("Filter by Segment", ["All"] + sorted(messages["segment"].unique().tolist()))

filtered_messages = messages.copy()
if selected_segment != "All":
    filtered_messages = filtered_messages[filtered_messages["segment"] == selected_segment]

st.dataframe(filtered_messages, use_container_width=True)

st.subheader("Unified Events After Identity Resolution")
st.dataframe(events, use_container_width=True)

st.subheader("How to Explain This")
st.markdown(
    """
    - **SDK / REST API simulation:** Raw events are captured as JSON.
    - **Identity resolution:** Device IDs are mapped to user IDs.
    - **Warehouse logic:** SQL creates customer segments.
    - **Reverse ETL:** Segment attributes are exported as a Braze-style payload.
    - **Liquid-style personalization:** Templates generate dynamic user messages.
    - **A/B testing:** Users are assigned to email or in-app variants.
    """
)
