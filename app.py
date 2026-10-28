import io
import os
import re
import runpy
from contextlib import redirect_stdout
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sympy as sp
import streamlit as st

BASE_DIR = Path(__file__).parent
os.chdir(BASE_DIR)  # lets Question4.py find student_performance.csv

PURPLE, PINK, TEAL, ORANGE = "#6C63FF", "#FF6584", "#2EC4B6", "#FF9F1C"
sns.set_theme(style="whitegrid")

st.set_page_config(page_title="Computational Mathematics Dashboard",
                   page_icon="📊", layout="wide")

st.markdown(f"""
<style>
.banner {{background: linear-gradient(120deg, {PURPLE}, {PINK}); padding: 28px 32px;
         border-radius: 16px; color: white; margin-bottom: 18px;}}
.banner h1 {{margin: 0; font-size: 2.2rem; color: white;}}
.banner p  {{margin: 6px 0 0 0; opacity: .92; font-size: 1.05rem;}}
[data-testid="stMetric"] {{background: rgba(108,99,255,.08); border-left: 6px solid {PURPLE};
         padding: 14px 18px; border-radius: 12px;}}
.stTabs [data-baseweb="tab"] {{font-size: 1.05rem; font-weight: 600;}}
</style>
<div class="banner">
  <h1>📊 Computational Mathematics Dashboard</h1>
  <p>Group 4 · Interactive results for Questions 1–4, powered by our own Python files</p>
</div>
""", unsafe_allow_html=True)


def run_file(name):
    """Run an ORIGINAL question file; return (its variables, its printed text)."""
    plt.close("all")
    buf = io.StringIO()
    with redirect_stdout(buf):
        variables = runpy.run_path(str(BASE_DIR / name))
    plt.close("all")
    return variables, buf.getvalue()


def raw_output(name, text):
    with st.expander(f"🧾 Raw printed output of {name}"):
        st.code(text, language="text")


def show_error(name, err):
    st.error(f"Could not run {name}: {err}")


# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("📁 Project files")
    st.write("Each tab runs one of our question files and turns its results into visuals.")
    for i in range(1, 5):
        with st.expander(f"Question{i}.py source code"):
            try:
                st.code((BASE_DIR / f"Question{i}.py").read_text(), language="python")
            except Exception as e:
                st.write(e)

tab1, tab2, tab3, tab4 = st.tabs(["📚 Question 1", "🧮 Question 2",
                                  "📈 Question 3", "🎓 Question 4"])

# ---------------- Question 1 ----------------
with tab1:
    st.header("Study hours statistics")
    try:
        v, out = run_file("Question1.py")
        h = list(v["h"])
        nums = [float(x) for x in re.findall(r"=\s*(-?\d+\.?\d*)", out)]
        before, after = nums[:4], nums[4:8]
        labels = ["Mean", "Median", "Variance", "Std deviation"]

        st.subheader("What happens when one value changes from 8 to 12?")
        cols = st.columns(4)
        for c, lab, b, a in zip(cols, labels, before, after):
            c.metric(lab, f"{a:.2f}", delta=f"{a - b:+.2f} vs original")

        left, right = st.columns(2)
        with left:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.hist(h, bins=6, color=PURPLE, edgecolor="white")
            ax.axvline(np.mean(h), color=PINK, lw=2, label=f"Mean {np.mean(h):.2f}")
            ax.axvline(np.median(h), color=ORANGE, lw=2, ls="--",
                       label=f"Median {np.median(h):.1f}")
            ax.set(xlabel="Study hours", ylabel="Frequency",
                   title="Histogram (after the change)")
            ax.legend()
            st.pyplot(fig)
        with right:
            fig, ax = plt.subplots(figsize=(6, 4))
            colors = [PINK if i == 2 else PURPLE for i in range(len(h))]  # index 2 = changed value
            ax.bar(range(1, len(h) + 1), h, color=colors)
            ax.set(xlabel="Student number", ylabel="Study hours",
                   title="Hours per student (pink = changed value)")
            st.pyplot(fig)

        st.info("Changing 8 → 12 pulls the mean up and makes the data more spread out "
                "(variance and standard deviation grow), while the median barely moves.")
        raw_output("Question1.py", out)
    except Exception as e:
        show_error("Question1.py", e)

# ---------------- Question 2 ----------------
with tab2:
    st.header("Matrix calculations")
    try:
        v, out = run_file("Question2.py")
        A, B, X = v["A"], v["B"], v["X"]
        R = v["R"]

        st.subheader("The linear system  A · X = B")
        st.latex(sp.latex(sp.Matrix(A)) + r"\cdot \begin{bmatrix}x\\y\\z\end{bmatrix} = "
                 + sp.latex(sp.Matrix(B)))

        cols = st.columns(5)
        cols[0].metric("Determinant", f"{np.linalg.det(A):.3f}")
        cols[1].metric("x", f"{X[0]:.3f}")
        cols[2].metric("y", f"{X[1]:.3f}")
        cols[3].metric("z", f"{X[2]:.3f}")
        cols[4].metric("Residual norm", f"{np.linalg.norm(R):.1e}")
        st.success("A residual norm close to 0 means the solution satisfies every equation.")

        left, right = st.columns(2)
        with left:
            fig, ax = plt.subplots(figsize=(5, 4))
            sns.heatmap(np.linalg.inv(A), annot=True, fmt=".2f", cmap="coolwarm",
                        center=0, ax=ax, cbar=False)
            ax.set_title("Inverse of A")
            st.pyplot(fig)
        with right:
            vals = np.real_if_close(np.linalg.eigvals(A))
            fig, ax = plt.subplots(figsize=(5, 4))
            ax.bar([f"λ{i + 1}" for i in range(len(vals))], np.real(vals),
                   color=[PURPLE, TEAL, ORANGE][:len(vals)])
            ax.set_title("Eigenvalues of A")
            st.pyplot(fig)

        with st.expander("🔎 Eigenvectors (columns)"):
            st.dataframe(pd.DataFrame(np.linalg.eig(A)[1]))
        raw_output("Question2.py", out)
    except Exception as e:
        show_error("Question2.py", e)

