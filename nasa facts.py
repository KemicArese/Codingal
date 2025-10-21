import requests

nasa_url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"

def get_nasa_apod_fact():
    response = requests.get(nasa_url)
    
    if response.status_code == 200:
        data = response.json()
        title = data.get('title', 'No Title')
        date = data.get('date', 'No Date')
        explanation = data.get('explanation', 'No Explanation')
        
        fact = (f"Title: {title}\nDate: {date}\nExplanation: {explanation}")
        return fact
    else:
        return "Could not retrieve NASA APOD data."
    
if __name__ == "__main__":
    print(get_nasa_apod_fact())