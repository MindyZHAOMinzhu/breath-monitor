# src/a111_interface.py

import numpy as np

def load_a111_data(duration_sec=10, sample_rate=20):
    # 👇 实际使用 Acconeer SDK 实时读取时替换这里
    print("⚠️ Real A111 data acquisition not implemented.")
    t = np.linspace(0, duration_sec, duration_sec * sample_rate)
    signal = np.zeros_like(t)  # 目前返回全 0 占位
    return t, signal
