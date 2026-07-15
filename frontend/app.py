import streamlit as st
import requests

st.set_page_config(page_title="Restaurant Finder", page_icon="🍽️")

st.title("🍽️ Restaurant Finder")

location = st.text_input("Enter Location")

if st.button("Search Restaurants"):

    if location:

        url = f"http://127.0.0.1:8000/restaurants/{location}"

        response = requests.get(url)

        if response.status_code == 200:

            restaurants = response.json()

            if restaurants:

                for i, restaurant in enumerate(restaurants, start=1):

                    with st.container(border=True):

                        st.subheader(f"{i}. {restaurant['name']}")

                        st.write("📍", restaurant["address"])

                        st.write("🏙️", restaurant["city"])

                        st.write("📮", restaurant["postcode"])

            else:
                st.warning("No restaurants found.")