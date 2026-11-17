

from poke_env.battle import Move, Pokemon

from players.heuristic.knowledge.pokemon_beliefs import PokemonBeliefs
from players.heuristic.think.scorers.damage_calculator import calculate_damage
from players.heuristic.utils.pokemon_role import PokemonRole


def calculate_offensive_move_score(move: Move, active: Pokemon, opponent: Pokemon, opponent_beliefs: PokemonBeliefs):
    damage = calculate_damage(move, active, opponent)
    damage_ratio = damage / opponent.max_hp
    score = damage_ratio * 100.0
    
    if active.base_stats["spe"] > opponent.base_stats["spe"] or move.priority >= 1:
        score += 15.0
    else:
        score -= 15.0
    
    if damage_ratio >= opponent.current_hp_fraction:
        score += 50.0
        if move.priority >= 1:
            score += 150.0
    else:
        if opponent_beliefs.role == PokemonRole.DEFENSIVE and damage_ratio <= 0.15:
            score -= 30.0
        if opponent_beliefs.role == PokemonRole.BULKY and damage_ratio <= 0.25:
            score -= 20.0
        if opponent_beliefs.role == PokemonRole.OFFENSIVE and damage_ratio <= 0.35:
            score -= 20.0
    
    return score