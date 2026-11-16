
from poke_env.battle import Pokemon

from config.translator import translate_pokemon_species
from players.heuristic.utils.pokemon_role import PokemonRole


class PokemonBeliefs:
    def __init__(self, species: str):
        self.species: str | None = species
        self.role: PokemonRole | None = None
        self.item_probs: dict[str, float] = {}
        

    def update_facts(self, opponent_pokemon: Pokemon):
        """
            Update facts for the active opponent pokemon
        """
        item = opponent_pokemon.item
        
        if item != "unknown_item":
            self.item_probs = { item: 1.0 }
        

    def is_item_confirmed(self):
        return 1.0 in self.item_probs.values()


    def __repr__(self):
        return f"OpponentTracker(species='{translate_pokemon_species(self.species)}', role={self.role}, item={self.item_probs})"