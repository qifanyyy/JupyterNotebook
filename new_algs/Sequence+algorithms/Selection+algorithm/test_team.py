from team import *
from poke import *

data = pkl.load(open("data/dataset.pkl", "rb"))

ivy = Poke(data, 'Ivysaur', moveset={
    'fast': 'Vine Whip',
    'charge': 'Sludge Bomb'
})
war = Poke(data, 'Wartortle', moveset={
    'fast': 'Water Gun',
    'charge': 'Aqua Jet'
})
cha = Poke(data, 'Charmeleon', moveset={
    'fast': 'Fire Fang',
    'charge': 'Fire Punch'
})

test_team = Team([ivy, war, cha])

def test_creation():
    assert len(test_team.pokes) == 3


def test_swich():
    assert test_team.active_poke.name == 'Ivysaur'
    test_team.switch(test_team.active_poke)
    assert test_team.active_poke.name == 'Charmeleon'
    test_team.switch(test_team.active_poke)
    assert test_team.active_poke.name == 'Wartortle'