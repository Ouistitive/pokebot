
import logging

from poke_env.battle import AbstractBattle, Move, Pokemon

from config.translator import translate_pokemon_species
from players.heuristic.knowledge.knowledge import Knowledge
from players.heuristic.knowledge.pokemon_beliefs import PokemonBeliefs
from players.heuristic.think.scorers.damage_calculator import calculate_damage, calculate_damage_opponent
from players.heuristic.think.scorers.switch_scorer import calculate_switch_score
from players.heuristic.utils.pokemon_role import PokemonRole

logger = logging.getLogger(__name__)


class Deliberator:
    def __init__(self):
        pass
    
    def deliberate(self, battle: AbstractBattle, knowledge: Knowledge):
        active_pokemon: Pokemon = battle.active_pokemon
        opponent_pokemon: Pokemon = battle.opponent_active_pokemon
        opponent_beliefs: PokemonBeliefs = knowledge.pokemon_beliefs[opponent_pokemon.species]
        
        moves = [move for move in battle.available_moves]
        available_switches: list[Pokemon] = battle.available_switches
        
        scored_actions = []
        
        for move in moves:
            score = self._evaluate_move(move, active_pokemon, opponent_pokemon, opponent_beliefs)
            scored_actions.append((score, {"type": "move", "action": move}))
        
        for switch_option in available_switches:
            score = self._evaluate_switch(active_pokemon, switch_option, opponent_pokemon, opponent_beliefs)
            scored_actions.append((score, {"type": "switch", "action": switch_option}))
        
        scored_actions.sort(key=lambda x: x[0], reverse=True)
        
        logger.debug(
            "%s (%s) VS %s (%s)",
            translate_pokemon_species(active_pokemon.species),
            active_pokemon.current_hp_fraction,
            translate_pokemon_species(opponent_pokemon.species),
            opponent_pokemon.current_hp_fraction,
        )
        logger.debug("--- OPTIONS EVALUATED ---")
        for score, action_info in scored_actions:
            name = action_info["action"].id if action_info["type"] == "move" else translate_pokemon_species(action_info["action"].species)
            logger.debug("[%s] %s -> Score : %s", action_info["type"].upper(), name, score)
        
        return scored_actions[0][1]["action"]
        
    
    def _evaluate_move(self, move: Move, active: Pokemon, opponent: Pokemon, opponent_beliefs: PokemonBeliefs) -> float:        
        damage = calculate_damage(move, active, opponent)
        damage_ratio = damage / opponent.max_hp
        score = damage_ratio * 100.0
        
        if active.base_stats["spe"] > opponent.base_stats["spe"]:
            score += 15.0
        else:
            score -= 15.0
        
        if damage_ratio >= opponent.current_hp_fraction:
            score += 50.0
        else:
            if opponent_beliefs.role == PokemonRole.DEFENSIVE and damage_ratio <= 0.15:
                score -= 30.0
            if opponent_beliefs.role == PokemonRole.BULKY and damage_ratio <= 0.4:
                score -= 20.0
        
        return score


    def _evaluate_switch(self, active_pokemon: Pokemon, pokemon_switch: Pokemon, opponent: Pokemon, opponent_beliefs: PokemonBeliefs) -> float:
        score = 75.0
        pokemon_moves = [move for move in pokemon_switch.moves.values()]
        opponent_moves = [move for move in opponent.moves.values()]
        
        score -= calculate_switch_score(active_pokemon, opponent)
        score += calculate_switch_score(pokemon_switch, opponent)
        
        for move in opponent_moves:
            damage = calculate_damage_opponent(move, pokemon_switch, opponent)
            damage_ratio = damage / pokemon_switch.max_hp
            if damage_ratio <= 0.2:
                score += 20
            else:
                score -= 20
        
        for move in pokemon_moves:
            damage = calculate_damage(move, pokemon_switch, opponent)
            damage_ratio = damage / opponent.max_hp
            if damage_ratio >= 0.5:
                score += 20
            else:
                score -= 20
        
        return score
