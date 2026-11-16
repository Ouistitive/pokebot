
from poke_env import Player
from poke_env.battle import AbstractBattle
from poke_env.player import BattleOrder

from players.heuristic.knowledge.knowledge import Knowledge
from players.heuristic.knowledge.perceiver import Perceiver
from players.heuristic.think.deliberator import Deliberator


class HeuristicPlayer(Player):
    def __init__(self, *args, **kwargs):
        self.knowledge = Knowledge()
        
        self.perceiver = Perceiver(self.knowledge)
        self.deliberator = Deliberator(self.knowledge)
        
        super().__init__(*args, **kwargs)


    def choose_move(self, battle: AbstractBattle) -> BattleOrder:
        self.perceiver.update(battle)
        action = self.deliberator.deliberate(battle)
        
        return self.create_order(action)

