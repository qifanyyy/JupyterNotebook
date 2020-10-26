from flask import Flask, abort, request
from flask_restful import Resource, Api
import os
import uuid
import parsing as p
import db_utils
import traceback
import threading
import json

from tasks.data import dataset_tasks as dt
from tasks.utils import train_utils as tu
import torch as th
from torch_geometric.data import Batch
from tasks.torch.models import ConditionalGlobalAttention


app = Flask(__name__, static_url_path="/static/")
api = Api(app)

allowed_dirs = set(['js', 'css', 'semantic'])

threads = {}


def att_callback():

    att = []

    def cb(model, kwargs):
        if isinstance(model, ConditionalGlobalAttention):
            kwargs['return_attention'] = True
            _, a = model(**kwargs)
            del kwargs['return_attention']
            att.append(a)
        return kwargs

    return att, cb


def transform_c(id, model_id, category, base_path, file_path):

    model, info = db_utils.load_model(model_id)

    ast_graph = info['experiment'].endswith('_graph')

    graph_path = os.path.join(base_path, "graph.json")
    try:
        graph_path, pos_path, _ = p.parse_c_code(file_path, graph_path)
        with open(graph_path, "r") as i:
            D = json.load(i)
        with open(pos_path, "r") as i:
            pos = json.load(i)
        G = dt.parse_dfs_nx_alt(D)
        data, index = p.create_data_bag(G, db_utils.get_ast_index(),
                                        category, pos=pos,
                                        ast_graph=ast_graph)
        data = Batch.from_data_list([data])
        att, cb = att_callback()
        model.register_callback(cb)
        pred = th.sigmoid(model(data))

        tools = info['tools']
        ranking = tu.get_ranking(pred[0], tools)

        with open(os.path.join(base_path, "prediction.json"), "w") as o:
            json.dump(ranking, o)

        pos = data.position
        attention = []

        index = {v: k for k, v in index.items()}

        for a in att:
            if a is None:
                attention.append(None)
                continue
            o = []
            for i in range(a.shape[0]):
                node_att = a[i][0].item()
                o.append(
                    [pos[0, i].item(), pos[1, i].item(), node_att,
                     index[i]]
                )
            attention.append(o)

        with open(os.path.join(base_path, "attention.json"), "w") as o:
            json.dump(attention, o)

    except Exception:
        exc = traceback.format_exc()
        with open(os.path.join(base_path, "exception"), "w") as o:
            o.write(exc)


def request_predict(form):
    id = str(uuid.uuid4())

    model_id = form['model_id']
    category = form['category']

    path = os.path.join(".", "process", id)
    os.makedirs(path)
    file_path = os.path.join(path, "file.c")

    with open(file_path, "w") as o:
        o.write(form['data'])

    thread = threading.Thread(
        target=transform_c,
        args=(id, model_id, category, path, file_path)
    )
    thread.start()

    threads[id] = thread
    return id


@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route("/<string:type>/<path:path>")
def send_static(type, path):
    if type not in allowed_dirs:
        return abort(404)
    path = os.path.join(type, path)
    path = os.path.normpath(path)

    if not path.startswith(type):
        return abort(404)

    return app.send_static_file(path)


class PredictionTask(Resource):

    def get(self, predict_id):
        path = os.path.join(".", "process", predict_id)
        if not os.path.exists(path):
            return abort(404)

        exc = os.path.join(path, 'exception')
        if os.path.exists(exc):
            with open(exc, "r") as i:
                return {'exception': i.read(), 'finish': True}

        path = os.path.join(".", "process", predict_id)
        state = {
            'graph': os.path.isfile(os.path.join(path, 'graph.json')),
            'position': os.path.isfile(os.path.join(path, 'graph.json.pos')),
            'pred': os.path.isfile(os.path.join(path, 'prediction.json')),
            'attention': os.path.isfile(os.path.join(path, 'attention.json'))
        }

        finished = True
        for v in state.values():
            finished = finished and v
        state['finish'] = finished

        if not finished and predict_id not in threads:
            return {'exception': "Seem to be an old request!",
                    'finished': True}

        return state

    def put(self):
        return {'request_id': request_predict(
            request.form
        )}


class GraphResource(Resource):

    def get(self, id):
        path = os.path.join(".", "process", id, "graph.json")

        if not os.path.isfile(path):
            return abort(404)

        with open(path, "r") as i:
            return json.load(i)


class InfoResource(Resource):

    def get(self):
        return db_utils.get_experiment_info()


class PredictionResource(Resource):
    def get(self, id):
        path = os.path.join(".", "process", id, "prediction.json")

        if not os.path.isfile(path):
            return abort(404)

        with open(path, "r") as i:
            return json.load(i)


class AttentionResource(Resource):
    def get(self, id):
        path = os.path.join(".", "process", id, "attention.json")

        if not os.path.isfile(path):
            return abort(404)

        with open(path, "r") as i:
            return json.load(i)


class PositionResource(Resource):
    def get(self, id):
        path = os.path.join(".", "process", id, "graph.json.pos")

        if not os.path.isfile(path):
            return abort(404)

        with open(path, "r") as i:
            return json.load(i)


api.add_resource(PredictionTask, '/api/task/',
                 '/api/task/<string:predict_id>/')
api.add_resource(GraphResource, "/api/graph/<string:id>/")
api.add_resource(InfoResource, "/api/models/")
api.add_resource(PredictionResource, "/api/prediction/<string:id>/")
api.add_resource(AttentionResource, "/api/attention/<string:id>/")
api.add_resource(PositionResource, "/api/position/<string:id>/")

if __name__ == '__main__':
    app.run(debug=True)
