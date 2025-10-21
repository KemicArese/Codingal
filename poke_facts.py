import requests
import random

url = "https://pokeapi.co/api/v2/pokemon/"
def get_random_pokemon_fact():
    pokemon_id = random.randint(1, 1025)
    
    # Fetch Pokémon data from the API
    response = requests.get(f"{url}{pokemon_id}")
    
    if response.status_code == 200:
        data = response.json()
        name = data['name'].capitalize()
        height = data['height'] / 10  # Convert decimeters to meters
        weight = data['weight'] / 10  # Convert hectograms to kilograms
        types = ', '.join([t['type']['name'].capitalize() for t in data['types']])
        
        fact = (f"Name: {name}\nHeight: {height} m\nWeight: {weight} kg\nType(s): {types}")
        return fact
    else:
        return "Could not retrieve Pokémon data."
    
if __name__ == "__main__":
    print(get_random_pokemon_fact())