
from poke_env.battle import AbstractBattle

from poke_env.battle import AbstractBattle, Move, MoveCategory, Pokemon

from config.translator import translate_pokemon_species
from players.heuristic.knowledge.knowledge import Knowledge
from players.heuristic.knowledge.opponent_tracker import OpponentTracker
from players.heuristic.think.scorers.damage_calculator import calculate_damage_opponent
from players.heuristic.think.scorers.switch_scorer import calculate_switch_score
from players.heuristic.utils.pokemon_role import PokemonRole
from players.max_damage.damage import calculate_damage


class Deliberator:
    def __init__(self, knowledge: Knowledge):
        self.knowledge = knowledge

    
    def deliberate(self, battle: AbstractBattle):
        active_pokemon: Pokemon = battle.active_pokemon
        opponent_pokemon: Pokemon = battle.opponent_active_pokemon
        opponent_tracker = self.knowledge.opponent_trackers[opponent_pokemon.species]
        
        moves = [move for move in battle.available_moves]
        available_switches: list[Pokemon] = battle.available_switches
        
        scored_actions = []
        
        for move in moves:
            score = self._evaluate_move(move, active_pokemon, opponent_pokemon)
            scored_actions.append((score, {"type": "move", "action": move}))
        
        for switch_option in available_switches:
            score = self._evaluate_switch(active_pokemon, switch_option, opponent_pokemon, opponent_tracker)
            scored_actions.append((score, {"type": "switch", "action": switch_option}))
        
        scored_actions.sort(key=lambda x: x[0], reverse=True)
        
        print(translate_pokemon_species(active_pokemon.species), f"({active_pokemon.current_hp_fraction}) VS", translate_pokemon_species(opponent_pokemon.species), f"({opponent_tracker.current_hp})")
        print("--- OPTIONS EVALUATED ---")
        for score, action_info in scored_actions:
            name = action_info["action"].id if action_info["type"] == "move" else translate_pokemon_species(action_info["action"].species)
            print(f"[{action_info['type'].upper()}] {name} -> Score : {score}")
        
        return scored_actions[0][1]["action"]
        
    
    def _evaluate_move(self, move: Move, active: Pokemon, opponent: Pokemon) -> float:
        opponent_tracker = self.knowledge.opponent_trackers[opponent.species]
        
        damage = calculate_damage(move, active, opponent)
        damage_ratio = damage / opponent.max_hp
        score = damage_ratio * 100.0
        
        if active.base_stats["spe"] > opponent_tracker.statistics["spe"] or move.priority > 1:
            score += 15.0
        else:
            score -= 15.0
        
        if score >= opponent_tracker.current_hp:
            score += 50.0
        else:
            if opponent_tracker.role == PokemonRole.DEFENSIVE and damage_ratio <= 0.15:
                score -= 30.0
            if opponent_tracker.role == PokemonRole.BULK and damage_ratio <= 0.4:
                score -= 20.0
        
        return score


    def _evaluate_switch(self, active_pokemon: Pokemon, pokemon_switch: Pokemon, opponent: Pokemon, opponent_tracker: OpponentTracker) -> float:
        score = 75.0
        pokemon_moves = [move for move in pokemon_switch.moves.values()]
        opponent_moves = opponent_tracker.moves
        
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

    def __init__(self):
        pass
    
    def deliberate(self, battle: AbstractBattle, knowledge: Perceiver):
        pass