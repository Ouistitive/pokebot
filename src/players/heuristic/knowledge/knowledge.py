

from poke_env.battle import Move

from players.heuristic.knowledge.pokemon_beliefs import PokemonBeliefs


class Knowledge:
    def __init__(self):
        self.pokemon_beliefs: dict[str, PokemonBeliefs] = {}
        
        self.previous_opponent_species: str | None = None
        self.last_opponent_hp: float = 1.0
        self.previous_pokemon_move_used: Move | None = None