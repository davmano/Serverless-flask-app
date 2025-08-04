from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Put your key in .env or replace here directly

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    "city": data["name"],
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"].capitalize(),
                    "humidity": data["main"]["humidity"],
                    "wind": data["wind"]["speed"]
                }
            else:
                error = f"Could not find weather for '{city}'. Please check the city name."
        else:
            error = "City name cannot be empty."

    return render_template("index.html", weather=weather_data, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
