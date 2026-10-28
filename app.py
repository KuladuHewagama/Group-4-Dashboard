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
    h = [5, 2, 8, 4, 7, 1, 5, 10, 4, 7,
     3, 6, 3, 5, 2, 7, 4, 9, 5, 11]

print("Mean =", np.mean(h))
print("Median =", np.median(h))
print("Variance =", np.var(h, ddof=1))
print("Standard deviation =", np.std(h, ddof=1))

# Change 8 to 12
h[2] = 12

print("\nAfter changing 8 to 12")
print("Mean =", np.mean(h))
print("Median =", np.median(h))
print("Variance =", np.var(h, ddof=1))
print("Standard deviation =", np.std(h, ddof=1))

plt.hist(h, edgecolor="black")
plt.xlabel("Study hours")
plt.ylabel("Frequency")
plt.show()

with q2:
    st.header("Question2")
    st.write("Matrix calculations and linear system")

with q3:
    st.header("Question3")
    st.write("Polynomial calculations and graph")

with q4:
    st.header("Question4")
    st.write("Student performance analysis")
