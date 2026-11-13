
from poke_env.battle import AbstractBattle, Pokemon

from players.heuristic.utils.pokemon_role import PokemonRole
from players.heuristic.utils.utils import calculate_pokemon_role
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
        opponent_tracker = self.opponent_trackers[opponent_pokemon.species]
        
        self._determine_role(opponent_pokemon, opponent_tracker)
        self._determine_items(opponent_tracker)
        
        self.previous_opponent_species = species


    def _determine_role(self, opponent_pokemon: Pokemon, opponent_tracker: OpponentTracker):
        """
            Try to define the pokemon's role in the team (whether its a sweeper, staller or bulky)
        """
        if not opponent_tracker.role is None:
            return
        
        opponent_tracker.role = calculate_pokemon_role(opponent_pokemon)
        
    def _determine_items(self, opponent_tracker: OpponentTracker):
        if opponent_tracker.item_held != "unknown_item":
            return
        
        if opponent_tracker.role == PokemonRole.DEFENSIVE:
            opponent_tracker.item_probs = {
                "heavy_duty_boots": 0.50,
                "rocky_helmet": 0.30,
                "assault_vest": 0.20,
            }
        elif opponent_tracker.role == PokemonRole.OFFENSIVE:
            opponent_tracker.item_probs = {
                "choice_scarf": 0.40,
                "choice_band": 0.30,
                "focus_sash": 0.30,
            }
        else:
            opponent_tracker.item_probs = {
                "heavy_duty_boots": 0.60,
                "assault_vest": 0.40,
            }