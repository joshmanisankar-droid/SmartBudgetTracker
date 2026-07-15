import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAINFOREST_API_KEY")

params = {
    "api_key": API_KEY,
    "type": "product",
    "url": "https://www.amazon.in/dp/B0DCNWN8NZ"
}

response = requests.get(
    "https://api.rainforestapi.com/request",
    params=params,
    timeout=30
)

print("Status:", response.status_code)
print(response.text)