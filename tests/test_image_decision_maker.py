import pytest

from src import constants
from src.game_action import GameActions
from src.image_decision_maker import is_ingame, make_decision
from src.image_template_loader import load_image_templates


@pytest.fixture(scope="module")
def template_images():
    return load_image_templates()


def test_is_ingame():
    assert is_ingame("ingame_opponent_3_pokemon_left.png")
    assert is_ingame("ingame_opponent_2_pokemon_left.png")
    assert is_ingame("ingame_opponent_1_pokemon_left.png")
    assert is_ingame("enemy_charge_attack.png")
    assert not is_ingame("random_image.png")


def test_make_decision_throws_exception_if_image_does_not_exist(template_images):
    with pytest.raises(FileNotFoundError):
        make_decision(template_images, "not_existing_image.png")


def test_make_decision_presses_close_button_on_available_pokemon_at_rank(
    template_images,
):
    result = make_decision(
        template_images, "./tests/images/available_pokemon_at_rank.png"
    )

    assert result.action is not None
    assert result.action == GameActions.tap_position
    assert result.position == (542, 2006)  # TODO
    assert not result.is_ingame


def test_make_decision_presses_battle_button_on_main_gbl_screen(template_images):
    result = make_decision(template_images, "./tests/images/battle_button_1.png")

    assert result.action is not None
    assert result.action == GameActions.tap_position
    assert result.position == (542, 2006)
    assert not result.is_ingame


def test_make_decision_presses_battle_button_on_main_gbl_screen_2(template_images):
    result = make_decision(template_images, "./tests/images/battle_button_2.png")

    assert result.action is not None
    assert result.action == GameActions.tap_position
    assert result.position == (435, 2145)
    assert not result.is_ingame


def test_make_decision_presses_ultra_league_button(template_images):
    result = make_decision(template_images, "./tests/images/choose_ultra_league.png")

    assert result.action is not None
    assert result.action == GameActions.tap_position
    assert result.position == (215, 1148)
    assert not result.is_ingame


def test_make_decision_presses_claim_rank_rewards(template_images):
    result = make_decision(template_images, "./tests/images/claim_rank_rewards.png")

    assert result.action is not None
    assert result.action == GameActions.tap_position
    assert result.position == (523, 1996)
    assert not result.is_ingame


def test_make_decision_collects_rewards1(template_images):
    result = make_decision(template_images, "./tests/images/collect_rewards_1.png")

    assert result.action is not None
    assert result.action == GameActions.tap_position
    assert result.position == (285, 1780)
    assert not result.is_ingame


def test_make_decision_collects_rewards2(template_images):
    result = make_decision(template_images, "./tests/images/collect_rewards_2.png")

    assert result.action is not None
    assert result.action == GameActions.tap_position
    assert result.position == (127, 1805)
    assert not result.is_ingame


def test_make_decision_collects_rewards3(template_images):
    result = make_decision(template_images, "./tests/images/collect_rewards_3.png")

    assert result.action is not None
    assert result.action == GameActions.tap_position
    assert result.position == (590, 1758)
    assert not result.is_ingame


def test_make_decision_presses_confirm_battle_party_button(template_images):
    result = make_decision(template_images, "./tests/images/confirm_battle_party.png")

    assert result.action is not None
    assert result.action == GameActions.tap_position
    assert result.position == (542, 2101)
    assert not result.is_ingame


def test_make_decision_presses_shield_to_defend_from_charge_attack(template_images):
    result = make_decision(template_images, "./tests/images/enemy_charge_attack.png")

    assert result.action is not None
    assert result.action == GameActions.tap_position
    assert result.position == (546, 1963)
    assert result.is_ingame


def test_make_decision_attacks_on_fixed_position_if_opponent_3_pokemon_left(
    template_images,
):
    result = make_decision(
        template_images, "./tests/images/ingame_opponent_3_pokemon_left.png"
    )

    assert result.action is not None
    assert result.action == GameActions.tap_position
    assert result.position == constants.ATTACK_TAP_POSITION
    assert result.is_ingame


def test_make_decision_presses_ok_button_on_last_game_of_set_if_win(template_images):
    result = make_decision(template_images, "./tests/images/last_game_of_set_win.png")

    assert result.action is not None
    assert result.action == GameActions.tap_position
    assert result.position == (539, 2193)
    assert not result.is_ingame


def test_make_decision_exits_bot_if_max_number_of_games_played_text(template_images):
    result = make_decision(
        template_images, "./tests/images/max_number_of_games_played.png"
    )

    assert result.action is not None
    assert result.action == GameActions.exit_program
    assert not result.is_ingame


def test_make_decision_returns_game_action_with_no_action_if_no_image_matches(
    template_images,
):
    result = make_decision(template_images, "./tests/images/no_action_to_take.png")

    assert result.action is not None
    assert result.action == GameActions.no_action
    assert not result.is_ingame
