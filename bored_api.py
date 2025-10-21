import requests

bored_api_url = "https://www.boredapi.com/api/activity/"

def get_activity():
    response = requests.get(bored_api_url)
    if response.status_code == 200:
        data = response.json()
        activity = data.get('activity', 'No Activity')
        return activity
    else:
        return "Could not retrieve activity data."


while True:    
    user_input = input("Type 'bored' to get an activity suggestion or 'exit' to quit: ").strip().lower()
    if user_input == 'bored':
        activity = get_activity()
        print(f"Suggested Activity: {activity}")
    elif user_input == 'exit':
        print("Goodbye!")
        break   