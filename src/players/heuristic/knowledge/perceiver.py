
from poke_env.battle import AbstractBattle, MoveCategory, Pokemon

from players.heuristic.knowledge import PokemonRole
from players.heuristic.knowledge.opponent_tracker import OpponentTracker


class Perceiver:
    def __init__(self):
        self.opponent_trackers: dict[str, OpponentTracker] = {}
        self.previous_opponent_species: str | None = None

    
    def update(self, battle: AbstractBattle):
        opponent_pokemon: Pokemon = battle.opponent_active_pokemon
        species = opponent_pokemon.species

        if not species in self.opponent_trackers:
            self.opponent_trackers[species] = OpponentTracker(species)
        active_pokemon_tracker = self.opponent_trackers[species]
        
        active_pokemon_tracker.update_facts(opponent_pokemon)
        
        self._determine_role(opponent_pokemon)
        
        self.previous_opponent_species = opponent_pokemon


    def _determine_role(self, opponent_pokemon: Pokemon):
        """
            Try to define the pokemon's role in the team (whether its a sweeper or staller)
        """
        opponent_tracker = self.opponent_trackers[opponent_pokemon.species]

        status_moves = 0
        offensive_moves = 0
        for move in opponent_tracker.moves:
            if move.category == MoveCategory.STATUS:
                status_moves += 1
            else:
                offensive_moves += 1

        if status_moves >= 2:
            opponent_tracker.role = PokemonRole.STALL
        elif offensive_moves >= 3:
            opponent_tracker.role = PokemonRole.SWEEP
