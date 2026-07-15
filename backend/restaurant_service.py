import requests
from config import API_KEY


def get_restaurants(location):
    # Get latitude and longitude
    geo_url = (
        f"https://api.geoapify.com/v1/geocode/search?"
        f"text={location}&apiKey={API_KEY}"
    )

    geo_response = requests.get(geo_url).json()

    if not geo_response.get("features"):
        return []

    lat = geo_response["features"][0]["properties"]["lat"]
    lon = geo_response["features"][0]["properties"]["lon"]

    # Search restaurants within 5 km
    restaurant_url = (
        f"https://api.geoapify.com/v2/places?"
        f"categories=catering.restaurant"
        f"&filter=circle:{lon},{lat},5000"
        f"&limit=5"
        f"&apiKey={API_KEY}"
    )

    response = requests.get(restaurant_url).json()

    restaurants = []

    for item in response.get("features", []):
        p = item["properties"]

        restaurants.append({
            "name": p.get("name", "Unknown Restaurant"),
            "address": p.get("formatted", "No Address"),
            "city": p.get("city", ""),
            "postcode": p.get("postcode", "")
        })

    return restaurants