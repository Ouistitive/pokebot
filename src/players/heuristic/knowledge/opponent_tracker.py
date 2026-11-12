
from poke_env.battle import Move, Pokemon

from players.heuristic.utils.pokemon_role import PokemonRole


class OpponentTracker:
    def __init__(self, species: str):
        self.species: str = species

        # Facts / Observables
        self.current_hp: float = 1.0
        self.status = None
        self.moves: list[Move] = []
        self.statistics: dict[str, int | None] = {
            "hp": None,
            "atk": None,
            "def": None,
            "spa": None,
            "spd": None,
            "spe": None,
        }
        self.item_held: str = "unknown_item"
        self.ability: str | None = None
        
        # Agent's beliefs
        self.item_probs: dict[str, float] = {}
        self.role: PokemonRole | None = None
        
    
    def update_facts(self, opponent_pokemon: Pokemon):
        """
            Update facts for the active opponent pokemon
            Facts updated: known moves, base stats
        """
        self.current_hp = opponent_pokemon.current_hp_fraction
        self.moves = [move for _, move in opponent_pokemon.moves.items()]
        self.status = opponent_pokemon.status
        self.statistics = opponent_pokemon.base_stats
        self.item_held = opponent_pokemon.item
        self.ability = opponent_pokemon.ability
        
        if self.item_held != "unknown_item":
            self.item_probs = { self.item_held: 1.0 }
    

    def __repr__(self):
        return f"OpponentTracker(species='{self.species}', hp={self.current_hp}, role={self.role}, item={self.item_held}, ability={self.ability})"
