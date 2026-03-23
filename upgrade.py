import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Pro Student Analytics", layout="wide")

st.title("📊 PRO Student Performance Dashboard")

# ---------------- GRADE FUNCTION ----------------
def grade(avg):
    if avg >= 80:
        return "Distinction"
    elif avg >= 60:
        return "Proficient"
    elif avg >= 40:
        return "Pass"
    elif 40 > avg > 0:
        return "Fail"
    elif avg == 0 :
        return "missing mark"

# ---------------- FILE UPLOAD ----------------
st.sidebar.header("📁 Upload Data")
file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

# fallback sample data
if file is not None:
    df = pd.read_csv(file)
else:
    df = pd.DataFrame({
        "Name": ["John", "Mary", "Alex", "Sarah"],
        "Maths": [78, 92, 60, 88],
        "OS": [85, 88, 70, 92],
        "COA": [90, 84, 65, 91],
        "IS": [70, 95, 55, 89]
    })

# ---------------- PROCESS DATA ----------------
df["Average"] = df[["Maths", "OS", "COA", "IS"]].mean(axis=1)
df["Grade"] = df["Average"].apply(grade)

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Filters")

filter_option = st.sidebar.selectbox(
    "Select View",
    ["All Students", "Top 3 Students", "Failing Students", "Missing Marks"]
)

if filter_option == "Top 3 Students":
    df_view = df.sort_values(by="Average", ascending=False).head(3)
elif filter_option == "Failing Students":
    df_view = df[df["Average"] < 40]
elif filter_option == "Missing Marks":
    df_view = df[df["Average"] == 0]
else:
    df_view = df

# ---------------- MAIN TABLE ----------------
st.subheader("📋 Student Data")
st.dataframe(df_view, use_container_width=True)

# ---------------- ANALYTICS ----------------
st.subheader("Key Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Class Average", f"{df['Average'].mean():.2f}")
col2.metric("Top Score", f"{df['Average'].max():.2f}")
col3.metric("Lowest Score", f"{df['Average'].min():.2f}")
col4.metric("Fail Count", len(df[df["Average"] < 40]))
col5.metric("Missing Marks",len(df[df["Average"] == 0]))

# ---------------- CHARTS ----------------
st.subheader("📈 Performance Visualization")

fig, ax = plt.subplots()
ax.bar(df["Name"], df["Average"])
ax.set_title("Student Average Representation")
ax.set_ylabel("Average")
st.pyplot(fig)

# ---------------- GRADE DISTRIBUTION ----------------
st.subheader("📊 Grade Distribution")
st.bar_chart(df["Grade"].value_counts())

# ---------------- DOWNLOAD ----------------
st.subheader("⬇ Download Processed Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV",
    csv,
    "processed_students.csv",
    "text/csv"
)
