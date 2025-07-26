import re, random
from colorama import Fore, init

# Initialize colorama (autoreset ensures each print resets after use)
init(autoreset=True)

# Destination & joke data
destinations = {
    "beaches": ["Bali", "Maldives", "Phuket"],
    "mountains": ["Swiss Alps", "Rocky Mountains", "Himalayas"],
    "cities": ["Tokyo", "Paris", "New York"]
}
jokes = [
    "Why don't programmers like nature? Too many bugs!",
    "Why did the computer go to the doctor? Because it had a virus!",
    "Why do travelers always feel warm? Because of all their hot spots!"
]

# Helper function to normalize user input (remove extra spaces, make lowercase)
def normalize_input(text):
    return re.sub(r"\s+", " ", text.strip().lower())

# Provide travel recommendations (recursive if user rejects suggestions)

def recommend_destination():
    print(Fore.CYAN + "Welcome to the Travel Recommendation System!")
    print("We have three types of destinations for you:")
    print("1. Beaches")
    print("2. Mountains")
    print("3. Cities")
    
    suggestion = random.choice(list(destinations.keys()))

    choice = input(f'How about visiting {suggestion}): ')

    if normalize_input(choice) in ["yes", "y"]:
        print(Fore.GREEN + f"Great choice! Here are some {suggestion} you might like:")
        for place in destinations[suggestion]:
            print(Fore.YELLOW + f"- {place}")

    elif normalize_input(choice) in ["no", "n"]:
        print(Fore.RED + "No problem! Let's try something else.")
        recommend_destination()

    else:
        print(Fore.RED + "Lets try that again. ")
        recommend_destination()


def packing_tips():
    print(Fore.CYAN + "TravelBot: Where to?")
    location = normalize_input(input(Fore. YELLOW + "You: "))
    print(Fore.CYAN + "TravelBot: How many days?")
    days = input(Fore.YELLOW + "You: ")
    print(Fore.GREEN + f"TravelBot: Packing tips for {days} days in {location}:")
    print(Fore.GREEN + "- Pack versatile clothes.")
    print(Fore.GREEN + "- Bring chargers/adapters.")
    print(Fore.GREEN + "- Check the weather forecast.")

#Tell a random joke
def tell_joke():
    print(Fore.YELLOW + f"TravelBot: {random.choice(jokes)}")


#Display help menu
def show_help():
    print(Fore.MAGENTA + "\nI can:")
    print(Fore.GREEN+ "- Suggest travel spots (say 'recommendation')")
    print(Fore.GREEN + " Offer packing tips (say 'packing')")
    print(Fore.GREEN + "Tell a joke (say 'joke')")
    print(Fore.CYAN + "Type 'exit' or 'bye to end.\n")

def chat():
    print(Fore.CYAN + "Hello! I'm TravelBot.")
    name = input(Fore.YELLOW + "Your name? ")
    print(Fore.GREEN + f"Nice to meet you, {name}!")

    show_help()

    while True:
        user_input = input(Fore.YELLOW + f"{name}: ")
        user_input = normalize_input(user_input)

        if "recommend" in user_input or "suggest" in user_input:
            recommend_destination()
        elif "pack" in user_input or "packing" in user_input:
            packing_tips()
        elif "joke" in user_input or "funny" in user_input:
            tell_joke()
        elif "help" in user_input:
            show_help()
        elif "exit" in user_input or "bye" in user_input:
            print(Fore.CYAN + "TravelBot: Safe travels! Goodbye!")
            break
        else:
            print(Fore.RED + "TravelBot: Could you rephrase?")

# Run the chatbot
if __name__ == "__main__":
    chat()
