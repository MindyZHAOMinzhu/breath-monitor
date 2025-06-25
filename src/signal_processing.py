from scipy.signal import butter, filtfilt, find_peaks

def bandpass_filter(signal, lowcut=0.1, highcut=0.8, fs=20):
    nyq = 0.5 * fs
    b, a = butter(2, [lowcut / nyq, highcut / nyq], btype='band')
    return filtfilt(b, a, signal)

def calculate_bpm(filtered_signal, fs=20):
    peaks, _ = find_peaks(filtered_signal, distance=fs*1.5)
    duration_sec = len(filtered_signal) / fs
    if duration_sec == 0:
        return 0
    return len(peaks) / (duration_sec / 60)
