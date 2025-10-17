import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Air Quality Monitor", page_icon="🌤️", layout="wide")

# --- Header ---
st.title("🌤️ Air Quality Monitoring Dashboard")
st.markdown("""
Upload your **Air Quality CSV file**.  
Expected columns: **Date, Time, Temperature(°C), Humidity(%), CO2(ppm)**  
""")

# --- File Upload ---
uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

if uploaded_file is not None:
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        df.columns = [col.strip().lower() for col in df.columns]

        # Check required columns
        required_cols = ["date", "time", "temperature(°c)", "humidity(%)", "co2(ppm)"]
        if not all(col in df.columns for col in required_cols):
            st.error("❌ CSV must contain Date, Time, Temperature(°C), Humidity(%), and CO2(ppm).")
            st.stop()

        # Combine date & time
        df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"])

        # Rename for simplicity
        df.rename(columns={
            "temperature(°c)": "temperature",
            "humidity(%)": "humidity",
            "co2(ppm)": "co2"
        }, inplace=True)

        # --- Data Cleaning ---
        df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
        df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")
        df["co2"] = pd.to_numeric(df["co2"], errors="coerce")

        # Replace NaN or negative values safely
        df["temperature"].fillna(df["temperature"].mean(), inplace=True)
        df["humidity"].fillna(df["humidity"].mean(), inplace=True)
        df["co2"].fillna(df["co2"].mean(), inplace=True)

        # Ensure humidity and co2 are positive
        df["humidity"] = df["humidity"].abs()
        df["co2"] = df["co2"].abs()

        # --- Data Preview ---
        st.subheader("📄 Data Preview")
        st.dataframe(df.head(10))

        # --- Summary Statistics ---
        st.subheader("📊 Summary Statistics")
        st.write(df[["temperature", "humidity", "co2"]].describe())

        # --- Trend Analysis ---
        st.subheader("📈 Trend Analysis")
        col1, col2 = st.columns(2)

        # Temperature Chart
        with col1:
            st.write("🌡️ Temperature Over Time")
            fig, ax = plt.subplots()
            ax.plot(df["datetime"], df["temperature"], color="orange")
            ax.set_xlabel("Time")
            ax.set_ylabel("Temperature (°C)")
            st.pyplot(fig)

        # Humidity Chart
        with col2:
            st.write("💧 Humidity Over Time")
            fig, ax = plt.subplots()
            ax.plot(df["datetime"], df["humidity"], color="blue")
            ax.set_xlabel("Time")
            ax.set_ylabel("Humidity (%)")
            st.pyplot(fig)

        # CO₂ Chart
        st.write("🌫️ CO₂ Levels Over Time")
        fig, ax = plt.subplots()
        ax.plot(df["datetime"], df["co2"], color="green")
        ax.set_xlabel("Time")
        ax.set_ylabel("CO₂ (ppm)")
        st.pyplot(fig)

        # --- Air Quality Status ---
        st.subheader("🧮 Air Quality Status")
        avg_co2 = df["co2"].mean()
        st.metric("Average CO₂ (ppm)", f"{avg_co2:.2f}")

        if avg_co2 < 800:
            st.success("✅ Good Air Quality")
        elif avg_co2 < 1200:
            st.warning("⚠️ Moderate Air Quality — Ventilate the area")
        else:
            st.error("🚨 Poor Air Quality — High CO₂ levels detected!")

        # --- VISUALIZATION SECTION ---
        st.markdown("---")
        st.header("📊 Visualizations")

        # Streamlit Scatter Chart
        st.subheader("🟢 Streamlit Scatter Chart")
        st.write("This chart shows Temperature vs CO₂ colored by Humidity level.")
        st.scatter_chart(
            data=df,
            x="temperature",
            y="co2",
            color="humidity"
        )

        # Interactive Plotly Chart
        st.subheader("🔵 Interactive Plotly Chart")
        st.write("Interactive Temperature vs Humidity chart with CO₂ as color intensity.")
        fig_plotly = px.scatter(
            df,
            x="temperature",
            y="humidity",
            color="co2",
            title="Interactive Plotly Chart - Air Quality",
            labels={"temperature": "Temperature (°C)", "humidity": "Humidity (%)", "co2": "CO₂ (ppm)"},
            hover_data=["datetime"]
        )
        st.plotly_chart(fig_plotly, use_container_width=True)

        # Interactive Scatter Plot with Plotly (size by Humidity)
        st.subheader("🔴 Interactive Scatter Plot with Plotly")
        st.write("Shows CO₂ level as bubble size for each reading.")
        fig_scatter = px.scatter(
            df,
            x="temperature",
            y="co2",
            size="humidity",
            color="humidity",
            hover_name="datetime",
            title="Temperature vs CO₂ with Humidity Bubble Size"
        )

        # Replace invalid or NaN sizes safely before showing
        fig_scatter.update_traces(
            marker=dict(
                sizemode='diameter',
                sizemin=5
            )
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        # Download processed data
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Processed CSV", csv, "processed_air_data.csv", "text/csv")

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")
else:
    st.info("Please upload your CSV file to start the analysis.")
