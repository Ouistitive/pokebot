
from poke_env.battle import Move, Pokemon, PokemonType, Status

from players.heuristic.knowledge.pokemon_beliefs import PokemonBeliefs
from players.heuristic.utils.pokemon_role import PokemonRole


def calculate_heal_move_score(move: Move, active: Pokemon, opponent: Pokemon) -> float:
    if move.heal == 0:
        return 0.0
    
    score = 50.0
    
    if active.current_hp_fraction <= 0.5:
        score += 70.0 * (1.0 - active.current_hp_fraction)
    else:
        score -= 30.0
    
    if opponent.base_stats["spe"] < active.base_stats["spe"]:
        score += 20.0

    return score


def calculate_boost_move_score(move: Move, active: Pokemon, opponent_beliefs: PokemonBeliefs, opponent_team: list[Pokemon]) -> float:
    boosts = move.boosts
    if boosts is None:
        return 0.0
    
    score = 40.0
    
    if opponent_beliefs.role == PokemonRole.DEFENSIVE:
        score += 40.0
    
    if active.current_hp_fraction < 0.4:
        score -= 50.0
    
    # If the boost is offensive (e.g. dragon dance, calm mind, sword dance...)
    if "atk" in boosts or "spa" in boosts:
        # Avoid setup when it's still too early (i.e. opponent HP are high)
        for opponent in opponent_team:
            if opponent.current_hp_fraction <= 0.4:
                score += 10.0
            elif opponent.current_hp_fraction >= 0.7:
                score -= 10.0
        
        setup_atk = boosts.get("atk", 0)
        setup_spa = boosts.get("spa", 0)
        
        score -= (setup_atk * 10 + setup_spa * 10)
    
    if "def" in boosts or "spd" in boosts:
        score += 10.0
    
    return score


def calculate_status_move_score(move: Move, active: Pokemon, opponent: Pokemon) -> float:
    if not move.status:
        return 0.0
    
    score = 40.0
    
    if opponent.current_hp_fraction <= 0.3:
        score -= 20.0
    elif opponent.current_hp_fraction >= 0.75:
        score += 50.0
    
    if _can_opponent_get_status(move.status, opponent):
        score += 30.0
    else:
        score -= 100.0
    
    
    if opponent.status is not None:
        score -= 100.0
    else:
        score += 20.0
    
    return score


def _can_opponent_get_status(status: Status, opponent: Pokemon) -> bool:
    opponent_types = {opponent.type_1, opponent.type_2}
    
    if status == Status.BRN and PokemonType.FIRE in opponent_types:
        return False
        
    if status == Status.PAR and PokemonType.ELECTRIC in opponent_types:
        return False
        
    if status in (Status.PSN, Status.TOX):
        if PokemonType.POISON in opponent_types or PokemonType.STEEL in opponent_types:
            return False
            
    if status == Status.FRZ and PokemonType.ICE in opponent_types:
        return False

    return True