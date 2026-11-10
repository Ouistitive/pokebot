import pytest
from poke_env import SimpleHeuristicsPlayer

from config.showdown_server import close_showdown_server, run_showdown_server
from players.max_damage.max_damage import MaxDamagePlayer


@pytest.mark.asyncio
async def test_max_damage_player_vs_heuristics():
    process = run_showdown_server()
    print(f"Pokemon Showdown server is running (PID: {process.pid})")

    try:
        a = MaxDamagePlayer(battle_format="gen9randombattle", max_concurrent_battles=10)
        b = SimpleHeuristicsPlayer(battle_format="gen9randombattle", max_concurrent_battles=10)
        
        await a.battle_against(b, n_battles=100)
        print(f"Player `a` won {a.n_won_battles}/100")

        assert a.n_won_battles >= 0

    finally:
        # 4. Nettoyage garanti même si le test échoue
        await a.ps_client.stop_listening()
        await b.ps_client.stop_listening()
        close_showdown_server(process)