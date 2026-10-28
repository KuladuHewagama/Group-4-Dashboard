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
    exec(open("Question1.py").read())
   

with q2:
    st.header("Question2")
    st.write("Question2.py")

with q3:
    st.header("Question3")
    st.write("Question3.py")

with q4:
    st.header("Question4")
    st.write("Question4.py")
