import requests

url = "https://api.nasa.gov/insight_weather/?api_key=DEMO_KEY&feedtype=json&ver=1.0"

def get_nasa_weather():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        sol_keys = data.get('sol_keys', [])
        if sol_keys:
            latest_sol = sol_keys[-1]
            sol_data = data.get(latest_sol, {})
            temperature = sol_data.get('AT', {}).get('av', 'No Data')
            wind_speed = sol_data.get('HWS', {}).get('av', 'No Data')
            pressure = sol_data.get('PRE', {}).get('av', 'No Data')
            return {
                'sol': latest_sol,
                'temperature': temperature,
                'wind_speed': wind_speed,
                'pressure': pressure
            }
        else:
            return "No sol data available."
    else:
        return "Could not retrieve NASA weather data."
while True:
    user_input = input("Type 'nasa' to get the latest Mars weather or 'q' to quit: ").strip().lower()
    if user_input == 'nasa':
        weather = get_nasa_weather()
        if isinstance(weather, dict):
            print(f"Latest Sol: {weather['sol']}")
            print(f"Average Temperature: {weather['temperature']} °C")
            print(f"Average Wind Speed: {weather['wind_speed']} m/s")
            print(f"Average Pressure: {weather['pressure']} Pa")
        else:
            print(weather)
    elif user_input == 'q':
        print("Goodbye!")
        break
    else:
        print("Invalid input. Please try again.")
