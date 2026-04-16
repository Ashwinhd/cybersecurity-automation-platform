import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import re

def extract_features(url):
    """
    Extracts numerical features from a URL for model prediction.
    """
    features = {
        'length': len(url),
        'has_ip': 1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) else 0,
        'num_dots': url.count('.'),
        'num_hyphens': url.count('-'),
        'has_at': 1 if '@' in url else 0
    }
    return features

def train_model():
    print("Loading dataset...")
    # Adjust path if script is run from a different directory
    dataset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'phishing_dataset.csv')
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}")
        return

    df = pd.read_csv(dataset_path)

    # Features and labels
    X = df[['length', 'has_ip', 'num_dots', 'num_hyphens', 'has_at']]
    y = df['label'] # 1 for phishing, 0 for legitimate

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save the model
    model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'phishing_model.pkl')
    
    print(f"Saving model to {model_path}...")
    joblib.dump(model, model_path)
    print("Model saved successfully!")

if __name__ == '__main__':
    train_model()
