
from poke_env.battle import Move, MoveCategory, Pokemon


def calculate_damage_opponent(move: Move, pokemon: Pokemon, opponent: Pokemon) -> float:
    if move.base_power == 0:
        return 0.0

    if move.category == MoveCategory.PHYSICAL:
        opponent_base_atk = opponent.base_stats.get("atk", 100)
                
        # Exact stat value is unknown (may have EV repartition) so use a simplified def estimation
        opponent_atk_stat_estimation = (opponent_base_atk * 2) + 5
    else:
        opponent_base_atk = opponent.base_stats.get("spa", 100)
                        
        # Exact stat value is unknown (may have EV repartition) so use a simplified def estimation
        opponent_atk_stat_estimation = (opponent_base_atk * 2) + 5

    if move.category == MoveCategory.PHYSICAL:
        pokemon_def_stat = pokemon.stats.get("def", 100)
    else:
        pokemon_def_stat = pokemon.stats.get("spd", 100)

    base_damage = (((2 * opponent.level / 5 + 2) * move.base_power * (opponent_atk_stat_estimation / pokemon_def_stat)) / 50) + 2

    stab = 1.5 if (opponent.type_1 == move.type or opponent.type_2 == move.type) else 1.0
    type_multiplier = pokemon.damage_multiplier(move)

    return float(base_damage * stab * type_multiplier)


def calculate_damage(move: Move, pokemon: Pokemon, opponent: Pokemon) -> float:
    if move.base_power == 0:
        return 0.0

    if move.category == MoveCategory.PHYSICAL:
        attacker_stat = pokemon.stats.get("atk", 100)
    else:
        attacker_stat = pokemon.stats.get("spa", 100)

    opponent_def_stat_estimation = 1
    if move.category == MoveCategory.PHYSICAL:
        opponent_base_def = opponent.base_stats.get("def", 100)
        
        # Exact stat value is unknown (may have EV repartition) so use a simplified def estimation
        opponent_def_stat_estimation = (opponent_base_def * 2) + 5
    else:
        opponent_base_spd = opponent.base_stats.get("spd", 100)
        
        # Exact stat value is unknown (may have EV repartition) so use a simplified spe. def estimation
        opponent_def_stat_estimation = (opponent_base_spd * 2) + 5

    if opponent_def_stat_estimation == 0:
        opponent_def_stat_estimation = 1

    base_damage = (((2 * pokemon.level / 5 + 2) * move.base_power * (attacker_stat / opponent_def_stat_estimation)) / 50) + 2

    stab = 1.5 if (pokemon.type_1 == move.type or pokemon.type_2 == move.type) else 1.0
    type_multiplier = opponent.damage_multiplier(move)

    return float(base_damage * stab * type_multiplier)