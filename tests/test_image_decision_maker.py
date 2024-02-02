from src.image_decision_maker import is_ingame


def test_is_ingame():
    assert is_ingame("ingame_opponent_3_pokemon_left.png")
    assert is_ingame("ingame_opponent_2_pokemon_left.png")
    assert is_ingame("ingame_opponent_1_pokemon_left.png")
    assert is_ingame("enemy_charge_attack.png")
    assert not is_ingame("random_image.png")
