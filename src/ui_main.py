import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from src.data_loader import load_mock_breathing_data
from src.signal_processing import bandpass_filter, calculate_bpm

st.set_page_config(page_title="Breath Monitor", layout="centered")

# Sidebar
st.sidebar.title("Settings")
duration = st.sidebar.slider("Duration (sec)", 5, 20, 10)

# Load and process data
t, raw = load_mock_breathing_data(duration_sec=duration)
filtered = bandpass_filter(raw)
bpm = calculate_bpm(filtered)

# Main interface
st.title("🫁 Breath Monitoring Dashboard")

col1, col2 = st.columns(2)
col1.metric("Breaths per Minute (BPM)", f"{bpm:.2f}")
col2.metric("Duration", f"{duration} sec")

st.subheader("Breathing Signal")
fig, ax = plt.subplots()
ax.plot(t, filtered, label="Filtered")
ax.plot(t, raw, alpha=0.3, label="Raw")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.legend()
st.pyplot(fig)

# Save button
if st.button("💾 Save to data/sample_data.npy"):
    np.save("data/sample_data.npy", filtered)
    st.success("Saved!")

# Refresh button
if st.button("🔄 Refresh"):
    st.rerun()
