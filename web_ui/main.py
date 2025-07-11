# web_ui/main.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt

from src.a121_data_source import A121BreathingMonitor

monitor = A121BreathingMonitor(use_fake=True)  # 后期改成 False 即用真实 A121
# result = monitor.get_data()
# print(result.breathing_rate)

st.set_page_config(page_title="Real-time Breathing Monitor", layout="wide")
st.title("🫁 Real-time Breathing Monitor")

refresh_interval = st.sidebar.slider("Refresh Interval (sec)", 0.1, 2.0, 0.5)

# 初始状态缓存
if "timestamps" not in st.session_state:
    st.session_state.timestamps = []
    st.session_state.bpms = []

# 两列结构
col1, col2 = st.columns([2, 1])
metric_box = col2.empty()
plot_box = col1.empty()

# 主循环：模拟 100 次更新
for _ in range(100):
    result = monitor.get_data()
    timestamp = time.time()
    st.session_state.timestamps.append(timestamp)
    st.session_state.bpms.append(result.breathing_rate)

    # 仅保留最近 30 个点
    if len(st.session_state.bpms) > 30:
        st.session_state.timestamps = st.session_state.timestamps[-30:]
        st.session_state.bpms = st.session_state.bpms[-30:]

    # 画图
    fig, ax = plt.subplots()
    t0 = st.session_state.timestamps[0]
    ax.plot([t - t0 for t in st.session_state.timestamps], st.session_state.bpms, label="BPM")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Breaths Per Minute")
    ax.set_title("Live BPM over Time")
    ax.grid(True)
    ax.legend()

    metric_box.metric("Current BPM", f"{result.breathing_rate:.1f}")
    plot_box.pyplot(fig)

    time.sleep(refresh_interval)

# import streamlit as st
# import numpy as np
# import matplotlib.pyplot as plt
# import time

# from src.data_interface import get_breathing_data
# from src.signal_processing import bandpass_filter, calculate_bpm

# # 页面设置
# st.set_page_config(page_title="Breath Monitor", layout="wide")

# # ===== 左侧选择模块（模拟多页面切换） =====
# st.sidebar.title("📂 Module Navigation")
# selected_module = st.sidebar.radio("Go to:", ["Overview", "Live Breathing", "How to Use", "About"])

# # ====== Module 1: Overview ======
# if selected_module == "Overview":
#     st.title("🫁 Breath Monitoring System")
#     st.markdown("""
# Welcome to the **handheld breath monitoring tool** — designed for wellness checks in shelters or outreach scenarios.
# This system combines radar sensing, real-time visualization, and minimal interaction UI to help field staff assess breathing status.
# """)

#     st.markdown("### 🔍 Features")
#     col1, col2 = st.columns([1, 1])
#     with col1:
#         st.markdown("- Real-time waveform\n- BPM Estimation\n- Data Logging\n- Field Friendly UI")
#     with col2:
#         st.image("web_ui/device_demo.png", caption="Handheld Demo", use_column_width=True)

#     st.markdown("---")

# # ====== Module 2: Live Breathing ======
# elif selected_module == "Live Breathing":
#     st.title("📈 Real-time Breathing Visualization")

#     # Data
#     sample_rate = 20
#     duration = 10
#     refresh_interval = 0.2
#     window_size = 100

#     t_all, raw_all = get_breathing_data(duration_sec=duration, sample_rate=sample_rate)
#     filtered = bandpass_filter(raw_all)
#     bpm = calculate_bpm(filtered)

#     # Layout: left waveform, right status
#     left_col, right_col = st.columns([2, 1])

#     with left_col:
#         plot_placeholder = st.empty()
#         for i in range(window_size, len(filtered)):
#             t_win = t_all[i - window_size:i]
#             raw_win = raw_all[i - window_size:i]
#             fil_win = filtered[i - window_size:i]

#             fig, ax = plt.subplots()
#             ax.plot(t_win, fil_win, label="Filtered", color="blue")
#             ax.plot(t_win, raw_win, label="Raw", color="gray", alpha=0.3)
#             ax.set_title("Live Breathing Signal")
#             ax.set_xlabel("Time (s)")
#             ax.set_ylabel("Amplitude")
#             ax.legend()
#             plot_placeholder.pyplot(fig)
#             time.sleep(refresh_interval)

#     with right_col:
#         st.metric("BPM", f"{bpm:.2f}")
#         if bpm < 8:
#             st.markdown(":orange[⚠️ Slow Breathing]")
#         elif bpm > 25:
#             st.markdown(":red[⚠️ Rapid Breathing]")
#         else:
#             st.markdown(":green[✅ Normal Breathing]")
        
#         st.button("💾 Save Snapshot")
    
#     st.markdown("---")

# # ====== Module 3: How to Use ======
# elif selected_module == "How to Use":
#     st.title("📝 How to Use the Device")
#     st.markdown("""
# 1. Place the radar near the **chest or abdomen**.
# 2. Ask the person to remain still for ~10 seconds.
# 3. Observe waveform and breathing rate.
# 4. Use status color and signal to decide next step.
# """)
#     st.image("web_ui/device_demo.png", caption="Illustration", use_column_width=True)

#     st.markdown("---")

# # ====== Module 4: About ======
# elif selected_module == "About":
#     st.title("ℹ️ Project Background")
#     st.markdown("""
# This project is part of a research initiative to support **non-contact respiratory monitoring** for at-risk populations,
# especially those in unsheltered settings, using **pulsed radar + handheld UI**.

# Built with:
# - 📡 Acconeer A111 mmWave radar
# - 🍓 Raspberry Pi Zero
# - 🐍 Python + Streamlit
# """)
