
from poke_env import Player
from poke_env.battle import AbstractBattle, Move
from poke_env.player import BattleOrder

from players.max_damage.damage import calculate_damage

class MaxDamagePlayer(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def choose_move(self, battle: AbstractBattle) -> BattleOrder:
        if battle.force_switch:
            available_switches = battle.available_switches
            if available_switches:
                return self.create_order(available_switches[0])
            
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
