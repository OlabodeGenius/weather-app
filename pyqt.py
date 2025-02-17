import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

API_KEY = "2d7f5ef45be03d457709f3557a11a629"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 400, 300)

        # Layout
        layout = QGridLayout()

        # City Input
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Enter City Name")
        layout.addWidget(self.city_input, 0, 0, 1, 2)

        # Search Button
        search_button = QPushButton("Get Weather", self)
        search_button.clicked.connect(self.display_weather)
        layout.addWidget(search_button, 0, 2)

        # Weather Information Labels
        self.temp_label = QLabel("Temperature: ", self)
        layout.addWidget(self.temp_label, 1, 0)

        self.desc_label = QLabel("Condition: ", self)
        layout.addWidget(self.desc_label, 2, 0)

        self.humidity_label = QLabel("Humidity: ", self)
        layout.addWidget(self.humidity_label, 3, 0)

        self.wind_label = QLabel("Wind Speed: ", self)
        layout.addWidget(self.wind_label, 4, 0)

        # Weather Icon
        self.icon_label = QLabel(self)
        layout.addWidget(self.icon_label, 1, 1, 4, 1, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def get_weather(self, city):
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        try:
            response = requests.get(BASE_URL, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.exceptions.RequestException:
            return None

    def display_weather(self):
        city = self.city_input.text()
        weather_data = self.get_weather(city)

        if weather_data:
            temperature = weather_data['main']['temp']
            weather_description = weather_data['weather'][0]['description']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']

            # Update labels
            self.temp_label.setText(f"Temperature: {temperature}°C")
            self.desc_label.setText(f"Condition: {weather_description.capitalize()}")
            self.humidity_label.setText(f"Humidity: {humidity}%")
            self.wind_label.setText(f"Wind Speed: {wind_speed} m/s")

            # Load weather icon
            icon_name = weather_data['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon_name}@2x.png"
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(icon_url).content)
            self.icon_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        else:
            QMessageBox.critical(self, "Error", "City not found or API error.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())