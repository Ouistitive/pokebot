
from poke_env.battle import Move, Pokemon


def calculate_damage(move: Move, pokemon: Pokemon, opponent: Pokemon) -> float:
    stab = 1.0
    if pokemon.type_1 == move.type or pokemon.type_2 == move.type:
        stab = 1.5

    multiplier = opponent.damage_multiplier(move)

    return move.base_power * stab * multiplier