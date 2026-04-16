from flask import Blueprint, request, jsonify
from services.ai_engine import analyze_url_for_phishing

ai_bp = Blueprint('ai_bp', __name__)

@ai_bp.route('/analyze-url', methods=['POST'])
def analyze_url():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
        
    try:
        prediction = analyze_url_for_phishing(url)
        return jsonify({
            "message": "Analysis completed",
            "prediction": prediction
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
