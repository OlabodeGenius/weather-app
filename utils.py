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
            print("API Response:", data)  # Debugging: Print the full API response
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
    except requests.exceptions.RequestException as e:
        return None, f"Network error: {str(e)}"