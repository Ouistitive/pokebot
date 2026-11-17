
import logging

from poke_env.battle import AbstractBattle, Pokemon

from config.translator import translate_pokemon_species
from players.heuristic.knowledge.knowledge import Knowledge
from players.heuristic.knowledge.pokemon_beliefs import PokemonBeliefs
from players.heuristic.utils.pokemon_role import PokemonRole
from players.heuristic.utils.utils import calculate_pokemon_role

logger = logging.getLogger(__name__)


class Perceiver:
    def __init__(self):
        pass

    
    def update(self, battle: AbstractBattle, knowledge: Knowledge):
        if battle.opponent_active_pokemon is None:
            return

        opponent: Pokemon = battle.opponent_active_pokemon
        species = opponent.species
        pokemon_beliefs = knowledge.pokemon_beliefs
        
        if not species in pokemon_beliefs:
            pokemon_beliefs[species] = PokemonBeliefs(species)
            
        active_pokemon_beliefs = pokemon_beliefs[species]
        active_pokemon_beliefs.update_facts(opponent)
        
        self._determine_role(opponent, active_pokemon_beliefs)
        self._determine_items(active_pokemon_beliefs)
        self._log_pokemon_turn(knowledge, battle.active_pokemon, opponent)
        
        knowledge.previous_opponent_species = opponent.species
        knowledge.last_opponent_hp = opponent.current_hp_fraction


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
            
    
    def _log_pokemon_turn(self, knowledge: Knowledge, active: Pokemon, opponent: Pokemon):
        if active and active.last_move:
            logger.info("%s uses: %s", translate_pokemon_species(active.species), active.last_move.id)
        
        if opponent and opponent.last_move:
            logger.info("%s uses: %s", translate_pokemon_species(opponent.species), opponent.last_move.id)

        if knowledge.previous_opponent_species and knowledge.previous_opponent_species != opponent.species:
            logger.info(
                "The opponent switched from %s to %s",
                translate_pokemon_species(knowledge.previous_opponent_species), 
                translate_pokemon_species(opponent.species)
            )
        else:
            hp_diff = knowledge.last_opponent_hp - opponent.current_hp_fraction
            if hp_diff > 0.001:
                logger.info("%s took %.1f%% HP", translate_pokemon_species(opponent.species), hp_diff * 100)
            elif hp_diff < -0.001:
                logger.info("%s healed %.1f%% HP", translate_pokemon_species(opponent.species), abs(hp_diff) * 100)