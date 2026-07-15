import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAINFOREST_API_KEY")


def scrape_product(url):
    if "amazon." not in url:
        raise Exception("Only Amazon links are supported.")

    params = {
        "api_key": API_KEY,
        "type": "product",
        "url": url
    }

    response = requests.get(
        "https://api.rainforestapi.com/request",
        params=params,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception("Failed to fetch product from Rainforest API.")

    data = response.json()

    if not data["request_info"]["success"]:
        raise Exception(data["request_info"].get("message", "Rainforest API Error"))

    product = data["product"]

    return {
        "title": product["title"],
        "price": float(product["buybox_winner"]["price"]["value"]),
        "image": product["main_image"]["link"],
        "availability": product["buybox_winner"]["availability"]["raw"]
    }