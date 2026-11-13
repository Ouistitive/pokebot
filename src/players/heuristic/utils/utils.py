
import math

from poke_env.battle import Pokemon

from players.heuristic.utils.pokemon_role import PokemonRole



def calculate_pokemon_role(pokemon: Pokemon) -> PokemonRole:
    """
        Calculate PokemonRole based its base statistics.
        Formula used:
            - Offensive: Max(ATK, SP.A) + SPE * 0.2
            - Defensive: sqrt( HP * ( (DEF + SP.D) / 2 ) )
    """
    stats = pokemon.base_stats
    offensive_score = max(stats["atk"], stats["spa"]) + (stats["spe"] * 0.2)
    defensive_score = math.sqrt(
        ( stats["hp"] * ((stats["def"] + stats["spd"]) / 2) )
    )
    
    ratio = offensive_score / defensive_score
    
    if ratio > 1.15:
        return PokemonRole.OFFENSIVE
    elif ratio < 0.85:
        return PokemonRole.DEFENSIVE
    return PokemonRole.BULKY