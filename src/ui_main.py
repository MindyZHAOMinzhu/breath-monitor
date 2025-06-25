import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ==== 引入自定义模块 ====
from src.data_loader import load_mock_breathing_data
from src.signal_processing import bandpass_filter, calculate_bpm

# Optional: 尝试导入真实设备接口
try:
    from src.a121_data_source import A121BreathingMonitor
    has_real_sensor = True
except ImportError:
    has_real_sensor = False

# ==== Streamlit 设置 ====
st.set_page_config(page_title="Breath Monitor", layout="centered")
st.sidebar.title("Settings")

# ==== 数据源选择 ====
data_source = st.sidebar.selectbox("Select Data Source", ["Mock Data", "Real A121 Sensor"])

duration = st.sidebar.slider("Duration (sec)", 5, 20, 10)

# ==== 载入数据 ====
if data_source == "Mock Data":
    t, raw = load_mock_breathing_data(duration_sec=duration)
    source_used = "Mock"
else:
    if has_real_sensor:
        # 初始化 A121 接口，只取一帧
        sensor = A121BreathingMonitor()
        result = sensor.get_data()
        bpm = result.breathing_rate
        t = np.linspace(0, duration, duration * 50)
        raw = np.sin(2 * np.pi * (bpm / 60.0) * t) + 0.1 * np.random.randn(len(t))  # 模拟真实信号
        source_used = "Real"
        sensor.stop()
    else:
        st.error("⚠️ A121 模块未安装，无法使用实时数据。请确保 src/a121_data_source.py 存在。")
        st.stop()

# ==== 数据处理 ====
filtered = bandpass_filter(raw)
bpm = calculate_bpm(filtered)

# ==== 主界面展示 ====
st.title("🫁 Breath Monitoring Dashboard")
st.caption(f"📡 Data Source: {source_used}")

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

# ==== 保存 ====
if st.button("💾 Save to data/sample_data.npy"):
    np.save("data/sample_data.npy", filtered)
    st.success("Saved!")

# ==== 刷新 ====
if st.button("🔄 Refresh"):
    st.rerun()
