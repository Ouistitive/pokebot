

from players.heuristic.knowledge.pokemon_beliefs import PokemonBeliefs


class Knowledge:
    def __init__(self):
        self.pokemon_beliefs: dict[str, PokemonBeliefs] = {}
        self.previous_opponent_species: str | None = None
        