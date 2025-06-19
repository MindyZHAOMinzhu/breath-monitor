from scipy.signal import butter, filtfilt
import numpy as np

def bandpass_filter(signal, fs=10, low=0.1, high=0.6):
    """
    对信号进行带通滤波，保留呼吸频率范围（0.1~0.6Hz）

    参数:
        signal: 原始信号
        fs: 采样率
        low: 最低保留频率
        high: 最高保留频率
    返回:
        滤波后信号
    """
    b, a = butter(2, [low / (fs/2), high / (fs/2)], btype='band')
    return filtfilt(b, a, signal)

def estimate_breathing_rate(signal, fs=10):
    """
    估计呼吸频率（使用 FFT）

    返回:
        呼吸频率，单位：次/分钟
    """
    fft = np.abs(np.fft.rfft(signal))
    freqs = np.fft.rfftfreq(len(signal), d=1/fs)

    # 限定呼吸频率范围 0.1~0.6 Hz
    valid_idx = np.where((freqs >= 0.1) & (freqs <= 0.6))
    peak_idx = np.argmax(fft[valid_idx])
    peak_freq = freqs[valid_idx][peak_idx]
    return peak_freq * 60  # 转换成 BPM
