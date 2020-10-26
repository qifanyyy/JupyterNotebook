from poke import *
from battle import *
import numpy as np
import pytest

data = pkl.load(open("data/dataset.pkl", "rb"))

test_team_1 = Team([
    Poke(data, 'Ivysaur'),
    Poke(data, 'Rhydon'),
    Poke(data, 'Blastoise')])
test_team_2 = Team([
    Poke(data, 'Skarmory'),
    Poke(data, 'Charmeleon'),
    Poke(data, 'Kadabra')])

test_battle = Battle(test_team_1, test_team_2)

def foo():
    test_team_1 = Team([
        Poke(data, 'Ivysaur'),
        Poke(data, 'Rhydon'),
        Poke(data, 'Blastoise')])
    test_team_2 = Team([
        Poke(data, 'Skarmory'),
        Poke(data, 'Charmeleon'),
        Poke(data, 'Kadabra')])

    test_battle = Battle(test_team_1, test_team_2)
    test_battle.run_battle()

def test_turn():
    assert np.all([p.active_poke.active_attack is None
            for p in test_battle.teams])

    test_battle.turn()

    assert np.all([p.active_poke.active_attack is not None
            for p in test_battle.teams])


def test_generate_report():
    report = test_battle.generate_report()
    assert report.shape == (6, 7)


def test_run_battle():
    test_battle.run_battle(False)

    assert test_battle.victor is not None
    assert test_battle.victor.pokes[0].name == 'Ivysaur'