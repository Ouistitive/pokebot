

from poke_env.battle import Move, Pokemon

from players.heuristic.knowledge.knowledge import Knowledge
from players.heuristic.knowledge.pokemon_beliefs import PokemonBeliefs
from players.heuristic.think.scorers.damage_calculator import calculate_damage
from players.heuristic.utils.pokemon_role import PokemonRole


def calculate_offensive_move_score(move: Move, active: Pokemon, opponent: Pokemon, opponent_beliefs: PokemonBeliefs, knowledge: Knowledge):
    damage_ratio = 0.0
    score = 0.0
    
    # Use previous damage taken by ennemy if known or else, calculate approximatively
    if move == knowledge.previous_pokemon_move_used:
        damage_ratio = knowledge.last_opponent_hp - opponent.current_hp_fraction
    else:
        damage = calculate_damage(move, active, opponent)
        damage_ratio = damage / opponent.max_hp
        
    effective_damage_ratio = min(damage_ratio, opponent.current_hp_fraction)
    score = effective_damage_ratio * 100.0 + damage_ratio * 25.0
    
    if active.base_stats["spe"] > opponent.base_stats["spe"] or move.priority >= 1:
        score += 15.0
    else:
        score -= 15.0
    
    if damage_ratio >= opponent.current_hp_fraction:
        score += 110.0
        if move.priority >= 1:
            score += 40.0
            
        score -= _calculate_move_safety_penalty(move)
    else:
        if opponent_beliefs.role == PokemonRole.DEFENSIVE and damage_ratio <= 0.15:
            score -= 30.0
        if opponent_beliefs.role == PokemonRole.BULKY and damage_ratio <= 0.25:
            score -= 20.0
        if opponent_beliefs.role == PokemonRole.OFFENSIVE and damage_ratio <= 0.35:
            score -= 20.0
        
    return score


def calculate_self_switch_move_score(move: Move, active: Pokemon, opponent: Pokemon, opponent_beliefs: PokemonBeliefs, opponent_team: list[PokemonBeliefs], knowledge: Knowledge) -> float:
    score = 0.0
    best_move, best_move_score = determine_pokemon_best_move_with_score(active, opponent)
    
    if opponent.current_hp_fraction <= 0.2:
        if best_move != move:
            score -= 10.0
        else:
            score += 10.0
    
    damage = calculate_damage(move, active, opponent)
    if damage * 1.15 <= best_move_score:
        score += 10.0
    
    if opponent_beliefs.role == PokemonRole.DEFENSIVE:
        score += 10.0
    
    return calculate_offensive_move_score(move, active, opponent, opponent_beliefs, knowledge)


def determine_pokemon_best_move_with_score(pokemon: Pokemon, opponent: Pokemon) -> tuple[Move, int]:
    moves = [move for move in pokemon.moves.values()]
    best_move = moves[0]
    best_score = 0

    for move in moves:
        score = calculate_damage(move, pokemon, opponent)
        if score > best_score:
            best_move = move
            best_score = score
    
    return (best_move, best_score)


def _calculate_move_safety_penalty(move: Move) -> float:
    penalty = 0.0

    if move.accuracy is not None and move.accuracy < 100:
        penalty += (100 - move.accuracy) * 0.4
    
    if move.recoil != 0.0:
        penalty += 8.0
    if move.self_boost is not None:
        for _, change in move.self_boost.items():
            if change < 0:
                penalty += abs(change) * 6.0

    return penalty