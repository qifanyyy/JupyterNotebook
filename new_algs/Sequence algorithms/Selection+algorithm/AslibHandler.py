import os
import sys
import arff
import collections
import pickle
import numpy as np

import TextToImage


class AslibHander(object):
    """
    The class for getting solver and CV information
    The main output is a dict
    [
       [#folds, scen: { inst: [local_path, folds,
                {local_path: str,
               fold: int,
               solvers: [],
               status: [],
               runtime: []} ]} ] ...
    ]
    """

    def __init__(self, config):
        self.config = config
        self.inst_dic = {}  # {scen: { inst: [path, folds, info{} ]}}
        # {scen: [[ {inst: [path, folds, info{} ]} }, #fold...]}
        self.finst_dic = {}
        if sys.platform == 'linux':
            self.file_prefix = self.config['lin_prefix']
        else:
            self.file_prefix = self.config['win_prefix']

    def load_scenarios(self, scen):
        # read algo and cv files
        # return a list of instance and its local path
        # return a list of instance folds
        # return a dic of instance and its solution's info
        scen_path = os.path.join(
            self.file_prefix, self.config['instance_path'], "data.pk")
        if os.path.isfile(scen_path):
            dd = pickle.load(open(scen_path, 'rb'))
            # self.finst_dic[scen] = dd[scen]
            self.finst_dic[scen] = dd
            if not self.finst_dic[scen] is None:
                return

        self.inst_dic[scen] = {}
        al_path = os.path.join(
            self.file_prefix, self.config['aslib_path'], scen, "algorithm_runs.arff")
        cv_path = os.path.join(
            self.file_prefix, self.config['aslib_path'], scen, "cv.arff")
        with open(al_path, 'r') as f:
            algo = arff.load(f)

        SolverItem = collections.namedtuple(
            'SolverItem', 'solvers status_index run_time repitition image_array')

        def sign(sta):
            if sta == 'ok':
                return 1
            else:
                return 0

        for row in algo['data']:
            # row ['inst', 'repitition', 'solver', 'runtime', 'status']
            local_path = os.path.join(
                self.file_prefix, self.config['instance_path'], row[0])
            if not os.path.isfile(local_path):
                raise FileNotFoundError(
                    "File #{} does not exist".format(local_path))
            if not row[0] in self.inst_dic[scen]:
                self.inst_dic[scen][row[0]] = [
                    '', 0, SolverItem([], [], [], [], [])]
            self.inst_dic[scen][row[0]][0] = local_path
            self.inst_dic[scen][row[0]][2].solvers.append(row[2])
            self.inst_dic[scen][row[0]][2].status_index.append(
                int(sign(row[4])))
            self.inst_dic[scen][row[0]][2].run_time.append(float(row[3]))
            self.inst_dic[scen][row[0]][2].repitition.append(int(row[1]))

        with open(cv_path, 'r') as f:
            cv = arff.load(f)
        for row in cv['data']:
            self.inst_dic[scen][row[0]][1] = row[2]
        # add image
        self._sort(scen)
        self.inst_dic = self.add_image(scen)

        self.finst_dic[scen] = []
        for i in range(1, 11):
            self.finst_dic[scen].append(
                [self.inst_dic[scen][inst] for inst in self.inst_dic[scen] if self.inst_dic[scen][inst][1] == i])

    def _sort(self, scen):
        """
        :param info: [[solvers], [], [], []]
        :return:
        """
        for inst, va in self.inst_dic[scen].items():
            info = []
            info.append(va[2].solvers)
            info.append(va[2].status_index)
            info.append(va[2].run_time)
            info.append(va[2].repitition)

            info_T = np.asarray(info).T.tolist()
            info_T.sort(key=lambda x: x[0])
            info_O = np.asarray(info_T).T.tolist()
            self.inst_dic[scen][inst][2] = self.inst_dic[scen][inst][2]._asdict()

            self.inst_dic[scen][inst][2]['solvers'] = info_O[0]
            self.inst_dic[scen][inst][2]['status_index'] = np.asarray(
                info_O[1], dtype=np.uint8).tolist()
            self.inst_dic[scen][inst][2]['run_time'] = np.asarray(
                info_O[2], dtype=np.float16).tolist()
            self.inst_dic[scen][inst][2]['repitition'] = np.asarray(
                info_O[3], dtype=np.uint8).tolist()

    def add_image(self, scen):
        """
        inputs: [[local_path, folds, {solvers:[], status_index:[], run_time:[], repitition:[]],...]
        :return: [[local_path, folds, {solvers:[], status_index:[], run_time:[], repitition:[], image_array:[128*128*1]} ],...]
        """
        te2im = TextToImage.TextToImage(scen, self.config, self.inst_dic)
        te2im.convert()
        return te2im.get_aslib_data()

    def get_inst(self):
        return self.inst_dic

    def get_finst(self):
        return self.finst_dic
