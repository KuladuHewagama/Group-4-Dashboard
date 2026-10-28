# Group 4 Dashboard - simple version
# This app runs our four question files and shows the results with explanations.

import io
import runpy
from contextlib import redirect_stdout
from pathlib import Path

import matplotlib
matplotlib.use("Agg")                      # lets graphs be drawn inside the web page
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sympy as sp
import streamlit as st

FOLDER = Path(__file__).parent


def run_question(file_name):
    """Run one of our question files and give back the variables it created.
    The printed text is hidden because we show nicer results instead."""
    with redirect_stdout(io.StringIO()):
        variables = runpy.run_path(str(FOLDER / file_name))
    plt.close("all")                       # close graphs made by the original file
    return variables


st.set_page_config(page_title="Group 4 Dashboard", page_icon="📊", layout="wide")
st.title("📊 Computational Mathematics Dashboard")
st.write("Results for Questions 1 to 4, with a simple explanation of what each result means.")

tab1, tab2, tab3, tab4 = st.tabs(["Question 1", "Question 2", "Question 3", "Question 4"])

# ------------------------------------------------------------------
# QUESTION 1 - Study hours
# ------------------------------------------------------------------
with tab1:
    st.header("Question 1: Study Hours")
    v = run_question("Question1.py")

    after = v["h"]                         # the list AFTER changing 8 to 12
    before = after.copy()
    before[2] = 8                          # put the original value back

    table = pd.DataFrame({
        "Before (8)": [np.mean(before), np.median(before), np.var(before, ddof=1), np.std(before, ddof=1)],
        "After (12)": [np.mean(after), np.median(after), np.var(after, ddof=1), np.std(after, ddof=1)],
    }, index=["Mean", "Median", "Variance", "Standard deviation"]).round(2)
    st.table(table)

    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.hist(after, edgecolor="black", color="skyblue")
    ax.set_xlabel("Study hours")
    ax.set_ylabel("Frequency")
    ax.set_title("Histogram of study hours")
    st.pyplot(fig)

    st.subheader("What this means")
    st.info(
        f"- The **mean** went from {np.mean(before):.2f} to {np.mean(after):.2f}. "
        f"One bigger value pulled the average up.\n"
        f"- The **median** went from {np.median(before)} to {np.median(after)}. "
        f"The median is the middle value, so it is not affected much by one change.\n"
        f"- The **standard deviation** went from {np.std(before, ddof=1):.2f} to "
        f"{np.std(after, ddof=1):.2f}. The data became a little more spread out."
    )

# ------------------------------------------------------------------
# QUESTION 2 - Matrices
# ------------------------------------------------------------------
with tab2:
    st.header("Question 2: Matrices")
    v = run_question("Question2.py")
    A, B, X, R = v["A"], v["B"], v["X"], v["R"]

    st.write("We solve the system **A · X = B**, where:")
    st.latex(r"A = " + sp.latex(sp.Matrix(A)) + r"\quad B = " + sp.latex(sp.Matrix(B)))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Determinant", f"{np.linalg.det(A):.2f}")
    c2.metric("x", f"{X[0]:.2f}")
    c3.metric("y", f"{X[1]:.2f}")
    c4.metric("z", f"{X[2]:.2f}")

    left, right = st.columns(2)
    with left:
        st.write("**Inverse of A**")
        st.dataframe(pd.DataFrame(np.linalg.inv(A)).round(3))
    with right:
        st.write("**Eigenvalues of A**")
        st.dataframe(pd.DataFrame({"Eigenvalue": np.real_if_close(np.linalg.eigvals(A))}).round(3))

    st.subheader("What this means")
    det = np.linalg.det(A)
    st.info(
        f"- The determinant is {det:.2f}. Because it is not zero, A has an inverse "
        f"and the system has exactly one solution.\n"
        f"- The solution is x = {X[0]:.2f}, y = {X[1]:.2f}, z = {X[2]:.2f}.\n"
        f"- The residual norm is {np.linalg.norm(R):.1e}, which is almost zero. "
        f"This means the solution fits all three equations.\n"
        f"- Eigenvalues show how the matrix stretches space in its special directions."
    )

