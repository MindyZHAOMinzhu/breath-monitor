from scipy.signal import butter, filtfilt
import numpy as np

def bandpass_filter(data, lowcut=0.1, highcut=0.8, fs=20, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

def calculate_bpm(signal, fs=20):
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(signal, distance=fs*1.5)
    bpm = len(peaks) / (len(signal) / fs) * 60
    return bpm
