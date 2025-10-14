import requests

def get_random_cat_fact():
    url = "https://catfact.ninja/fact"
    response = requests.get(url)
    if response.status_code == 200:
        fact = response.json()
        return fact['fact']
    else:
        return "Failed to retrieve a cat fact."
    
def main() :
    print("Welcome to the Cat Fact Generator!")
    while True:
        user_input = input("Type 'fact' to get a cat fact or 'exit' to quit: ").strip().lower()
        if user_input in ['exit', 'quit']:
            print("Goodbye!")
            break
        fact = get_random_cat_fact()
        print(fact)

if __name__ == "__main__":
    main()