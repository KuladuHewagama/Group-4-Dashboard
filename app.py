import streamlit as st

st.set_page_config(
    page_title="Computational Mathematics Dashboard",
    layout="wide"
)

st.title("Computational Mathematics Dashboard")
st.write("Results and visualizations for Questions 1–4")

q1, q2, q3, q4 = st.tabs([
    "Question1",
    "Question2",
    "Question3",
    "Question4"
])

with q1:
    st.header("Question1")
    st.write("Study hours: statistics and histogram")

with q2:
    st.header("Question2")
    st.write("Matrix calculations and linear system")

with q3:
    st.header("Question3")
    st.write("Polynomial calculations and graph")

with q4:
    st.header("Question4")
    st.write("Student performance analysis")
