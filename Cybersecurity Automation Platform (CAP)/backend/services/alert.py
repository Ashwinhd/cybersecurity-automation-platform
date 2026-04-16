import time
from database.db import alerts_collection
from bson import ObjectId

def get_all_alerts():
    """Fetches all alerts from the database."""
    if alerts_collection is None:
        return []
    alerts = list(alerts_collection.find())
    # Convert ObjectId to string for JSON serialization
    for alert in alerts:
        alert["_id"] = str(alert["_id"])
    return alerts

def resolve_alert(alert_id):
    """Marks an alert as resolved."""
    if alerts_collection is None:
        return False
    try:
        result = alerts_collection.update_one(
            {"_id": alert_id}, # Standard ID if using UUID, or ObjectId
            {"$set": {"status": "resolved", "resolved_at": time.time()}}
        )
        # Also try matching by alert_id field if _id doesn't work
        if result.matched_count == 0:
            result = alerts_collection.update_one(
                {"alert_id": alert_id},
                {"$set": {"status": "resolved", "resolved_at": time.time()}}
            )
        return result.matched_count > 0
    except Exception as e:
        print(f"Error resolving alert: {e}")
        return False
