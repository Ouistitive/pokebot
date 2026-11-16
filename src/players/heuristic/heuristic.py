
from poke_env import Player
from poke_env.battle import AbstractBattle
from poke_env.player import BattleOrder

from players.heuristic.knowledge.knowledge import Knowledge
from players.heuristic.knowledge.perceiver import Perceiver
from players.heuristic.think.deliberator import Deliberator


class HeuristicPlayer(Player):
    def __init__(self, *args, **kwargs):
        self.knowledge_by_battle: dict[str, Knowledge] = {}
        
        self.perceiver = Perceiver()
        self.deliberator = Deliberator()
        
        super().__init__(*args, **kwargs)


    def choose_move(self, battle: AbstractBattle) -> BattleOrder:
        knowledge = self.knowledge_by_battle.setdefault(battle.battle_tag, Knowledge())
        
        self.perceiver.update(battle, knowledge)
        action = self.deliberator.deliberate(battle, knowledge)
        
        return self.create_order(action)


    def _battle_finished_callback(self, battle: AbstractBattle):
        print(self.knowledge_by_battle[battle.battle_tag].pokemon_beliefs)
        
        self.knowledge_by_battle.pop(battle.battle_tag, None)
        return super()._battle_finished_callback(battle)