# Group 4 Dashboard
# This app runs our four Python files (Question1.py to Question4.py),
# then shows their results and their own graphs on the dashboard.

import io
import re
import runpy
import warnings
from contextlib import redirect_stdout
from pathlib import Path

import matplotlib
matplotlib.use("Agg")                      # lets the graphs from our files appear in the web page
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sympy as sp
import streamlit as st

warnings.filterwarnings("ignore")
FOLDER = Path(__file__).parent


def run_question(file_name):
    """Run one of our question files.
    Returns: the variables it created, the text it printed, and the graphs it drew."""
    plt.close("all")
    printed = io.StringIO()
    with redirect_stdout(printed):
        variables = runpy.run_path(str(FOLDER / file_name))
    graphs = [plt.figure(n) for n in plt.get_fignums()]
    return variables, printed.getvalue(), graphs


def show_graphs(graphs):
    """Show the graphs exactly as our Python file drew them."""
    for g in graphs:
        st.pyplot(g)
    plt.close("all")


st.set_page_config(page_title="Group 4 Dashboard", page_icon="📊", layout="wide")
st.title("📊 Computational Mathematics Dashboard")
st.write("Results for Questions 1 to 4, taken from our Python files.")

tab1, tab2, tab3, tab4 = st.tabs(["Question 1", "Question 2", "Question 3", "Question 4"])

# ------------------------------------------------------------------
# QUESTION 1 - Study hours
# ------------------------------------------------------------------
with tab1:
    st.header("Question 1: Study Hours")
    v, text, graphs = run_question("Question1.py")

    # Our file prints 4 values before the change, then 4 values after it
    numbers = [float(x) for x in re.findall(r"=\s*(-?\d+\.?\d*)", text)]
    table = pd.DataFrame(
        {"Before changing 8 to 12": numbers[:4], "After changing 8 to 12": numbers[4:8]},
        index=["Mean", "Median", "Variance", "Standard deviation"],
    ).round(3)

    st.subheader("Statistics")
    st.table(table)
    st.subheader("Histogram")
    show_graphs(graphs)

# ------------------------------------------------------------------
# QUESTION 2 - Matrices
# ------------------------------------------------------------------
with tab2:
    st.header("Question 2: Matrices")
    v, text, graphs = run_question("Question2.py")
    A, B, X, R = v["A"], v["B"], v["X"], v["R"]

    st.latex(r"A = " + sp.latex(sp.Matrix(A)) + r"\qquad B = " + sp.latex(sp.Matrix(B)))

    c1, c2 = st.columns(2)
    c1.metric("Determinant", f"{np.linalg.det(A):.3f}")
    c2.metric("Residual norm", f"{np.linalg.norm(R):.2e}")

    c1, c2, c3 = st.columns(3)
    c1.metric("Solution x", f"{X[0]:.3f}")
    c2.metric("Solution y", f"{X[1]:.3f}")
    c3.metric("Solution z", f"{X[2]:.3f}")

    left, right = st.columns(2)
    with left:
        st.subheader("Inverse of A")
        st.dataframe(pd.DataFrame(np.linalg.inv(A)).round(3))
        st.subheader("Eigenvalues")
        st.dataframe(pd.DataFrame({"Eigenvalue": np.real_if_close(np.linalg.eigvals(A))}).round(3))
    with right:
        st.subheader("Eigenvectors")
        st.dataframe(pd.DataFrame(np.linalg.eig(A)[1]).round(3))
        st.subheader("Residual")
        st.dataframe(pd.DataFrame({"Residual": R}))

# ------------------------------------------------------------------
# QUESTION 3 - Polynomial
# ------------------------------------------------------------------
with tab3:
    st.header("Question 3: Polynomial")
    v, text, graphs = run_question("Question3.py")
    t, f = v["t"], v["f"]

    st.latex(r"f(t) = " + sp.latex(f))

    left, right = st.columns(2)
    with left:
        st.subheader("(a) Factorised form")
        st.latex(sp.latex(sp.factor(f)))
        st.subheader("(b) Roots and f(t) = 2")
        st.write("Roots of f(t) = 0:", [str(r) for r in sp.Poly(f, t).nroots()])
        st.write("Solutions of f(t) = 2:", [str(s) for s in sp.solve(sp.Eq(f, 2), t)])
    with right:
        st.subheader("(c) Derivatives")
        st.latex(r"f'(t) = " + sp.latex(sp.diff(f, t)))
        st.latex(r"f''(t) = " + sp.latex(sp.diff(f, t, 2)))

    left, right = st.columns(2)
    left.subheader("(d) Indefinite integral")
    left.latex(sp.latex(sp.integrate(f, t)) + " + C")
    right.subheader("(e) Definite integral from 0 to 2")
    right.latex(sp.latex(sp.integrate(f, (t, 0, 2))))

    show_graphs(graphs)

# ------------------------------------------------------------------
# QUESTION 4 - Student performance
# ------------------------------------------------------------------
with tab4:
    st.header("Question 4: Student Performance")
    v, text, graphs = run_question("Question4.py")
    data = v["Data"]

    st.subheader("(a) The data")
    st.metric("Dimension (rows, columns)", str(data.shape))
    st.dataframe(data)
    with st.expander("Data types and summary statistics"):
        st.dataframe(data.dtypes.astype(str).rename("Data type"))
        st.dataframe(data.describe())

    st.subheader("(b) Exam marks")
    c1, c2, c3 = st.columns(3)
    c1.metric("Mean", f"{data['Exam'].mean():.2f}")
    c2.metric("Median", f"{data['Exam'].median():.2f}")
    c3.metric("Standard deviation", f"{data['Exam'].std():.2f}")

    st.subheader("(c) Correlation")
    st.metric("Study Hours vs Exam", f"{data['Study Hours'].corr(data['Exam']):.3f}")

    st.subheader("(d) Graphs")
    show_graphs(graphs)
