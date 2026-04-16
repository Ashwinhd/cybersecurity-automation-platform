import time
import uuid
import random
from database.db import alerts_collection

def detect_intrusion(payload):
    """
    Simulates an Intrusion Detection System analyzing a payload.
    Checks for common attack signatures.
    """
    print(f"Analyzing payload: {payload}")
    # Simulate processing time
    time.sleep(1)
    
    signatures = {
        "SQL Injection": ["' OR '1'='1", "UNION SELECT", "DROP TABLE"],
        "XSS": ["<script>", "javascript:", "onerror="],
        "Directory Traversal": ["../", "..\\", "/etc/passwd"]
    }
    
    detected_attacks = []
    if payload:
        for attack_type, sigs in signatures.items():
            for sig in sigs:
                if sig.lower() in payload.lower():
                    detected_attacks.append(attack_type)
                    break
                
    results = {
        "analysis_id": str(uuid.uuid4()),
        "timestamp": time.time(),
        "payload": payload,
        "detected_attacks": detected_attacks,
        "is_malicious": len(detected_attacks) > 0
    }
    
    if results["is_malicious"] and alerts_collection is not None:
        for attack in detected_attacks:
            alert = {
                "alert_id": str(uuid.uuid4()),
                "type": "Network Intrusion Detected",
                "severity": "High",
                "description": f"Potential {attack} attempt detected in payload.",
                "status": "new",
                "timestamp": time.time()
            }
            alerts_collection.insert_one(alert)
            
    return results