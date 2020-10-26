from taskflow import backend
from tasks import preparation as p
import argparse
from bson.objectid import ObjectId


parser = argparse.ArgumentParser()
parser.add_argument("tid")

args = parser.parse_args()

id = args.tid
id = ObjectId(id)

with backend.openLocalSession() as sess:
    sess.run(p.ast_features_bag(id, 5000))
