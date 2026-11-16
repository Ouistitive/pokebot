
from poke_env.battle import AbstractBattle, Pokemon

from players.heuristic.knowledge.knowledge import Knowledge
from players.heuristic.knowledge.pokemon_beliefs import PokemonBeliefs
from players.heuristic.utils.pokemon_role import PokemonRole
from players.heuristic.utils.utils import calculate_pokemon_role


class Perceiver:
    def __init__(self):
        pass

    
    def update(self, battle: AbstractBattle, knowledge: Knowledge):
        opponent_pokemon: Pokemon = battle.opponent_active_pokemon
        species = opponent_pokemon.species
        pokemon_beliefs = knowledge.pokemon_beliefs
        
        if not species in pokemon_beliefs:
            pokemon_beliefs[species] = PokemonBeliefs(species)
            
        active_pokemon_beliefs = pokemon_beliefs[species]
        active_pokemon_beliefs.update_facts(opponent_pokemon)
        
        self._determine_role(opponent_pokemon, active_pokemon_beliefs)
        self._determine_items(active_pokemon_beliefs)
        
        knowledge.previous_opponent_species = opponent_pokemon.species


    def _determine_role(self, opponent_pokemon: Pokemon, active_pokemon_beliefs: PokemonBeliefs):
        """
            Try to define the pokemon's role in the team (whether its a sweeper, staller or bulky)
        """
        if not active_pokemon_beliefs.role is None:
            return
        
        active_pokemon_beliefs.role = calculate_pokemon_role(opponent_pokemon)
        
    def _determine_items(self, active_pokemon_beliefs: PokemonBeliefs):
        if active_pokemon_beliefs.is_item_confirmed():
            return
        
        if active_pokemon_beliefs.role == PokemonRole.DEFENSIVE:
            active_pokemon_beliefs.item_probs = {
                "heavy_duty_boots": 0.50,
                "rocky_helmet": 0.30,
                "assault_vest": 0.20,
            }
        elif active_pokemon_beliefs.role == PokemonRole.OFFENSIVE:
            active_pokemon_beliefs.item_probs = {
                "choice_scarf": 0.40,
                "choice_band": 0.30,
                "focus_sash": 0.30,
            }
        else:
            active_pokemon_beliefs.item_probs = {
                "heavy_duty_boots": 0.60,
                "assault_vest": 0.40,
            }