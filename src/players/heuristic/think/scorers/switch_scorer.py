MULTIPLIER_SCORES = {
    0.0: 30,   # Immunité (bonus maximum, optionnel mais recommandé)
    0.25: 20,  # Double résistance (très efficace pour switch)
    0.5: 10,   # Résistance simple
    1.0: 0,    # Neutre
    2.0: -10,  # Faiblesse simple
    4.0: -20   # Double faiblesse (très risqué)
}

def calculate_switch_score(pokemon_switch, opponent):
    mult_1 = opponent.damage_multiplier(pokemon_switch.type_1)
    
    if hasattr(pokemon_switch, 'type_2') and pokemon_switch.type_2 and pokemon_switch.type_2 != pokemon_switch.type_1:
        mult_2 = opponent.damage_multiplier(pokemon_switch.type_2)
        total_multiplier = mult_1 * mult_2
    else:
        total_multiplier = mult_1

    return MULTIPLIER_SCORES.get(total_multiplier, 0)