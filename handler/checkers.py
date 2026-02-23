from datetime import timedelta, datetime

# ---------------------------
# Global state
# ---------------------------
pending_emergency = {}  
user_usage = {}         
DAILY_LIMIT = 5
WINDOW = timedelta(hours=24)

def check_rate_limit(user_id, text):
    now = datetime.now()
    usage = user_usage.get(user_id)

    if usage:
        if now - usage["first_request_time"] < WINDOW:

            user_sms_emergency = usage.get("user_sms_emergency", False)

            if usage["count"] >= DAILY_LIMIT:

                if text.strip() in ("1", "۱", "2", "۲") and not user_sms_emergency:
                    usage["user_sms_emergency"] = True
                    usage["count"] += 1
                    return True

                return False

            usage["count"] += 1

        else:
            user_usage[user_id] = {
                "count": 0,
                "first_request_time": now,
                "user_sms_emergency": False
            }

    else:
        user_usage[user_id] = {
            "count": 1,
            "first_request_time": now,
            "user_sms_emergency": False
        }

    count = user_usage.get(user_id).get('count', 0)
    return True, count