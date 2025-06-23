import numpy as np

def load_mock_breathing_data(duration_sec=10, sample_rate=20):
    t = np.linspace(0, duration_sec, duration_sec * sample_rate)
    signal = 0.5 * np.sin(2 * np.pi * 0.25 * t) + 0.1 * np.random.randn(len(t))
    return t, signal
