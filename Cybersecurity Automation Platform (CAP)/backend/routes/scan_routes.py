from flask import Blueprint, request, jsonify
from services.scanner import run_network_scan
from database.db import scans_collection

scan_bp = Blueprint('scan_bp', __name__)

@scan_bp.route('/run', methods=['POST'])
def run_scan():
    data = request.get_json()
    target = data.get('target')
    
    if not target:
        return jsonify({"error": "Target is required"}), 400
        
    try:
        results = run_network_scan(target)
        return jsonify({
            "message": "Scan completed successfully",
            "results": results
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@scan_bp.route('/', methods=['GET'])
def get_scans():
    if scans_collection is None:
        return jsonify({"scans": []}), 200
    
    scans = list(scans_collection.find().sort("timestamp", -1))
    for scan in scans:
        scan["_id"] = str(scan["_id"])
    
    return jsonify({"scans": scans}), 200
