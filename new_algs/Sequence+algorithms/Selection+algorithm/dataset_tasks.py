import taskflow as tsk
from taskflow import task_definition
from taskflow.backend import openLocalSession
from taskflow.distributed import openRemoteSession
from taskflow import utils

import requests
import math
from tqdm import tqdm
import os
import bz2

from zipfile import ZipFile
from glob import glob
import xml.etree.ElementTree as ET

import hashlib
from pymongo import UpdateOne
from bson.objectid import ObjectId

import subprocess as sp
from gridfs import GridFS
import shutil

import networkx as nx
import json
import time


types_str = {
    'memory': ['valid-deref',
               'valid-free',
               'valid-memtrack',
               'valid-memcleanup',
               'valid-memsafety'],
    'reachability': ['unreach-call'],
    'overflow': ['no-overflow'],
    'termination': ['termination']
}

SV_BENCHMARKS_GIT = "https://github.com/sosy-lab/sv-benchmarks.git"


def _download_file(url, path):
    r = requests.get(url, stream=True)

    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024
    wrote = 0

    print("Download url: %s >> %s" % (url, path))
    with open(path, 'wb') as f:
        for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size/block_size), unit='KB'):
            wrote = wrote + len(data)
            f.write(data)
    if total_size != 0 and wrote != total_size and os.path.getsize(path) != total_size:
        os.remove(file)
        raise ValueError("ERROR, something went wrong")


def create_folder(path):
    if len(os.path.splitext(path)[1]) > 0:
        path = os.path.dirname(path)

    if not os.path.isdir(path):
        os.makedirs(path)


def read_svcomp_data(path):
    D = {}

    directory = os.path.dirname(path)
    tmp_dir = os.path.join(directory, "tmp")

    try:
        with ZipFile(path, 'r') as zipObj:
            zipObj.extractall(path=tmp_dir)

        for entry in tqdm(glob(os.path.join(tmp_dir, "*.bz2"))):
            read_svcomp_bz2(entry, D)

    finally:
        if os.path.exists(tmp_dir):
            os.system('rm -rf %s' % tmp_dir)

    return D


def detect_type(text):
    global types_str

    for k, V in types_str.items():
        for v in V:
            if v in text:
                return k

    raise ValueError("Unknown type for properties \"%s\"" % text)


def short_name(name):
    name = name.replace("../sv-benchmarks/c/", "")
    name = name.replace("/", "_")
    name = name.replace(".", "_")
    return name


def ground_truth(file, type):
    global types_str

    for type_str in types_str[type]:
        if 'true-%s' % type_str in file:
            return True
        if 'false-%s' % type_str in file:
            return False

    raise ValueError("Cannot detect type %s in file \"%s\"." % (type, file))


def read_svcomp_bz2(path, result):
    with bz2.open(path) as o:
        xml = o.read()

    root = ET.fromstring(xml)

    if 'java' in root.attrib['name'].lower():
        return

    tool_name = root.attrib['benchmarkname']

    for run in root.iter('run'):
        attr = run.attrib
        file = attr['name']
        name = short_name(file)
        category = detect_type(attr['properties'])

        for column in run:
            title = column.attrib['title']

            if title == 'status':
                status = column.attrib['value']

            if title == 'cputime':
                cputime = float(column.attrib['value'][:-1])

        if category not in result:
            result[category] = {}
        if tool_name not in result[category]:
            result[category][tool_name] = {}
        result[category][tool_name][name] = {
            'file': file,
            'status': status,
            'ground_truth': ground_truth(file, category),
            'cputime': cputime
        }


def sp_run_success(cmd):
    # utils.run_command(cmd)
    c = ' '.join(cmd)
    os.system(c)


