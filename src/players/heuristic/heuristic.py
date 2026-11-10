
from poke_env import Player
from poke_env.battle import AbstractBattle
from poke_env.player import BattleOrder

from players.heuristic.knowledge import Knowledge


class HeuristicPlayer(Player):
    
    def __init__(self, *args, **kwargs):
        self.knowledge = Knowledge()
        super().__init__(*args, **kwargs)
    
    def choose_move(self, battle: AbstractBattle) -> BattleOrder:
        self.knowledge.update(battle)
        
        
        pass
    