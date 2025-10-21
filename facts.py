import requests

url = "https://uselessfacts.jsph.pl/random.json?language=en"

def get_random_fact():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data["text"])
    else:
        print("Error:", response.status_code)

while True:
    print("\nRandom Fact:")
    print("Press enter to get a new fact or type 'q' to quit.")
    user_input = input()
    if user_input.lower() == 'q':
        break
    
    get_random_fact()