# ---------------- Question 3 ----------------
with tab3:
    st.header("Polynomial calculations")
    try:
        v, out = run_file("Question3.py")
        t, f = v["t"], v["f"]
        d1, d2 = sp.diff(f, t), sp.diff(f, t, 2)

        st.latex(r"f(t) = " + sp.latex(f) + r"\qquad = \quad " + sp.latex(sp.factor(f)))

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Derivatives**")
            st.latex(r"f'(t) = " + sp.latex(d1))
            st.latex(r"f''(t) = " + sp.latex(d2))
        with c2:
            st.markdown("**Integral**")
            st.latex(sp.latex(sp.integrate(f, t)) + " + C")
        with c3:
            st.metric("Definite integral from 0 to 2", f"{float(sp.integrate(f, (t, 0, 2))):.2f}")
            st.write("Solutions of f(t) = 2:", sp.solve(sp.Eq(f, 2), t))

        roots = [complex(r) for r in sp.Poly(f, t).nroots()]
        real_roots = [r.real for r in roots if abs(r.imag) < 1e-9]
        crit = [float(c) for c in sp.solve(d1, t)]

        fn = sp.lambdify(t, f, "numpy")
        xs = np.linspace(-1, 5, 400)
        fig, ax = plt.subplots(figsize=(10, 4.5))
        ax.plot(xs, fn(xs), color=PURPLE, lw=3, label="f(t)")
        ax.axhline(0, color="gray", lw=1)
        ax.scatter(real_roots, [0] * len(real_roots), color=PINK, s=90, zorder=5,
                   label="Real root")
        ax.scatter(crit, [float(f.subs(t, c)) for c in crit], color=ORANGE, s=90,
                   zorder=5, label="Turning points")
        for c in crit:
            ax.annotate(f"({c:.0f}, {float(f.subs(t, c)):.0f})", (c, float(f.subs(t, c))),
                        textcoords="offset points", xytext=(8, 8))
        ax.set(xlabel="t", ylabel="f(t)", title="Graph of f(t)")
        ax.legend()
        st.pyplot(fig)

        st.write("**All roots of f(t) = 0:**",
                 [f"{r.real:.3f}" + (f" {r.imag:+.3f}i" if abs(r.imag) > 1e-9 else "")
                  for r in roots])
        raw_output("Question3.py", out)
    except Exception as e:
        show_error("Question3.py", e)

# ---------------- Question 4 ----------------
with tab4:
    st.header("Student performance analysis")
    try:
        v, out = run_file("Question4.py")
        data = v["Data"]
        corr = data["Study Hours"].corr(data["Exam"])

        cols = st.columns(5)
        cols[0].metric("Students", data.shape[0])
        cols[1].metric("Mean exam mark", f"{data['Exam'].mean():.1f}")
        cols[2].metric("Median exam mark", f"{data['Exam'].median():.1f}")
        cols[3].metric("Std deviation", f"{data['Exam'].std():.1f}")
        cols[4].metric("Hours ↔ Exam correlation", f"{corr:.2f}")

        strength = "very strong" if abs(corr) > 0.8 else "moderate" if abs(corr) > 0.5 else "weak"
        st.success(f"Study hours and exam marks have a {strength} "
                   f"{'positive' if corr > 0 else 'negative'} relationship.")

        a, b = st.columns(2)
        with a:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.scatter(data["Study Hours"], data["Exam"], color=PURPLE, s=80)
            m, c = np.polyfit(data["Study Hours"], data["Exam"], 1)
            xs = np.linspace(data["Study Hours"].min(), data["Study Hours"].max(), 50)
            ax.plot(xs, m * xs + c, color=PINK, lw=2, label="Trend line")
            ax.set(xlabel="Study hours", ylabel="Exam marks", title="Study hours vs exam marks")
            ax.legend()
            st.pyplot(fig)
        with b:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.hist(data["Exam"], bins=10, color=TEAL, edgecolor="white")
            ax.set(xlabel="Exam marks", ylabel="Frequency", title="Distribution of exam marks")
            st.pyplot(fig)

        c_, d_ = st.columns(2)
        with c_:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.boxplot(y=data["Exam"], color=ORANGE, ax=ax)
            ax.set_title("Box plot of exam marks")
            st.pyplot(fig)
        with d_:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.heatmap(data[["Study Hours", "Assignment", "Exam"]].corr(), annot=True,
                        fmt=".2f", cmap="coolwarm", ax=ax)
            ax.set_title("Correlation heatmap")
            st.pyplot(fig)

        st.subheader("🏆 Top 3 students by exam mark")
        st.dataframe(data.nlargest(3, "Exam"), hide_index=True)
        with st.expander("📋 Full dataset and summary statistics"):
            st.dataframe(data)
            st.dataframe(data.describe())
        raw_output("Question4.py", out)
    except Exception as e:
        show_error("Question4.py", e)
