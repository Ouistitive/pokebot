import json


translator_cache = {}

def translate_pokemon_species(pokemon_species: str) -> str:
    index = -1
    
    if pokemon_species in translator_cache:
        return translator_cache[pokemon_species]
    
    with open('pokemon_data/us.json', 'r', encoding='utf-8') as file:
        data: list[str] = json.load(file)
        index = next((i for i, x in enumerate(data) if x.lower() == pokemon_species.lower()), None)
    
    if index is None:
        return pokemon_species
    
    with open("pokemon_data/fr.json", 'r', encoding='utf-8') as file:
        data: list[str] = json.load(file)
        translator_cache[pokemon_species] = data[index]
        
    return data[index]