
import asyncio

from poke_env import SimpleHeuristicsPlayer

from config.showdown_server import close_showdown_server, run_showdown_server
from players.heuristic.heuristic import HeuristicPlayer


async def main():
    process = run_showdown_server()
    print(f"Pokemon Showdown server is running (PID: {process.pid})")

    a = HeuristicPlayer(battle_format="gen9randombattle", max_concurrent_battles=10)
    b = SimpleHeuristicsPlayer(battle_format="gen9randombattle", max_concurrent_battles=10)
    await a.battle_against(b, n_battles=1)
    print(f"Player `a` won {a.n_won_battles}/1")

    print(a.knowledge.pokemon_beliefs)

    await a.ps_client.stop_listening()
    await b.ps_client.stop_listening()

    close_showdown_server(process)

if __name__ == "__main__":
    asyncio.run(main())