def prepare_svcomp_git(competition_year, directory):

    base_path = os.path.join(directory, "svcomp-git")
    git_path = os.path.join(base_path, "sv-benchmarks")

    create_folder(base_path)

    if not os.path.exists(git_path):
        global SV_BENCHMARKS_GIT
        sp_run_success(["git", "-C", base_path, "clone", SV_BENCHMARKS_GIT])

    if not os.path.exists(git_path):
        raise tsk.EnvironmentException(
                    "Something went wrong during git clone.")

    sp_run_success(["git", "-C", git_path, "checkout", "tags/svcomp%s" % competition_year[2:]])

    return git_path


def run_pesco(pesco_path, in_file, out_file, pos_path=None, heap="10g", timeout=900):
    path_to_source = in_file

    run_path = os.path.join(pesco_path, "scripts", "cpa.sh")
    output_path = out_file

    if not os.path.isdir(pesco_path):
        raise ValueError("Unknown pesco path %s" % pesco_path)

    if not (os.path.isfile(path_to_source) and (path_to_source.endswith('.i') or path_to_source.endswith('.c'))):
        raise ValueError('path_to_source is no valid filepath. [%s]' % path_to_source)

    cmd = [run_path,
           "-graphgen",
           "-heap", heap,
           "-Xss512k",
           "-setprop", "neuralGraphGen.output="+output_path]

    if pos_path is not None:
        cmd.extend(["-setprop", "neuralGraphGen.nodePosition="+pos_path])

    cmd.append(path_to_source)

    proc = utils.run_command(
                    cmd,
                    timeout=timeout
                    )


# Tasks

@task_definition()
def load_svcomp(competition_year, env=None):
    url = "https://sv-comp.sosy-lab.org/%s/results/results-verified/All-Raw.zip" % competition_year

    path = "./svcomp/svcomp_%s.zip" % competition_year

    if not env or not env.is_remote_io_loaded():
        raise tsk.EnvironmentException("Need a remote context to process competition data")

    coll = env.get_db().svcomp

    if coll.find_one({'svcomp': competition_year}) is not None:
        return list(set([
            r['name'] for r in coll.find({'svcomp': competition_year}, ['name'])
        ]))

    tmp = env.get_cache_dir()
    if tmp is not None:
        path = os.path.join(tmp, path)

    create_folder(path)

    if not os.path.exists(path):
        _download_file(url, path)

    if not os.path.exists(path):
        raise ValueError("Something went wrong for competition: %s" % competition_year)

    comp = read_svcomp_data(path)

    updates = []
    names = set([])
    for category, V in comp.items():

        for tool, D in V.items():

            for name, entry in D.items():

                update = {
                    'name': name,
                    'svcomp': competition_year,
                    'category': category,
                    'tool': tool
                }
                update.update(entry)

                identifier = '::'.join(sorted(['%s_%s' % (k, v) for k, v in update.items()]))
                identifier = hashlib.blake2b(identifier.encode('utf-8'), digest_size=12).digest()
                identifier = ObjectId(identifier)
                update['_id'] = identifier
                names.add(update['name'])

                updates.append(UpdateOne({
                    '_id': identifier
                }, {'$set': update}, upsert=True))

    coll.bulk_write(updates)

    return list(names)


