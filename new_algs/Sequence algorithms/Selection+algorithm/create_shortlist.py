from poke import *
from team import *
from battle import *
import copy
import pickle as pkl

data = pkl.load(open("data/dataset.pkl", "rb"))

def optimise_stats(species, cp=1500):
    p = Poke(data, species)
    if p.cp < 1400:
        return None
    elif p.cp < 1500:
        return p
    else:
        level = 40
        while p.cp > 1500:
            level -= 1
            p = Poke(data, species, level=level)
        level = level + 1
        atk = 15
        defn = 15
        sta = 15
        p = Poke(data, species, level = level)
        while p.cp > 1500:
            stats = p.stats.copy()
            if sta == 0:
                stats['sta'] = 0
            if defn == 0:
                stats['def'] = 0
            if atk == 0:
                stats['atk'] = 0
            if (stats['def'] > stats['atk'] 
                and stats['def'] > stats['sta']):
                defn -= 1
            elif (stats['sta'] > stats['atk'] 
                and stats['sta'] > stats['def']):
                sta -= 1
            else:
                atk -= 1
            p = Poke(data, species, level = level, ivs = [atk, defn, sta])
    return p

gl_stats = {
    p:optimise_stats(p) for p in data['pokes'].keys()
}

def test_moveset(p):
    movesets = []
    for k in gl_stats.keys():
        test_battle = Battle(
            Team([
                Poke(data, p.name, ivs = p.ivs, level = p.level)
            ]),
            Team([
                copy.copy(gl_stats[k])
            ])
        )
        movesets.append(test_battle.run_battle())
    return(movesets)

p = gl_stats['Zekrom']

timeit test_moveset(p)

i = 0
mvsts = []
for p in gl_stats.values():
    i = i + 1
    print(i)
    # 960ms per loop
    # 650ms after cythonising poke
    # 650ms after cythonising poke/battle/team
    # 285ms after removing call to pandas result
    mvsts.append(test_moveset(p))


mvsts = np.reshape(mvsts, len(gl_stats)**2)
mvsts = [pd.DataFrame(p) for p in mvsts]
mvsts = pd.concat(mvsts)

# pkl.dump(mvsts, open("data/moveset_tests.pkl", "wb"))
movesets = pkl.load(open("data/moveset_tests.pkl", "rb"))

# Filter for team 0 (pokemon was test case)
movesets = movesets[movesets['team'] == 0]
# Select movesets with the maximum damage dealt / (damage taken as % HP)
movesets = movesets.groupby(['poke','fast_move','charge_move']).sum().reset_index()
hp = pd.DataFrame.from_dict(
    {k:v.hp for k,v in gl_stats.items()},
    orient = 'index',
    columns = ['hp']).rename_axis('poke').reset_index()
movesets = pd.merge(movesets, hp)
movesets['ratio'] = movesets['dmg_dealt'] / (movesets['dmg_taken']/movesets['hp'])
max_ratio = movesets.groupby(['poke']).max().reset_index()
max_ratio = max_ratio[['poke','ratio']]
movesets = pd.merge(max_ratio, movesets)
movesets['ratio'] = movesets['ratio'] / np.mean(movesets['ratio'])

# deathrate is average damage taken as % hp
# e.g. dr of 1 means lose every battle
movesets['deathrate'] = (movesets['dmg_taken'] /
                        (movesets['hp'] * 441))

# interrogate
movesets.sort_values(by=['ratio'])
movesets.sort_values(by=['deathrate'])

# remove movesets without enough data points (Mew has random moves :( )
movesets = movesets[movesets['turns_active'] > 200]

# save list of initial values
pkl.dump(movesets, open("data/initial_values.pkl", "wb"))

