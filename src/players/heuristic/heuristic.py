
from poke_env import Player
from poke_env.battle import AbstractBattle
from poke_env.player import BattleOrder

from players.heuristic.knowledge.knowledge import Knowledge
from players.heuristic.knowledge.perceiver import Perceiver
from players.heuristic.think.deliberator import Deliberator


class HeuristicPlayer(Player):
    def __init__(self, *args, **kwargs):
        self.knowledge = Perceiver()
        
        super().__init__(*args, **kwargs)


    def choose_move(self, battle: AbstractBattle) -> BattleOrder:
        self.knowledge.update(battle)
        
        

        if battle.trapped or not battle.available_moves:
            if battle.available_switches:
                return self.create_order(battle.available_switches[0])
            
        if battle.available_moves:
            return self.create_order(battle.available_moves[0])
            
        return self.choose_default_move(battle)
    