@task_definition(workload="heavy")
def code_to_graph(name, competition, git_init=True, env=None):
    if 'PESCO_PATH' not in os.environ:
        raise tsk.EnvironmentException(
                    "Environment variable PESCO_PATH has to be defined!")

    if not env or not env.is_remote_io_loaded():
        raise tsk.EnvironmentException(
                    "Need a remote context to process competition data")

    svcomp_db = env.get_db().svcomp

    info = svcomp_db.find_one({'name': name, 'svcomp': competition})

    if info is None:
        raise ValueError("Unknown task id %s [SVCOMP %s]" % (str(name), competition))

    if 'graph_ref' in info:
        return info['graph_ref']

    fs = GridFS(env.get_db())
    ret = fs.find_one({'name': info['name'], 'app_type': 'code_graph',
                       'competition': competition})

    if ret is not None:
        svcomp_db.update_many({'name': info['name'], 'svcomp': info['svcomp']},
                              {'$set': {'graph_ref': ret._id}})
        return ret._id

    svcomp_db.update_many({'name': info['name'], 'svcomp': info['svcomp']},
                          {'$set': {'graph_ref': 0}})

    try:

        if git_init:
            git_path = prepare_svcomp_git(info['svcomp'], env.get_host_cache_dir())
        else:
            git_path = os.path.join(env.get_host_cache_dir(),
                                    "svcomp-git",
                                    "sv-benchmarks")
        file_path = info['file'].replace("../sv-benchmarks/", "")
        file_path = os.path.join(git_path, file_path)

        if not os.path.isfile(file_path):
            raise ValueError("Some problem occur while accessing file %s." % file_path)

        pesco_path = os.environ['PESCO_PATH']
        out_path = info['name'] + ".json"
        out_path = os.path.join(env.get_cache_dir(), out_path)

        start_time = time.time()

        run_pesco(
            pesco_path,
            file_path,
            out_path
        )

        run_time = time.time() - start_time

        if not os.path.exists(out_path):
            raise tsk.EnvironmentException(
                "Pesco doesn't seem to be correctly configured! No output for %s" % info['name']
            )

        file = fs.new_file(name=info['name'],
                           competition=info['svcomp'],
                           app_type='code_graph',
                           encoding="utf-8")

        try:
            with open(out_path, "r") as i:
                shutil.copyfileobj(i, file)
        finally:
            file.close()

        svcomp_db.update_many({'name': info['name'], 'svcomp': info['svcomp']},
                              {'$set': {'graph_ref': file._id,
                                        'run_time': run_time}})

    except Exception as e:
        svcomp_db.update_many({'name': info['name'], 'svcomp': info['svcomp']},
                              {'$unset': {'graph_ref': 0}})
        raise e

    return file._id


def is_forward_and_parse(e):
    if e.endswith('|>'):
        return e[:-2], True
    return e[2:], False


def estimate_depth(G, n):

    seen = set([])
    queue = [(n, 1)]

    while len(queue) > 0:
        v, depth = queue.pop()

        if v in seen:
            continue
        seen.add(v)

        G.nodes[v]['depth'] = depth

        for u, _ in G.in_edges(v):
            if u not in seen:
                queue.append((u, depth + 1))


def parse_dfs_nx_alt(R):
    if R is None:
        return nx.MultiDiGraph()
    graph = nx.MultiDiGraph()

    for k, v in R['nodes'].items():
        graph.add_node(k, label=v)

    for u, l, v in R['edges']:
        e_label, forward = is_forward_and_parse(l)
        if forward:
            graph.add_edge(u, v, key=e_label)
        else:
            graph.add_edge(v, u, key=e_label)

    for n in graph.nodes():
        if graph.out_degree(n) == 0:
            s = n.split("_")
            if len(s) == 2:
                graph.add_edge(n, s[0], key="s")
                graph.nodes[s[0]]['depth'] = 0
                estimate_depth(graph, n)

    return graph


def load_graph(task_id, env):
    if not env or not env.is_remote_io_loaded():
        raise tsk.EnvironmentException(
                    "Need a remote context to process competition data")

    svcomp_db = env.get_db().svcomp

    info = svcomp_db.find_one({'_id': task_id})

    if info is None:
        raise ValueError("Unknown task id %s" % str(task_id))

    if 'graph_ref' not in info:
        raise ValueError("Graph %s is not computed" % str(info['name']))

    fs = GridFS(env.get_db())
    text = fs.get(info['graph_ref']).read().decode('utf-8')

    G = parse_dfs_nx_alt(json.loads(text))
    G.graph['name'] = info['name']
    G.graph['reference'] = info['graph_ref']
    return G


if __name__ == '__main__':

    comp = "2018"

    load = load_svcomp(comp)
    load_it = tsk.fork(load)
    graph_it = code_to_graph(load_it, comp, git_init=False)

    with openRemoteSession(
        session_id="317e3bb0-caf4-4f57-9975-0e782371a866"
    ) as sess:
        sess.run(graph_it)
