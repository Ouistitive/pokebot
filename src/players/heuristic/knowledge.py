
from enum import Enum

from poke_env.battle import AbstractBattle, MoveCategory, Pokemon, Weather


class PokemonRole(Enum):
    STALL = 1
    SWEEP = 2


class OpponentTracker:
    def __init__(self, species: str):
        self.species: str = species

        # Facts / Observables
        self.current_hp: float = 1.0
        self.status = None
        
        # Agent's beliefs
        self.item_probs: dict[str, float] = {}
        self.role: PokemonRole | None = None

    def __repr__(self):
        return f"OpponentTracker(species='{self.species}', hp={self.current_hp}, role={self.role})"


class Knowledge:
    def __init__(self):
        self.opponent_trackers: dict[str, OpponentTracker] = {}
        self.previous_opponent_species: str | None = None
        self.previous_opponent_hp: float = 1.0

    
    def update(self, battle: AbstractBattle):
        opponent_pokemon: Pokemon = battle.opponent_active_pokemon
        species = opponent_pokemon.species

        if not species in self.opponent_trackers:
            self.opponent_trackers[species] = OpponentTracker(species)

        self._determine_role(opponent_pokemon)

        self.previous_opponent_species = opponent_pokemon
        self.opponent_trackers[species].current_hp = opponent_pokemon.current_hp_fraction


    def _determine_role(self, opponent_pokemon: Pokemon):
        opponent_tracker = self.opponent_trackers[opponent_pokemon.species]

        status_moves = 0
        offensive_moves = 0
        for _, v in opponent_pokemon.moves.items():
            if v.category == MoveCategory.STATUS:
                status_moves += 1
            else:
                offensive_moves += 1

        if status_moves >= 2:
            opponent_tracker.role = PokemonRole.STALL
        elif offensive_moves >= 3:
            opponent_tracker.role = PokemonRole.SWEEP
