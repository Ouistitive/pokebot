
import logging

from poke_env.battle import AbstractBattle, Move, MoveCategory, Pokemon

from config.translator import translate_pokemon_species
from players.heuristic.knowledge.knowledge import Knowledge
from players.heuristic.knowledge.pokemon_beliefs import PokemonBeliefs
from players.heuristic.think.scorers.damage_calculator import calculate_damage, calculate_damage_opponent
from players.heuristic.think.scorers.damage_scorer import calculate_offensive_move_score, calculate_self_switch_move_score, determine_pokemon_best_move_with_score
from players.heuristic.think.scorers.status_scorer import calculate_boost_move_score, calculate_heal_move_score, calculate_status_move_score
from players.heuristic.think.scorers.switch_scorer import calculate_switch_score
from players.heuristic.utils.pokemon_role import PokemonRole

logger = logging.getLogger(__name__)


class Deliberator:
    def __init__(self):
        pass
    
    def deliberate(self, battle: AbstractBattle, knowledge: Knowledge):
        action = self._do_default_action(battle)
        if action is not None:
            return action
        
        active_pokemon: Pokemon = battle.active_pokemon
        opponent_pokemon: Pokemon = battle.opponent_active_pokemon
        opponent_beliefs: PokemonBeliefs = knowledge.pokemon_beliefs[opponent_pokemon.species]
        
        moves = [move for move in battle.available_moves]
        available_switches: list[Pokemon] = battle.available_switches

        scored_actions = []
        
        for move in moves:
            score = self._evaluate_move(
                knowledge,
                move, 
                active_pokemon, 
                opponent_pokemon, 
                opponent_beliefs, 
                [mon for mon in battle.opponent_team.values()]
            )
            scored_actions.append((score, {"type": "move", "action": move}))
        
        for switch_option in available_switches:
            score = self._evaluate_switch(active_pokemon, switch_option, opponent_pokemon, opponent_beliefs)
            scored_actions.append((score, {"type": "switch", "action": switch_option}))
        
        scored_actions.sort(key=lambda x: x[0], reverse=True)
        self._log_evaluated_moves(active_pokemon, opponent_pokemon, scored_actions)
        
        return scored_actions[0][1]["action"]
        
    
    def _evaluate_move(self, knowledge: Knowledge, move: Move, active: Pokemon, opponent: Pokemon, opponent_beliefs: PokemonBeliefs, opponent_team: list[Pokemon]) -> float:        
        score = 0.0
        
        if move.base_power == 0.0:
            if move.heal > 0:
                score = calculate_heal_move_score(move, active, opponent)
            elif move.boosts:
                score = calculate_boost_move_score(move, active, opponent_beliefs, opponent_team)
            else:
                
                score = calculate_status_move_score(move, active, opponent)

        else:
            if move.self_switch:
                score = calculate_self_switch_move_score(move, active, opponent, opponent_beliefs, opponent_team, knowledge)
            else:
                score = calculate_offensive_move_score(move, active, opponent, opponent_beliefs, knowledge)

        accuracy = move.accuracy if move.accuracy is not None else 1.0
        # Avoid punishing too severly when it has low accuracy
        if accuracy <= 0.9:
            accuracy = min(1.0, accuracy + 0.1)
    
        return score * accuracy * move.expected_hits


    def _evaluate_switch(self, active_pokemon: Pokemon, pokemon_switch: Pokemon, opponent: Pokemon, opponent_beliefs: PokemonBeliefs) -> float:
        score = 40.0
        switching_cost = 20.0
        
        opponent_moves = [move for move in opponent.moves.values()]
        
        # If the active pokemon is stil alive, evaluate based on its types
        if active_pokemon is not None and not active_pokemon.fainted:
            score -= calculate_switch_score(active_pokemon, opponent)
        score += calculate_switch_score(pokemon_switch, opponent)
        
        for move in opponent_moves:
            damage = calculate_damage_opponent(move, pokemon_switch, opponent)
            damage_ratio = damage / pokemon_switch.max_hp
            if damage_ratio <= 0.2:
                score += 15.0
            else:
                score -= 15.0

        if opponent.current_hp_fraction <= 0.2:
            score -= 30.0

        best_active_move = determine_pokemon_best_move_with_score(active_pokemon, opponent)
        best_switch_move = determine_pokemon_best_move_with_score(pokemon_switch, opponent)     
        
        if best_switch_move[1] > best_active_move[1] + switching_cost:
            score += 40.0
        else:
            score -= 60.0
        
        if active_pokemon is not None and not active_pokemon.fainted:
            total_boosts = sum(active_pokemon.boosts.values()) if active_pokemon.boosts else 0
            if total_boosts > 0:
                score -= (total_boosts * 15.0)
        
        return score


    def _do_default_action(self, battle: AbstractBattle):
        if battle.active_pokemon is None or battle.opponent_active_pokemon is None:
            return self.choose_random_singles_move(battle)

        # Forced switch with no candidate, or no legal action at all
        if battle.force_switch and not battle.available_switches:
            return self.choose_random_singles_move(battle)
        if not battle.available_moves and not battle.available_switches:
            return self.choose_random_singles_move(battle)
        
        return None


    def _log_evaluated_moves(self, active: Pokemon, opponent: Pokemon, scored_actions):
        logger.debug(
            "%s (%s) VS %s (%s)",
            translate_pokemon_species(active.species),
            active.current_hp_fraction,
            translate_pokemon_species(opponent.species),
            opponent.current_hp_fraction,
        )
        logger.debug("--- OPTIONS EVALUATED ---")
        for score, action_info in scored_actions:
            name = action_info["action"].id if action_info["type"] == "move" else translate_pokemon_species(action_info["action"].species)
            logger.debug("[%s] %s -> Score : %s", action_info["type"].upper(), name, score)