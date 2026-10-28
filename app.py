import runpy
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).parent

st.set_page_config(page_title="Computational Mathematics Dashboard", layout="wide")
st.title("Computational Mathematics Dashboard")
st.write("Results and visualizations for Questions 1–4")

tabs = st.tabs(["Question 1", "Question 2", "Question 3", "Question 4"])

for i, tab in enumerate(tabs, start=1):
    with tab:
        st.header(f"Question {i}")
        runpy.run_path(str(BASE_DIR / f"Question{i}.py"))

q1, q2, q3, q4 = st.tabs(["Question 1", "Question 2", "Question 3", "Question 4"])

