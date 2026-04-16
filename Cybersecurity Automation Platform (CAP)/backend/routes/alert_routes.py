from flask import Blueprint, request, jsonify
from services.alert import get_all_alerts, resolve_alert

alert_bp = Blueprint('alert_bp', __name__)

@alert_bp.route('/', methods=['GET'])
def list_alerts():
    try:
        alerts = get_all_alerts()
        return jsonify({"alerts": alerts}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@alert_bp.route('/resolve/<id>', methods=['POST'])
def handle_resolve(id):
    try:
        success = resolve_alert(id)
        if success:
            return jsonify({"message": f"Alert {id} resolved"}), 200
        else:
            return jsonify({"error": "Alert not found or could not be resolved"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
