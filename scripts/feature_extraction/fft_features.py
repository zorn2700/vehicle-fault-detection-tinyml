import numpy as np
from scipy.fft import rfft, rfftfreq
from scipy.stats import kurtosis

def extract_features(vibration_signal, sample_rate=1000):
    """
    Extract 4 vibration features from raw signal
    Returns: (peak_freq, rms, spectral_centroid, kurtosis)
    """
    N = len(vibration_signal)
    fft_vals = np.abs(rfft(vibration_signal))
    freqs = rfftfreq(N, 1/sample_rate)
    
    # Peak frequency
    peak_freq = freqs[np.argmax(fft_vals[1:])]  # skip DC
    
    # RMS
    rms = np.sqrt(np.mean(vibration_signal**2))
    
    # Spectral centroid
    centroid = np.sum(freqs * fft_vals) / np.sum(fft_vals)
    
    # Kurtosis
    kurt = kurtosis(vibration_signal)
    
    return peak_freq, rms, centroid, kurt
