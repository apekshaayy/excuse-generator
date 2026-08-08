import streamlit as st
import google.generativeai as genai
import requests


# ---------- API Functions ----------

def get_weather(city, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(url, params=params)
    data = response.json()

    if data.get("cod") == "404" and "," in city:
        # retry with just the city part, e.g. "Pashan, Pune" -> "Pune"
        fallback_city = city.split(",")[-1].strip()
        response = requests.get(url, params={"q": fallback_city, "appid": api_key, "units": "metric"})
        data = response.json()

    condition = data["weather"][0]["main"]
    temp = data["main"]["temp"]
    return condition, temp


def geocode(place, api_key):
    url = "https://api.openrouteservice.org/geocode/search"
    params = {"api_key": api_key, "text": place, "size": 1}
    response = requests.get(url, params=params)
    data = response.json()

    coords = data["features"][0]["geometry"]["coordinates"]  # [lon, lat]
    return coords


def get_traffic(origin, destination, api_key):
    origin_coords = geocode(origin, api_key)
    dest_coords = geocode(destination, api_key)

    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    params = {
        "api_key": api_key,
        "start": f"{origin_coords[0]},{origin_coords[1]}",
        "end": f"{dest_coords[0]},{dest_coords[1]}",
        "radiuses": "1000,1000"
    }
    response = requests.get(url, params=params)
    data = response.json()

    # st.write(data)

    summary = data["features"][0]["properties"]["summary"]
    duration_min = summary["duration"] / 60      # seconds → minutes
    distance_km = summary["distance"] / 1000     # meters → km
    return duration_min, distance_km

def generate_excuse(context, distress, condition, temp, duration, distance, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3-flash-preview")
    prompt = f"""Write a believable excuse for missing a {context}. 
    The distress level is {distress} (mild = mildly apologetic, moderate = genuinely stressed, panic = full-blown crisis mode)
    Use these real details casually in the excuse:
    - The weather of the city this person lives in is {condition}, {temp} Celcius.
    - For traffic, the distance is {distance:.0f} km route, currently taking {duration:.0f} minutes.
    Use casual but convincing language. 
    Keep it 2-3 sentences, sound natural and specific, no greetings or sign-offs.
    """

    response = model.generate_content(prompt)
    return response.text


# ---------- Secrets ----------

weather_key = st.secrets["OPENWEATHER_API_KEY"]
ors_key = st.secrets["OPENROUTESERVICE_API_KEY"]
generative_key = st.secrets["GEMINI_API_KEY"]


# ---------- UI ----------

st.title("Excuse Generator")

location = st.text_input("Where are you right now?", placeholder="e.g. Ahmedabad")
destination = st.text_input("Where are you headed?", placeholder="e.g. Pune")
context = st.selectbox("What are you missing?", ["School/College", "Famly Gathering", "Meetup", "Date"])
st.subheader("Distress Level")
distress = st.select_slider(
    "How panicked should this sound?",
    options=["Mild", "Moderate", "Panic"],
    value="Moderate"
)


# if location:
    # st.write(f"Got it. Using **{location}** for weather & traffic.")

# if st.button("Check Weather"):
    # condition, temp = get_weather(location, weather_key)
    # st.write(f"It is currently **{condition}**, {temp}°C in **{location}**.")

# if st.button("Check Traffic"):
    # duration, distance = get_traffic(location, destination, ors_key)
    # st.write(f"Route is **{distance:.1f} km**, about **{duration:.0f} min** drive.")

# if st.button("Generate Excuse"):
    # condition, temp = get_weather(location, weather_key)
    # duration, distance = get_traffic(location, destination, ors_key)
    # excuse = generate_excuse(context, condition, temp, duration, distance, generative_key)
    # st.write(excuse)

if st.button("Generate Excuse", type="primary"):
    if not location or not destination:
        st.warning("Fill in both the sections first.")
    else:
        with st.spinner("Cooking up your excuse..."):
            condition, temp = get_weather(location, weather_key)
            duration, distance = get_traffic(location, destination, ors_key)
            excuse = generate_excuse(context, distress, condition, temp, duration, distance, generative_key)
        st.success("Here's your excuse:")
        st.write(excuse)
        with st.expander("See the real data behind it"):
            st.write(f"Weather: {condition}, {temp}°C")
            st.write(f"Traffic: {distance:.1f} km, {duration:.0f} min")