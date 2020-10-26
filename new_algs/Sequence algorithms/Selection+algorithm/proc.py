import pandas as pd
import pickle as pkl

fp = "raw/database.xlsx"

types = pd.read_excel(fp, "Types")
types['t1'] = types['t1'].map(lambda x: x[:3])
types['t2'] = types['t2'].map(lambda x: x[:3])
types = {n: grp.loc[n].to_dict()['eff']
         for n, grp in types.set_index(
             ['t1', 't2']).groupby(level='t1')}
pkl.dump(types, open("../data/types.pkl", "wb"))

cp = pd.read_excel(fp, "CP Mult").to_dict("records")
cp = {r['Level']:r['CP multiplier'] for r in cp}
pkl.dump(cp, open("../data/cpmults.pkl", "wb"))

base_stats = pd.read_excel(fp, "Base Stats")
base_stats = base_stats.set_index("Name").to_dict("index")

fast_moves = pd.read_excel("raw/moves.xlsx",
    "fast").set_index("MOVE")
fast_moves['CAT'] = 'fast'
charge_moves = pd.read_excel("raw/moves.xlsx", 
    "charge").set_index("MOVE")
charge_moves['CAT'] = 'charge'
fields =  ['CAT', 'TYPE', 'PWR', 'ENG', 'TURNS']
moves = pd.concat([fast_moves[fields],
    charge_moves[fields]])
moves['TYPE'] = moves['TYPE'].map(lambda x: x[:3])
moves = moves.to_dict('index')
pkl.dump(moves, open("../data/moves.pkl", "wb"))

learned_moves = pd.read_excel(fp, "learned moves")
learned_moves = {k:learned_moves.move[learned_moves.name == k].tolist()
    for k in learned_moves.name.unique()}
pkl.dump(learned_moves, open("../data/learnedmoves.pkl", "wb"))

db = pd.read_excel(fp, "Database")
db = db.drop(columns=['CP', 'Product (k)', 'P/CP'])
db = db.set_index("Name").to_dict("index")
pkl.dump(db, open("../data/pogostats.pkl", "wb"))

pokes = pkl.load(open("../data/processed_pokes.pkl", "rb"))
# Filter out all pokes without movesets (~10% - these are mostly unreleased)
pokes = {k:v for k,v in pokes.items() if v['field_primary_moves'] != ''}

dataset = {
    'pokes': pokes,
    'moves': moves,
    'cp': cp,
    'types': types
}
pkl.dump(dataset, open("../data/dataset.pkl", "wb"))