# ------------------------------------------------------------------
# QUESTION 3 - Polynomial
# ------------------------------------------------------------------
with tab3:
    st.header("Question 3: Polynomial")
    v = run_question("Question3.py")
    t, f = v["t"], v["f"]
    d1, d2 = sp.diff(f, t), sp.diff(f, t, 2)

    st.latex(r"f(t) = " + sp.latex(f))
    left, right = st.columns(2)
    with left:
        st.write("**Factorised form**")
        st.latex(sp.latex(sp.factor(f)))
        st.write("**Derivatives**")
        st.latex(r"f'(t) = " + sp.latex(d1))
        st.latex(r"f''(t) = " + sp.latex(d2))
    with right:
        st.write("**Integrals**")
        st.latex(r"\int f(t)\,dt = " + sp.latex(sp.integrate(f, t)) + " + C")
        area = sp.integrate(f, (t, 0, 2))
        st.latex(r"\int_0^2 f(t)\,dt = " + sp.latex(area))

    # Graph of the polynomial with turning points marked
    turning = [float(p) for p in sp.solve(d1, t)]
    fn = sp.lambdify(t, f, "numpy")
    xs = np.linspace(-1, 5, 300)
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.plot(xs, fn(xs), color="steelblue")
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.scatter(turning, [fn(p) for p in turning], color="red", zorder=5, label="Turning points")
    ax.set_xlabel("t")
    ax.set_ylabel("f(t)")
    ax.set_title("Graph of f(t)")
    ax.legend()
    st.pyplot(fig)

    st.subheader("What this means")
    notes = []
    for p in turning:
        kind = "maximum (top of a hill)" if d2.subs(t, p) < 0 else "minimum (bottom of a valley)"
        notes.append(f"- At t = {p:.0f} the graph has a local {kind}, with f = {fn(p):.0f}.")
    real_roots = [complex(r).real for r in sp.Poly(f, t).nroots() if abs(complex(r).imag) < 1e-9]
    notes.append(f"- The graph crosses the t-axis (f = 0) at t = {real_roots[0]:.2f}.")
    notes.append(f"- f(t) = 2 happens at t = {', '.join(str(s) for s in sp.solve(sp.Eq(f, 2), t))}.")
    notes.append(f"- The area under the curve from t = 0 to t = 2 is {area}.")
    st.info("\n".join(notes))

# ------------------------------------------------------------------
# QUESTION 4 - Student performance
# ------------------------------------------------------------------
with tab4:
    st.header("Question 4: Student Performance")
    v = run_question("Question4.py")
    data = v["Data"]
    corr = data["Study Hours"].corr(data["Exam"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mean exam mark", f"{data['Exam'].mean():.1f}")
    c2.metric("Median exam mark", f"{data['Exam'].median():.1f}")
    c3.metric("Standard deviation", f"{data['Exam'].std():.1f}")
    c4.metric("Correlation", f"{corr:.2f}")

    with st.expander("Show the data table"):
        st.dataframe(data)

    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    axes[0, 0].scatter(data["Study Hours"], data["Exam"])
    axes[0, 0].set(xlabel="Study Hours", ylabel="Exam Marks", title="Study Hours vs Exam Marks")
    axes[0, 1].hist(data["Exam"], bins=10, edgecolor="black")
    axes[0, 1].set(xlabel="Exam Marks", ylabel="Frequency", title="Distribution of Exam Marks")
    axes[1, 0].boxplot(data["Exam"])
    axes[1, 0].set(ylabel="Exam Marks", title="Box Plot of Exam Marks")
    sns.heatmap(data[["Study Hours", "Assignment", "Exam"]].corr(), annot=True,
                fmt=".2f", cmap="coolwarm", ax=axes[1, 1])
    axes[1, 1].set_title("Correlation Heatmap")
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("What this means")
    strength = "very strong" if abs(corr) > 0.8 else "moderate" if abs(corr) > 0.5 else "weak"
    best = data.loc[data["Exam"].idxmax()]
    st.info(
        f"- The correlation between study hours and exam marks is {corr:.2f}, "
        f"a {strength} {'positive' if corr > 0 else 'negative'} relationship. "
        f"Students who study more tend to get higher marks.\n"
        f"- The mean ({data['Exam'].mean():.1f}) and median ({data['Exam'].median():.1f}) are close, "
        f"so the marks are fairly evenly spread.\n"
        f"- The highest mark is {best['Exam']} by student {best['Student']}, "
        f"who studied {best['Study Hours']} hours."
    )
