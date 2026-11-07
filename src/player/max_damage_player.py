
from poke_env import Player, RandomPlayer
from poke_env.battle import AbstractBattle, Move
from poke_env.player import BattleOrder

from utils.damage_calculator import calculate_damage


class MaxDamagePlayer(RandomPlayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def choose_move(self, battle: AbstractBattle) -> BattleOrder:
        available_moves = battle.available_moves

        if not available_moves:
            return super().choose_move(battle)
        
        best_move: Move = available_moves[0]
        best_estimated_damage = -1
        for move in available_moves:
            estimated_damage = calculate_damage(move, battle.active_pokemon, battle.opponent_active_pokemon)
            
            if best_estimated_damage < estimated_damage:
                best_estimated_damage = estimated_damage
                best_move = move

        return self.create_order(best_move)
