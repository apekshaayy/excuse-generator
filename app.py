import streamlit as st
# from streamlit_geolocation import streamlit_geolocation
import requests

def get_weather(city, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    data = response.json()
    st.write(data) 
    condition = data["weather"][0]["main"]
    temp = data["main"]["temp"]
    return condition, temp

api_key = st.secrets["OPENWEATHER_API_KEY"]

location = st.text_input("Where are you right now?", placeholder="e.g. Pune, Ahmedabad")

if location:
    st.write(f"Got it. Using **{location}** for weather & traffic.")

if st.button("Check Weather"):
    condition, temp = get_weather(location, api_key)
    st.write(f"It is currently **{condition}** in **{location}**.")