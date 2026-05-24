import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json
import os

def load_dataset(data_dir='datasets/processed/'):
    normal = pd.read_csv(data_dir + 'normal.csv')
    early = pd.read_csv(data_dir + 'early_bearing.csv')
    severe = pd.read_csv(data_dir + 'severe_bearing.csv')
    belt = pd.read_csv(data_dir + 'belt_loose.csv')
    alt = pd.read_csv(data_dir + 'alternator_fault.csv')
    
    normal['label'] = 0
    early['label'] = 1
    severe['label'] = 2
    belt['label'] = 2
    alt['label'] = 2
    
    df = pd.concat([normal, early, severe, belt, alt], ignore_index=True)
    feature_cols = ['vib_peak_hz', 'vib_rms_g', 'vib_centroid', 'vib_kurtosis',
                    'magnetic_rms_uv', 'current_rms_a', 'temp_c']
    X = df[feature_cols].values
    y = df['label'].values
    return X, y

if __name__ == '__main__':
    X, y = load_dataset()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=50, max_depth=10),
        'SVM': SVC(kernel='rbf', probability=True),
        'MLP': MLPClassifier(hidden_layer_sizes=(16,8), max_iter=500)
    }
    
    results = {}
    os.makedirs('models/trained', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        results[name] = float(acc)
        print(f"{name}: {acc:.3f}")
        # Save model
        joblib.dump(model, f'models/trained/{name.lower()}.pkl')
    
    # Save accuracy report
    with open('results/accuracy_report.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n✅ Training complete. Models saved in models/trained/")
    print("📊 Accuracy report saved in results/accuracy_report.json")
    
    # Also generate a simple confusion matrix plot if matplotlib available
    try:
        import matplotlib.pyplot as plt
        from sklearn.metrics import ConfusionMatrixDisplay
        ConfusionMatrixDisplay.from_estimator(models['RandomForest'], X_test, y_test)
        plt.savefig('results/confusion_matrix.png')
        print("✅ Confusion matrix saved to results/confusion_matrix.png")
    except ImportError:
        print("⚠️ Install matplotlib to generate confusion matrix plot")
