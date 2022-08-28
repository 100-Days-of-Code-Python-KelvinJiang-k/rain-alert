import requests
from twilio.rest import Client
import os

# OWN_API only provides weather forecast data every 3 hours
api_key = os.environ.get("OWN_API_KEY")
lat = 51.507351
lon = -0.127758
OWN_endpoint = "https://api.openweathermap.org/data/2.5/forecast"
HOURS_FORECASTED = 12

# Twilio API
account_SID = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
from_number = os.environ.get("FROM_NUMBER")
to_number = os.environ.get("TO_NUMBER")

weather_params = {
    "lat": lat,
    "lon": lon,
    "appid": api_key,
}

response = requests.get(OWN_endpoint, params=weather_params)

weather_data = response.json()["list"]
weather_slice = weather_data[0: HOURS_FORECASTED // 3]

will_rain = False
for weather in weather_slice:
    weather_id = weather["weather"][0]["id"]
    if weather_id < 700:
        will_rain = True

if will_rain:
    client = Client(account_SID, auth_token)

    message = client.messages.create(
        body="It will rain today.",
        from_=from_number,
        to=to_number,
    )

    print(message.sid)
