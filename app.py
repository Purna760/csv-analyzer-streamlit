import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Air Quality Monitor", page_icon="🌤️", layout="wide")

st.title("🌤️ Air Quality Monitoring Dashboard")
st.write("""
Upload your **Air Quality CSV file**.  
Make sure it has the following columns:
**Date, Time, Temperature(°C), Humidity(%), CO2(ppm)**
""")

# File uploader
uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

if uploaded_file is not None:
    try:
        # Read CSV (skip no rows since header is row 1)
        df = pd.read_csv(uploaded_file)

        # Clean column names
        df.columns = [col.strip().lower() for col in df.columns]

        # Ensure necessary columns exist
        required_cols = ["date", "time", "temperature(°c)", "humidity(%)", "co2(ppm)"]
        if not all(col.lower() in df.columns for col in required_cols):
            st.error("❌ CSV must contain Date, Time, Temperature(°C), Humidity(%), and CO2(ppm) columns.")
            st.stop()

        # Combine date and time into one column
        df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"])

        # Rename for easier handling
        df.rename(columns={
            "temperature(°c)": "temperature",
            "humidity(%)": "humidity",
            "co2(ppm)": "co2"
        }, inplace=True)

        # Display preview
        st.subheader("📄 Data Preview")
        st.dataframe(df.head(10))

        # Summary statistics
        st.subheader("📊 Summary Statistics")
        st.write(df[["temperature", "humidity", "co2"]].describe())

        # Plot section
        st.subheader("📈 Trend Analysis")

        col1, col2 = st.columns(2)

        # Temperature graph
        with col1:
            st.write("🌡️ Temperature Over Time")
            fig, ax = plt.subplots()
            ax.plot(df["datetime"], df["temperature"], color="orange")
            ax.set_xlabel("Time")
            ax.set_ylabel("Temperature (°C)")
            st.pyplot(fig)

        # Humidity graph
        with col2:
            st.write("💧 Humidity Over Time")
            fig, ax = plt.subplots()
            ax.plot(df["datetime"], df["humidity"], color="blue")
            ax.set_xlabel("Time")
            ax.set_ylabel("Humidity (%)")
            st.pyplot(fig)

        # CO₂ graph
        st.write("🌫️ CO₂ Levels Over Time")
        fig, ax = plt.subplots()
        ax.plot(df["datetime"], df["co2"], color="green")
        ax.set_xlabel("Time")
        ax.set_ylabel("CO₂ (ppm)")
        st.pyplot(fig)

        # Air quality analysis
        st.subheader("🧮 Air Quality Status")
        avg_co2 = df["co2"].mean()

        st.metric("Average CO₂ (ppm)", f"{avg_co2:.2f}")

        if avg_co2 < 800:
            st.success("✅ Good Air Quality")
        elif avg_co2 < 1200:
            st.warning("⚠️ Moderate Air Quality — Ventilate the room")
        else:
            st.error("🚨 Poor Air Quality — High CO₂ levels detected!")

        # Download cleaned data
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Processed CSV", csv, "processed_air_data.csv", "text/csv")

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")
else:
    st.info("Please upload a CSV file to begin analysis.")
