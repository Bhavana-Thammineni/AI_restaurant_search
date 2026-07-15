import streamlit as st
import requests

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="🍽️ AI Restaurant Finder",
    page_icon="🍽️",
    layout="wide"
)

# -----------------------------
# API Key
# -----------------------------
# Local development:
# Uncomment the line below and replace with your API key
# API_KEY = "YOUR_GEOAPIFY_API_KEY"

# Streamlit Cloud:
API_KEY = st.secrets["GEOAPIFY_API_KEY"]


# -----------------------------
# Function to fetch restaurants
# -----------------------------
def get_restaurants(location):
    try:
        # Get latitude and longitude
        geo_url = (
            f"https://api.geoapify.com/v1/geocode/search?"
            f"text={location}&limit=1&apiKey={API_KEY}"
        )

        geo_response = requests.get(geo_url, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("features"):
            return []

        lat = geo_data["features"][0]["properties"]["lat"]
        lon = geo_data["features"][0]["properties"]["lon"]

        # Search restaurants
        restaurant_url = (
            f"https://api.geoapify.com/v2/places?"
            f"categories=catering.restaurant"
            f"&filter=circle:{lon},{lat},5000"
            f"&limit=5"
            f"&apiKey={API_KEY}"
        )

        response = requests.get(restaurant_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        restaurants = []

        for item in data.get("features", []):
            p = item["properties"]

            restaurants.append({
                "name": p.get("name", "Unknown Restaurant"),
                "address": p.get("formatted", "Address not available"),
                "city": p.get("city", ""),
                "postcode": p.get("postcode", ""),
                "lat": p.get("lat"),
                "lon": p.get("lon")
            })

        return restaurants

    except Exception as e:
        st.error(f"Error: {e}")
        return []


# -----------------------------
# UI
# -----------------------------
st.title("🍽️ AI Restaurant Finder")

st.write(
    "Search the **Top 5 Restaurants** in any location."
)

location = st.text_input(
    "Enter Location",
    placeholder="Example: KPHB, Hyderabad"
)

if st.button("🔍 Search Restaurants"):

    if location.strip() == "":
        st.warning("Please enter a location.")
        st.stop()

    with st.spinner("Searching restaurants..."):

        restaurants = get_restaurants(location)

    if not restaurants:
        st.error("No restaurants found.")
    else:

        st.success(f"Found {len(restaurants)} restaurants.")

        for i, r in enumerate(restaurants, start=1):

            with st.container(border=True):

                st.subheader(f"{i}. {r['name']}")

                st.write(f"📍 **Address:** {r['address']}")

                if r["city"]:
                    st.write(f"🏙️ **City:** {r['city']}")

                if r["postcode"]:
                    st.write(f"📮 **Postal Code:** {r['postcode']}")

                if r["lat"] and r["lon"]:
                    maps_url = (
                        f"https://www.google.com/maps/search/?api=1"
                        f"&query={r['lat']},{r['lon']}"
                    )

                    st.markdown(
                        f"[🗺️ Open in Google Maps]({maps_url})"
                    )

st.markdown("---")
st.caption("Built using Streamlit + Geoapify API")
