import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# App Title
st.set_page_config(page_title="Air Quality Monitor", page_icon="🌤️", layout="wide")
st.title("🌤️ Air Quality Monitoring Data Analyzer")

st.write("Upload your CSV file with columns: **Date, Time, Temperature (°C), Humidity (%), CO₂ (ppm)**")

# Upload CSV
uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

if uploaded_file is not None:
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)

        # Rename columns if needed
        df.columns = [col.strip().lower() for col in df.columns]

        # Combine Date + Time
        if "date" in df.columns and "time" in df.columns:
            df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"])
        else:
            st.error("CSV must contain 'Date' and 'Time' columns.")
            st.stop()

        # Display Data
        st.subheader("📄 Uploaded Data Preview")
        st.dataframe(df.head())

        # Summary Statistics
        st.subheader("📊 Summary Statistics")
        st.write(df.describe())

        # Line charts
        st.subheader("📈 Trend Graphs")
        col1, col2 = st.columns(2)

        with col1:
            st.write("🌡️ Temperature Over Time")
            fig, ax = plt.subplots()
            ax.plot(df["datetime"], df["temperature"], color='orange')
            ax.set_xlabel("Time")
            ax.set_ylabel("Temperature (°C)")
            st.pyplot(fig)

        with col2:
            st.write("💧 Humidity Over Time")
            fig, ax = plt.subplots()
            ax.plot(df["datetime"], df["humidity"], color='blue')
            ax.set_xlabel("Time")
            ax.set_ylabel("Humidity (%)")
            st.pyplot(fig)

        # CO2 plot
        st.write("🌫️ CO₂ Levels Over Time")
        fig, ax = plt.subplots()
        ax.plot(df["datetime"], df["co2"], color='green')
        ax.set_xlabel("Time")
        ax.set_ylabel("CO₂ (ppm)")
        st.pyplot(fig)

        # Air Quality Analysis
        st.subheader("🧮 Air Quality Analysis")

        avg_co2 = df["co2"].mean()
        st.metric("Average CO₂ (ppm)", f"{avg_co2:.2f}")

        if avg_co2 < 800:
            st.success("✅ Good Air Quality")
        elif avg_co2 < 1200:
            st.warning("⚠️ Moderate Air Quality — Consider ventilation")
        else:
            st.error("🚨 Poor Air Quality — High CO₂ levels detected!")

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a CSV file to begin analysis.")
