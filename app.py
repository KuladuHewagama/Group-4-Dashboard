import io
import os
import runpy
from contextlib import redirect_stdout
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # draw figures in memory so Streamlit can show them
import matplotlib.pyplot as plt
import streamlit as st

BASE_DIR = Path(__file__).parent
os.chdir(BASE_DIR)  # so Question4.py can find student_performance.csv

st.set_page_config(page_title="Computational Mathematics Dashboard", layout="wide")
st.title("Computational Mathematics Dashboard")
st.write("Results and visualizations for Questions 1–4")


def run_question(filename):
    """Run an original question file, then show its print() text and its plots."""
    plt.close("all")
    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer):          # capture everything print() writes
            runpy.run_path(str(BASE_DIR / filename))
    except Exception as e:
        st.error(f"Error while running {filename}: {e}")

    text = buffer.getvalue()
    if text:
        st.subheader("Output")
        st.code(text, language="text")

    figures = [plt.figure(n) for n in plt.get_fignums()]  # figures made by plt.show() code
    if figures:
        st.subheader("Graphs")
        for fig in figures:
            st.pyplot(fig)
    plt.close("all")


tabs = st.tabs(["Question 1", "Question 2", "Question 3", "Question 4"])

for i, tab in enumerate(tabs, start=1):
    with tab:
        st.header(f"Question {i}")
        run_question(f"Question{i}.py")
