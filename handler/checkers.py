from datetime import timedelta, datetime

# ---------------------------
# Global state
# ---------------------------
pending_emergency = {}  
user_usage = {}         
DAILY_LIMIT = 3
WINDOW = timedelta(hours=24)

def check_rate_limit(user_id):
    now = datetime.now()
    usage = user_usage.get(user_id)

    if usage:
        if now - usage["first_request_time"] < WINDOW:
            if usage["count"] >= DAILY_LIMIT:
                return False  
            usage["count"] += 1
        else:
            user_usage[user_id] = {"count": 1, "first_request_time": now}
    else:
        user_usage[user_id] = {"count": 1, "first_request_time": now}

    return True, user_usage.get(user_id).get('count')