
from poke_env.battle import AbstractBattle, Weather


class PokemonBelief:
    def __init__(self):
        self.species: str = ""
        self.item_probs: dict[str, float] = {}
        self.role: str | None = None


class Knowledge:    
    def __init__(self):
        self.beliefs: dict[str, PokemonBelief] = {}
    
    def update(self, battle: AbstractBattle):
        
        pass