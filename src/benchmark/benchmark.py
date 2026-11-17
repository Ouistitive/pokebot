

import asyncio
import csv
from datetime import datetime
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from poke_env import MaxBasePowerPlayer, Player, RandomPlayer, SimpleHeuristicsPlayer

from config.showdown_server import close_showdown_server, run_showdown_server
from players.heuristic.heuristic import HeuristicPlayer



async def benchmark_agent(player: Player, N_BATTLE: int, BATTLE_FORMAT: int, MAX_CONCURRENT_BATTLE: int):
    opponent_players: list[Player] = [
        RandomPlayer(battle_format=BATTLE_FORMAT, max_concurrent_battles=MAX_CONCURRENT_BATTLE),
        MaxBasePowerPlayer(battle_format=BATTLE_FORMAT, max_concurrent_battles=MAX_CONCURRENT_BATTLE),
        SimpleHeuristicsPlayer(battle_format=BATTLE_FORMAT, max_concurrent_battles=MAX_CONCURRENT_BATTLE)
    ]
    
    csv_file = "results/benchmark.csv"
    file_exists = Path(csv_file).exists()
    
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow([
                "timestamp", "agent_name", "opponent_name", "battle_format", 
                "n_battles", "n_won", "win_rate_percent", "total_time_sec", 
                "time_per_battle_sec", "max_concurrent_battles"
            ])
        else:
            writer.writerow([])
            
        for opponent in opponent_players:
            won_snapshot = player.n_won_battles
            start_time = time.time()
            
            await player.battle_against(opponent, n_battles=N_BATTLE)
            
            elapsed_time = time.time() - start_time
            n_won = player.n_won_battles - won_snapshot
            win_rate = (n_won / N_BATTLE) * 100
            time_per_battle = elapsed_time / N_BATTLE
            
            agent_name = player.__class__.__name__
            opponent_name = opponent.__class__.__name__
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"[{agent_name} vs {opponent_name}] Gagné: {n_won}/{N_BATTLE} ({win_rate}%) en {elapsed_time:.2f}s")
            
            writer.writerow([
                timestamp, agent_name, opponent_name, BATTLE_FORMAT,
                N_BATTLE, n_won, round(win_rate, 2), round(elapsed_time, 2),
                round(time_per_battle, 4), MAX_CONCURRENT_BATTLE
            ])
            
            await opponent.ps_client.stop_listening()


async def main():
    N_BATTLE = 200
    BATTLE_FORMAT = "gen9randombattle"
    MAX_CONCURRENT_BATTLE = 15
    
    process = run_showdown_server()
        
    await benchmark_agent(
        HeuristicPlayer(battle_format=BATTLE_FORMAT, max_concurrent_battles=MAX_CONCURRENT_BATTLE),
        N_BATTLE, 
        BATTLE_FORMAT, 
        MAX_CONCURRENT_BATTLE
    )
    
    close_showdown_server(process)


if __name__ == "__main__":
    asyncio.run(main())