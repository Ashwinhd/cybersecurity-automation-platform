import time
import os
import joblib
import re

# Global variable to cache the model in memory
_model = None

def get_model():
    global _model
    if _model is None:
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'models', 'phishing_model.pkl')
        try:
            _model = joblib.load(model_path)
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    return _model

def extract_features(url):
    """
    Extracts numerical features from a URL for model prediction. (Must match training features)
    """
    import pandas as pd
    features = {
        'length': len(url),
        'has_ip': 1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) else 0,
        'num_dots': url.count('.'),
        'num_hyphens': url.count('-'),
        'has_at': 1 if '@' in url else 0
    }
    # Return as a DataFrame to match the format expected by sklearn Random Forest
    return pd.DataFrame([features])

def analyze_url_for_phishing(url):
    """
    Analyzes a URL using the trained Random Forest model.
    """
    model = get_model()
    
    if model is None:
        # Fallback if model fails to load
        return {
            "url": url,
            "error": "Machine learning model unavailable",
            "model_version": "error"
        }
    
    # Extract features from the URL
    features_df = extract_features(url)
    
    # Predict (0 or 1) and get probability
    prediction = model.predict(features_df)[0]
    probabilities = model.predict_proba(features_df)[0]
    
    # The risk score is the probability of the positive class (phishing = 1)
    risk_score = probabilities[1]
    is_phishing = bool(prediction == 1)
    
    return {
        "url": url,
        "is_phishing": is_phishing,
        "risk_score": round(risk_score, 4),
        "timestamp": time.time(),
        "model_version": "v1.0-rf"
    }
