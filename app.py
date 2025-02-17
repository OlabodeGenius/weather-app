from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "your api key"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None
    if request.method == "POST":
        city = request.form["city"]
        weather_data, error = get_weather(city)
    return render_template("index.html", weather_data=weather_data, error=error)

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            weather = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"].capitalize(),
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "icon": data["weather"][0]["icon"]
            }
            return weather, None
        else:
            return None, "City not found or API error."
    except requests.exceptions.RequestException:
        return None, "Network error."

if __name__ == "__main__":
    app.run(debug=True)
