import requests

def get_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    if response.status_code == 200:
        joke = response.json()
        return f"{joke['setup']} - {joke['punchline']}"
    else:
        return "Failed to retrieve a joke."
    

def main() :
    print("Welcome to the Joke Generator!")
    while True:
        user_input = input("Type 'joke' to get a joke or 'exit' to quit: ").strip().lower()
        if user_input in ['exit', 'quit']:
            print("Goodbye!")
            break
        joke = get_joke()
        print(joke)

if __name__ == "__main__":
    main()