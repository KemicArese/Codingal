import requests

def get_advice():
    url = "https://api.adviceslip.com/advice"
    response = requests.get(url)
    if response.status_code == 200:
        advice = response.json()
        return advice['slip']['advice']
    else:
        return "Failed to retrieve advice."
    

def main() :
    print("Welcome to the Advice Generator!")
    while True:
        user_input = input("Type 'advice' to get advice or 'exit' to quit: ").strip().lower()
        if user_input in ['exit', 'quit']:
            print("Goodbye!")
            break
        advice = get_advice()
        print(advice)

if __name__ == "__main__":
    main()