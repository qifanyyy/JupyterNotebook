import pytest
from poke import *
import pickle as pkl
import math

data = pkl.load(open("data/dataset.pkl", "rb"))


ivy = Poke(data, 'Ivysaur', moveset={
    'fast': 'Vine Whip',
    'charge': 'Sludge Bomb'
})
mew = Poke(data, 'Mew', moveset={
    'fast': 'Shadow Claw',
    'charge': 'Psyshock'
})

def test_name():
    assert ivy.name == 'Ivysaur'
    assert mew.name == 'Mew'

def test_cp():
    assert ivy.cp == 1699
    assert mew.cp == 3265

def test_type():
    assert mew.type == ['Psy']
    assert len(ivy.type) == 2

def test_hp():
    assert ivy.hp == 170
    assert mew.hp == 240

def test_get_damage():
    assert ivy.get_damage(ivy.moveset['fast'], mew) == 3

def test_attack():
    assert ivy.cooldown == 0
    assert ivy.active_attack is None

    ivy.attack(mew)
    assert ivy.cooldown == 1
    assert ivy.active_attack is not None
    assert mew.hp == 240
    
    ivy.attack(mew)
    assert ivy.cooldown == 0
    assert ivy.active_attack is None
    assert mew.hp == 237

def test_compare():
    assert ivy.compare(mew) == pytest.approx(0.39248, 0.0001)
    assert mew.compare(ivy) == 1/ivy.compare(mew)