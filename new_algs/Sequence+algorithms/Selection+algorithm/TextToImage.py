import os
import sys
import math
import numpy as np
from PIL import Image
from sklearn import preprocessing as pp


class TextToImage(object):
    """
    the class for converting the text to image
    input: [[local_path, folds, {solvers:[], status_index:[], run_time:[], repitition:[]],...]
    output: [[local_path, folds, {solvers:[], status_index:[], run_time:[], repitition:[], image_array:[128*128*1]} ],...]
    """

    def __init__(self, scen, config, aslib_data):
        self.config = config
        self.aslib_data = aslib_data
        self.scen = scen
        self.new_scale = list(range(0, 256, 20))

    def pixel_scale(self, num_seq, raw_scale):
        assert len(self.new_scale) == len(raw_scale)
        return [self.new_scale[raw_scale.index(num_seq[i])] for i in range(len(num_seq))]

    def convert(self):
        """
        inputs: {scen: { inst: [path, folds, info{} ]}}
        :return:
        """
        norm_container = []
        norm_index = []
        for inst in self.aslib_data[self.scen]:
            ch_seq = self._get_ch(self.aslib_data[self.scen][inst][0])
            num_seq = [ord(c) for c in ch_seq]
            raw_scale = list(set(num_seq))
            raw_scale.sort()
            num_seq = self.pixel_scale(num_seq, raw_scale)
            # num_seq = np.array([ord(c) for c in ch_seq])
            squ_mat = self._seq_to_mat(num_seq)
            norm_container.extend(squ_mat)
            norm_index.append(inst)
            # self.aslib_data[self.scen][inst][2] = self.aslib_data[self.scen][inst][2]._asdict()
            self.aslib_data[self.scen][inst][2]['image_array'] = squ_mat
        # TODO normalize image array
        # TODO by this operation, the value after this op is not easy to differ
        # preprocessed by subtracting the mean and normalizing each feature
        norm_container = pp.scale(norm_container)
        ind = 0
        span = self.config['image_size'][0]
        for inst in norm_index:
            self.aslib_data[self.scen][inst][2]['image_array'] = np.asarray(norm_container[ind * span: (ind + 1) * 128],
                                                                            dtype=np.float16).reshape(128, 128, 1)
            ind += 1
            # self.aslib_data[self.scen][inst][2].image_array = self.aslib_data[self.scen][inst][2]._asdict()

    def _get_ch(self, inst):
        """
        :param inst: local_path
        :return:
        """
        with open(inst, 'r') as f:
            lines = f.readlines()
            mark = 0
            index = 0
            while not mark:
                if lines[index][0] == 'p':
                    mark = 1
                index += 1
            seq = "".join(lines[index:])
            seq.replace(' 0\n', '\n')

        return seq

    def _seq_to_mat(self, num_seq):
        if self.config['round_method'] == 'ceil':
            leng = math.ceil(math.sqrt(len(num_seq)))
        if self.config['round_method'] == 'floor':
            leng = math.floor(math.sqrt(len(num_seq)))
        if self.config['round_method'] == 'round':
            leng = round(math.sqrt(len(num_seq)))
        else:
            raise ReferenceError('#leng can not be computed')

        num_mat = np.resize(num_seq, [leng, leng])
        image = Image.fromarray(num_mat.astype('uint8')).convert('L')
        if self.config['interpolation_method'] == "NEAREST":
            squ_mat = image.resize(self.config['image_size'], Image.NEAREST)
        if self.config['interpolation_method'] == "LANCZOS":
            squ_mat = image.resize(self.config['image_size'], Image.LANCZOS)
        if self.config['interpolation_method'] == "BILINEAR":
            squ_mat = image.resize(self.config['image_size'], Image.BILINEAR)
        if self.config['interpolation_method'] == "BICUBIC":
            squ_mat = image.resize(self.config['image_size'], Image.BICUBIC)

        return np.asarray(squ_mat, dtype=np.uint16)

    def get_aslib_data(self):
        return self.aslib_data
