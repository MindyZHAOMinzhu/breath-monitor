import numpy as np

def load_mock_breathing_data(length=300, fs=10):
   
    t = np.linspace(0, length/fs, length)
    # 呼吸频率 0.25Hz -> 15 次/分钟
    clean_signal = 0.5 * np.sin(2 * np.pi * 0.25 * t)
    noise = 0.05 * np.random.randn(length)
    return clean_signal + noise
