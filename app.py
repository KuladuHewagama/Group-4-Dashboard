from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sympy as sp
import streamlit as st

BASE_DIR = Path(__file__).parent

st.set_page_config(page_title="Computational Mathematics Dashboard", layout="wide")
st.title("Computational Mathematics Dashboard")
st.write("Results and visualizations for Questions 1–4")

q1, q2, q3, q4 = st.tabs(["Question 1", "Question 2", "Question 3", "Question 4"])

# ---------------- Question 1 ----------------
with q1:
    st.header("Question 1: Study hours statistics")
    h = [5, 2, 8, 4, 7, 1, 5, 10, 4, 7,
         3, 6, 3, 5, 2, 7, 4, 9, 5, 11]

    def stats(data):
        return pd.DataFrame({
            "Value": [np.mean(data), np.median(data),
                      np.var(data, ddof=1), np.std(data, ddof=1)]
        }, index=["Mean", "Median", "Variance", "Standard deviation"])

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Original data")
        st.dataframe(stats(h))
    h2 = h.copy()
    h2[2] = 12  # change 8 to 12
    with c2:
        st.subheader("After changing 8 to 12")
        st.dataframe(stats(h2))

    fig, ax = plt.subplots()
    ax.hist(h2, edgecolor="black")
    ax.set_xlabel("Study hours")
    ax.set_ylabel("Frequency")
    ax.set_title("Histogram of study hours (after change)")
    st.pyplot(fig)

# ---------------- Question 2 ----------------
with q2:
    st.header("Question 2: Matrix calculations")
    A = np.array([[2, 1, 1],
                  [1, 3, 2],
                  [3, 1, 2]])
    B = np.array([10, 18, 17])

    st.write("Matrix A")
    st.dataframe(pd.DataFrame(A))
    st.write("**Determinant =**", np.linalg.det(A))
    st.write("**Inverse**")
    st.dataframe(pd.DataFrame(np.linalg.inv(A)))
    vals, vecs = np.linalg.eig(A)
    st.write("**Eigenvalues**", vals)
    st.write("**Eigenvectors** (columns)")
    st.dataframe(pd.DataFrame(vecs))
    X = np.linalg.solve(A, B)
    st.write("**Solution X =**", X)
    R = A @ X - B
    st.write("**Residual =**", R)
    st.write("**Residual norm =**", np.linalg.norm(R))

# ---------------- Question 3 ----------------
with q3:
    st.header("Question 3: Polynomial calculations")
    t = sp.Symbol("t")
    f = t**3 - 6*t**2 + 9*t + 2

    st.latex(r"f(t) = " + sp.latex(f))
    st.write("(a) Factorised form:")
    st.latex(sp.latex(sp.factor(f)))
    st.write("(b) Roots of f(t) = 0:", sp.Poly(f, t).nroots())
    st.write("    Solutions of f(t) = 2:", sp.solve(sp.Eq(f, 2), t))
    st.write("(c) Derivatives:")
    st.latex(r"f'(t) = " + sp.latex(sp.diff(f, t)))
    st.latex(r"f''(t) = " + sp.latex(sp.diff(f, t, 2)))
    st.write("(d) Indefinite integral:")
    st.latex(sp.latex(sp.integrate(f, t)) + " + C")
    st.write("(e) Definite integral from 0 to 2:", sp.integrate(f, (t, 0, 2)))

    fn = sp.lambdify(t, f, "numpy")
    xs = np.linspace(-1, 5, 400)
    fig, ax = plt.subplots()
    ax.plot(xs, fn(xs))
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.set_xlabel("t")
    ax.set_ylabel("f(t)")
    ax.set_title("Graph of f(t)")
    ax.grid(True)
    st.pyplot(fig)

# ---------------- Question 4 ----------------
with q4:
    st.header("Question 4: Student performance analysis")
    data = pd.read_csv(BASE_DIR / "student_performance.csv")

    st.subheader("(a) Data overview")
    st.write("Dimension =", data.shape)
    st.dataframe(data)
    st.write("Data types")
    st.dataframe(data.dtypes.astype(str).rename("dtype"))
    st.write("Summary statistics")
    st.dataframe(data.describe())

    st.subheader("(b) Exam marks")
    st.write("Mean =", data["Exam"].mean())
    st.write("Median =", data["Exam"].median())
    st.write("Standard deviation =", data["Exam"].std())

    st.subheader("(c) Correlation (Study Hours vs Exam)")
    st.write("Correlation =", data["Study Hours"].corr(data["Exam"]))

    st.subheader("(d) Visualizations")
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes[0, 0].scatter(data["Study Hours"], data["Exam"])
    axes[0, 0].set(xlabel="Study Hours", ylabel="Exam Marks",
                   title="Study Hours vs Exam Marks")
    axes[0, 1].hist(data["Exam"], bins=10, edgecolor="black")
    axes[0, 1].set(xlabel="Exam Marks", ylabel="Frequency",
                   title="Distribution of Exam Marks")
    axes[1, 0].boxplot(data["Exam"].dropna())
    axes[1, 0].set(ylabel="Exam Marks", title="Box Plot of Exam Marks")
    corr = data[["Study Hours", "Assignment", "Exam"]].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=axes[1, 1])
    axes[1, 1].set_title("Correlation Heatmap")
    plt.tight_layout()
    st.pyplot(fig)
