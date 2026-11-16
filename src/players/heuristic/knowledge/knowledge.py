

from players.heuristic.knowledge.opponent_tracker import OpponentTracker


class Knowledge:
    def __init__(self):
        self.opponent_trackers: dict[str, OpponentTracker] = {}
        self.previous_opponent_species: str | None = None
        