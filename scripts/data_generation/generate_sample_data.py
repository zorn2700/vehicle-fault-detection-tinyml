import numpy as np
import pandas as pd
import os

processed_dir = 'datasets/processed/'
os.makedirs(processed_dir, exist_ok=True)

n_samples = 2000

def generate_normal():
    return pd.DataFrame({
        'vib_peak_hz': np.random.normal(25, 3, n_samples),
        'vib_rms_g': np.random.normal(0.12, 0.02, n_samples),
        'vib_centroid': np.random.normal(350, 50, n_samples),
        'vib_kurtosis': np.random.normal(2.8, 0.3, n_samples),
        'magnetic_rms_uv': np.random.normal(45, 5, n_samples),
        'current_rms_a': np.random.normal(8.2, 0.5, n_samples),
        'temp_c': np.random.normal(88, 3, n_samples)
    })

def generate_early_bearing():
    return pd.DataFrame({
        'vib_peak_hz': np.random.normal(32, 4, n_samples),
        'vib_rms_g': np.random.normal(0.28, 0.04, n_samples),
        'vib_centroid': np.random.normal(520, 60, n_samples),
        'vib_kurtosis': np.random.normal(4.2, 0.5, n_samples),
        'magnetic_rms_uv': np.random.normal(52, 6, n_samples),
        'current_rms_a': np.random.normal(8.6, 0.6, n_samples),
        'temp_c': np.random.normal(92, 4, n_samples)
    })

def generate_severe():
    return pd.DataFrame({
        'vib_peak_hz': np.random.normal(48, 5, n_samples),
        'vib_rms_g': np.random.normal(0.65, 0.1, n_samples),
        'vib_centroid': np.random.normal(780, 80, n_samples),
        'vib_kurtosis': np.random.normal(5.8, 0.7, n_samples),
        'magnetic_rms_uv': np.random.normal(78, 9, n_samples),
        'current_rms_a': np.random.normal(9.5, 0.8, n_samples),
        'temp_c': np.random.normal(105, 5, n_samples)
    })

generate_normal().to_csv(f'{processed_dir}normal.csv', index=False)
generate_early_bearing().to_csv(f'{processed_dir}early_bearing.csv', index=False)
generate_severe().to_csv(f'{processed_dir}severe_bearing.csv', index=False)
generate_severe().to_csv(f'{processed_dir}belt_loose.csv', index=False)
generate_severe().to_csv(f'{processed_dir}alternator_fault.csv', index=False)

print("✅ Generated sample datasets in datasets/processed/")
