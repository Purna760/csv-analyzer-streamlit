import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="CSV Analyzer", layout="wide")

st.title("📊 CSV File Analyzer")
st.write("Upload your CSV file to explore and visualize data interactively!")

# File upload
uploaded_file = st.file_uploader("📁 Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read file
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    st.subheader("📈 Basic Information")
    st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")

    # Summary stats
    st.subheader("📊 Summary Statistics")
    st.write(df.describe())

    # Column selection for chart
    st.subheader("📉 Visualizations")
    columns = df.columns.tolist()

    x_axis = st.selectbox("Select X-axis", columns)
    y_axis = st.selectbox("Select Y-axis", columns)

    chart_type = st.radio("Choose chart type", ["Line", "Bar", "Scatter", "Pie"])

    if st.button("Generate Chart"):
        st.write(f"### {chart_type} Chart: {y_axis} vs {x_axis}")
        fig, ax = plt.subplots()

        if chart_type == "Line":
            ax.plot(df[x_axis], df[y_axis])
        elif chart_type == "Bar":
            ax.bar(df[x_axis], df[y_axis])
        elif chart_type == "Scatter":
            ax.scatter(df[x_axis], df[y_axis])
        elif chart_type == "Pie":
            df.groupby(x_axis)[y_axis].sum().plot.pie(autopct='%1.1f%%', ax=ax)
            ax.set_ylabel("")

        st.pyplot(fig)

else:
    st.info("👆 Upload a CSV file to start analyzing.")
