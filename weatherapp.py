import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
from geopy.geocoders import Nominatim

# Replace 'your_api_key' with your actual OpenWeatherMap API key
API_KEY = "2d7f5ef45be03d457709f3557a11a629"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

def get_location_by_ip():
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        location = geolocator.geocode("me")
        if location and location.address:
            return location.address.split(", ")[-3]  # Extract city name
        else:
            return None
    except Exception as e:
        return None

def auto_detect_location():
    city = get_location_by_ip()
    if city:
        city_entry.delete(0, tk.END)
        city_entry.insert(0, city)
        display_weather()
    else:
        temp_label.config(text="Unable to detect location.")

def get_forecast(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

def show_forecast():
    city = city_entry.get()
    forecast_data = get_forecast(city)
    if forecast_data:
        forecast_window = tk.Toplevel(root)
        forecast_window.title("5-Day Weather Forecast")
        forecast_window.geometry("600x400")
        forecast_list = ttk.Treeview(forecast_window, columns=("Date", "Temp", "Condition"), show="headings")
        forecast_list.heading("Date", text="Date")
        forecast_list.heading("Temp", text="Temperature (°C)")
        forecast_list.heading("Condition", text="Condition")
        forecast_list.pack(fill=tk.BOTH, expand=True)
        for item in forecast_data['list']:
            date = item['dt_txt']
            temp = item['main']['temp']
            condition = item['weather'][0]['description']
            forecast_list.insert("", "end", values=(date, temp, condition))
    else:
        temp_label.config(text="Error fetching forecast data.")

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {"error": "Invalid API key. Please check your OpenWeatherMap API key."}
        elif response.status_code == 404:
            return {"error": "City not found. Please enter a valid city name."}
        else:
            return {"error": f"Error fetching data: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}

def display_weather():
    city = city_entry.get()
    weather_data = get_weather(city)
    if 'error' in weather_data:
        temp_label.config(text=weather_data['error'])
        desc_label.config(text="")
        humidity_label.config(text="")
        wind_label.config(text="")
        icon_label.config(image="")
    else:
        temperature = weather_data['main']['temp']
        weather_description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        # Update the labels with weather information
        temp_label.config(text=f"Temperature: {temperature}°C")
        desc_label.config(text=f"Condition: {weather_description.capitalize()}")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind Speed: {wind_speed} m/s")
        # Load weather icon
        icon_name = weather_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_name}@2x.png"
        try:
            icon_response = requests.get(icon_url, stream=True, timeout=10)
            if icon_response.status_code == 200:
                with open("templates/static/images/weather_icon.png", "wb") as img_file:
                    img_file.write(icon_response.content)
                img = Image.open("templates/static/images/weather_icon.png")
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                icon_label.config(image=img_tk)
                icon_label.image = img_tk  # Keep a reference to avoid garbage collection
        except requests.exceptions.RequestException:
            icon_label.config(image="")

# Dark mode toggle
dark_mode = False

def toggle_dark_mode():
    global dark_mode
    if dark_mode:
        root.config(bg="white")
        style.configure("TLabel", background="white", foreground="black")
        style.configure("TButton", background="white", foreground="black")
        dark_mode = False
    else:
        root.config(bg="#2c2c2c")
        style.configure("TLabel", background="#2c2c2c", foreground="white")
        style.configure("TButton", background="#2c2c2c", foreground="white")
        dark_mode = True

# Create the main application window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x500")
root.resizable(False, False)

# Style configuration
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 14))
style.configure("TButton", font=("Helvetica", 14))

# City input
city_label = ttk.Label(root, text="Enter City:")
city_label.pack(pady=10)

city_entry = ttk.Entry(root, font=("Helvetica", 14))
city_entry.pack(pady=10)

# Buttons
search_button = ttk.Button(root, text="Get Weather", command=display_weather)
search_button.pack(pady=20)

location_button = ttk.Button(root, text="Detect Location", command=auto_detect_location)
location_button.pack(pady=10)

forecast_button = ttk.Button(root, text="Show 5-Day Forecast", command=show_forecast)
forecast_button.pack(pady=10)

dark_mode_button = ttk.Button(root, text="Toggle Dark Mode", command=toggle_dark_mode)
dark_mode_button.pack(pady=10)

# Weather information display
temp_label = ttk.Label(root, text="Temperature: ")
temp_label.pack(pady=5)

desc_label = ttk.Label(root, text="Condition: ")
desc_label.pack(pady=5)

humidity_label = ttk.Label(root, text="Humidity: ")
humidity_label.pack(pady=5)

wind_label = ttk.Label(root, text="Wind Speed: ")
wind_label.pack(pady=5)

# Weather icon
icon_label = ttk.Label(root)
icon_label.pack(pady=20)

# Run the application
root.mainloop()