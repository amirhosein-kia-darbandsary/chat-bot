import requests
import os

def get_work_status():
    try:
        resp = requests.get(os.environ.get("GET_STATUS"))  
        data = resp.json()
        return data.get("WORK_STATUS", "free")
    except:
        return "free"  