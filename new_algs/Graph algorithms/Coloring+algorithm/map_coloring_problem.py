# -*- coding: utf-8 -*-
# @Author: Peter
# @Date:   2019-01-02 14:21:27
# @Last Modified by:   Peter
# @Last Modified time: 2019-01-06 15:38:53
from bs4 import BeautifulSoup
from flask import Flask, render_template
app = Flask(__name__)


def color_norepeat(adjmat, colors, node_num):
    """

    判断颜色是否重复

    Arguments:
        adjmat {list} -- 地图的邻接矩阵
        colors {list} -- 省份的颜色列表
        node_num {int} -- 省份节点编号

    Returns:
        bool -- 如果颜色不重复返回True，否者返回False
    """
    for i, item in enumerate(adjmat[node_num]):
        if item == 1 and colors[i] == colors[node_num]:
            return False
    return True


def search(adjmat, node_num, colors, color_num):
    """

    枚举法求解地图着色问题

    Arguments:
        adjmat {list} -- 地图的邻接矩阵
        node_num {int} -- 省份节点编号
        colors {list} -- 省份的颜色列表
        color_num {int} -- 颜色编号

    Returns:
        bool -- 如果当前方案满足条件就返回True，否者返回False
    """
    n = len(adjmat)
    if node_num >= n:
        return True
    else:
        for i in range(1, color_num + 1):
            colors[node_num] = i
            if color_norepeat(adjmat, colors, node_num):
                if search(adjmat, node_num + 1, colors, color_num):
                    return True
            # colors[node_num] = 0
    return False


def mcp(adjmat):
    """

    map coloring problem

    Arguments:
        adjmat {list} -- 地图的邻接矩阵

    Returns:
        list, int -- 返回颜色匹配方案，已经使用的颜色总数
    """
    color_sum = 4
    n = len(adjmat)
    colors = [0 for _ in range(n)]
    for color_num in range(1, color_sum + 1):
        if search(adjmat, 0, colors, color_num):
            # print('The min number of colors:', color_num)
            break
    return colors, color_num


def read_data():
    """
    读取数据
    """
    adjmat = []
    with open('data.txt', 'r') as f:
        for line in f:
            line = line.strip()
            arr = [int(value) for value in line.split(',')]
            adjmat.append(arr)
    return adjmat


def draw_block_map(colors, indices, file_name):
    """

    使用BeautifulSoup给svg地图上色

    Arguments:
        colors {list} -- 待涂颜色
        indices {list} -- 列表每个元素分别对应每个城市，表示该城市对应的颜色
        file_name {list} -- 待涂地图文件名

    Returns:
        str -- 上完色的xml格式svg矢量图
    """
    svg = open(file_name, 'r', encoding='utf-8').read()  # 读取地图数据
    soup = BeautifulSoup(svg, "lxml")
    paths = soup.findAll('path')
    # 颜色列表
    count = 0
    for p in paths:
        color = colors[indices[count]]
        p['fill'] = color  # 改变地图对应区域的颜色
        count += 1
    return soup.prettify()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dyemap')
def dyemap():
    file_name = 'ChinaMap.svg'
    # output_file = 'output.svg'
    colors = ['red', 'green', 'blue', 'gray']
    adjmat = read_data()
    colors_indices, color_num = mcp(adjmat)
    colors_indices = [i - 1 for i in colors_indices]
    result_svg = draw_block_map(colors, colors_indices, file_name)
    # with open(output_file, 'w', encoding='utf-8') as f:
    #     f.write(result_svg)
    return result_svg + '<div>最少使用颜色数量：' + str(len(list(set(colors)))) +'</div>'


@app.route('/restore')
def restore():
    file_name = 'ChinaMap.svg'
    svg = open(file_name, 'r', encoding='utf-8').read()  # 读取地图数据
    return svg


if __name__ == '__main__':
    # file_name = 'ChinaMap.svg'
    # output_file = 'output.svg'
    # colors = ['red', 'green', 'blue', 'gray']
    # provinces = ["广西", "广东", "云南", "贵州", "湖南", "江西", "福建",
    #             "浙江", "安徽", "湖北", "重庆", "四川", "西藏", "青海",
    #             "新疆", "甘肃", "陕西", "宁夏", "内蒙", "北京", "黑龙江",
    #             "吉林", "辽宁", "天津", "河北", "山西", "河南", "江苏",
    #             "山东", "上海", "海南", "台湾", "香港", "澳门"]
    # adjmat = read_data()
    # colors_indices, color_num = mcp(adjmat)
    # colors_indices = [i - 1 for i in colors_indices]
    # result_svg = draw_block_map(colors, colors_indices, file_name)
    # with open(output_file, 'w', encoding='utf-8') as f:
    #     f.write(result_svg)
    app.run(port=8000, host='0.0.0.0')
