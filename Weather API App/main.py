import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import scrolledtext
import requests

GEONAMES_USERNAME = "Mayur_Kalwar"
OPENWEATHERMAP_API_KEY = "88c9c008a82ddf46231b1d89703b4a53"

def get_weather():
    city = city_entry.get()

    if not city:
        messagebox.showwarning("Warning", "Please enter a city.")
        return

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": OPENWEATHERMAP_API_KEY, "units": "metric"}

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            city_name = data['name']
            country_name = data['sys']['country']

            weather_info = f"Weather in {city_name}, {country_name}: {weather_description}\nTemperature: {temperature}°C"
            weather_label.config(text=weather_info)

        else:
            messagebox.showerror("Error", f"Error: {data['message']}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def get_forecast():
    city = city_entry.get()
    forecast_type = forecast_type_var.get()

    if not city:
        messagebox.showwarning("Warning", "Please enter a city.")
        return

    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": OPENWEATHERMAP_API_KEY, "units": "metric"}

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            forecast_info = ""

            if forecast_type == "Hourly":
                for entry in data['list']:
                    timestamp = entry['dt_txt']
                    temperature = entry['main']['temp']
                    weather_description = entry['weather'][0]['description']
                    forecast_info += f"{timestamp}: {weather_description}, Temperature: {temperature}°C\n"

            elif forecast_type == "Daily":
                for entry in data['list'][::8]:  # Show every 8th entry for daily forecast
                    timestamp = entry['dt_txt']
                    temperature = entry['main']['temp']
                    weather_description = entry['weather'][0]['description']
                    forecast_info += f"{timestamp}: {weather_description}, Temperature: {temperature}°C\n"

            elif forecast_type == "Monthly":
                monthly_data = {}
                for entry in data['list']:
                    date = entry['dt_txt'][:7]
                    if date not in monthly_data:
                        temperature = entry['main']['temp']
                        weather_description = entry['weather'][0]['description']
                        monthly_data[date] = f"{date}: {weather_description}, Temperature: {temperature}°C\n"

                for info in monthly_data.values():
                    forecast_info += info

            forecast_text.config(state=tk.NORMAL)
            forecast_text.delete(1.0, tk.END)
            forecast_text.insert(tk.END, forecast_info)
            forecast_text.config(state=tk.DISABLED)

        else:
            messagebox.showerror("Error", f"Error: {data['message']}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

root = tk.Tk()
root.title("Weather App")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.configure(bg="#00FFFF")  # Dark blue background color

frame = tk.Frame(root, bg="#3949AB", padx=20, pady=20)  # Indigo frame
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

city_label = tk.Label(frame, text="Enter City:", font=("Helvetica", 16), bg="#3949AB", fg="white")
city_label.grid(row=0, column=0, pady=10)

city_var = tk.StringVar()
city_entry = tk.Entry(frame, textvariable=city_var, font=("Helvetica", 12))
city_entry.grid(row=1, column=0, pady=10)

forecast_type_label = tk.Label(frame, text="Select Forecast Type:", font=("Helvetica", 16), bg="#3949AB", fg="white")
forecast_type_label.grid(row=2, column=0, pady=10)

forecast_types = ["Hourly", "Daily", "Monthly"]
forecast_type_var = tk.StringVar()
forecast_type_dropdown = ttk.Combobox(frame, textvariable=forecast_type_var, values=forecast_types, font=("Helvetica", 12), state="readonly")
forecast_type_dropdown.grid(row=3, column=0, pady=10)
forecast_type_dropdown.set(forecast_types[0])  # Set the first forecast type as the default value

get_weather_button = tk.Button(frame, text="Get Weather", command=get_weather, font=("Helvetica", 14), bg="#1976D2", fg="white")  # Dark blue button with white text
get_weather_button.grid(row=4, column=0, pady=10)

forecast_button = tk.Button(frame, text="Get Forecast", command=get_forecast, font=("Helvetica", 14), bg="#1976D2", fg="white")  # Dark blue button with white text
forecast_button.grid(row=5, column=0, pady=10)

forecast_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=10, font=("Helvetica", 12))
forecast_text.grid(row=6, column=0, pady=10)

weather_label = tk.Label(frame, text="", font=("Helvetica", 14), bg="#3949AB", fg="white")  # Indigo background for the weather info
weather_label.grid(row=7, column=0, pady=10)

root.mainloop()
