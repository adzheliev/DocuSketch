import psutil
import requests

load = psutil.virtual_memory().percent

if load > 90:
    request_to_send = {"memory_usage": load}
    response = requests.post(url='API_URL', data=request_to_send)