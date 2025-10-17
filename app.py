import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(page_title="Air Quality Monitoring Dashboard", layout="wide")

# ----------------------------
# Page Title
# ----------------------------
st.markdown(
    "<h1 style='text-align:center; color:#00FFFF;'>📊 Air Quality Monitoring Model</h1>",
    unsafe_allow_html=True,
)
st.markdown("<hr style='border: 1px solid #00FFFF;'>", unsafe_allow_html=True)

# ----------------------------
# Section Title
# ----------------------------
st.markdown(
    "<h2 style='color:#FFD700;'>📈 Visualizations</h2>",
    unsafe_allow_html=True,
)

# ----------------------------
# Generate Sample Air Quality Data
# ----------------------------
np.random.seed(42)
data = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'PM2.5': np.random.uniform(10, 200, 100),
    'category': np.random.choice(['A', 'B', 'C'], 100)
})

# Clean data to avoid NaN errors
data['PM2.5'] = data['PM2.5'].fillna(10).abs()

# ----------------------------
# Streamlit Scatter Chart
# ----------------------------
st.markdown(
    "<h3 style='color:#90EE90;'>Streamlit Scatter Chart</h3>",
    unsafe_allow_html=True,
)

st.scatter_chart(
    data,
    x='x',
    y='y',
    color='category',
)

# ----------------------------
# Interactive Plotly Chart
# ----------------------------
st.markdown(
    "<h3 style='color:#90EE90;'>Interactive Plotly Chart</h3>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h4 style='color:#FFA07A;'>Interactive Scatter Plot with Plotly</h4>",
    unsafe_allow_html=True,
)

# Create Plotly Scatter
fig = px.scatter(
    data,
    x='x',
    y='y',
    color='category',
    size='PM2.5',
    hover_data=['PM2.5'],
    title="Interactive Scatter Plot with Plotly",
)

fig.update_layout(
    template='plotly_dark',
    title_font=dict(size=20, color='cyan'),
    legend_title_text='Category',
    margin=dict(l=20, r=20, t=50, b=20),
)

# Display interactive chart
st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Footer
# ----------------------------
st.markdown("<hr style='border: 1px solid #00FFFF;'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:gray;'>Developed by P.CH.P IOT Solution</p>",
    unsafe_allow_html=True,
)
