import math
from sklearn import preprocessing
from sklearn.neighbors import KernelDensity
import numpy as np
from sklearn.neighbors import kde
import scipy.stats as sta
from openpyxl import Workbook


def gaussian1(x):
    '''
    一维的高斯估计
    x -- 一维数组
    return: gaussian 估计密度值
    '''
    re = sta.gaussian_kde(x)
    return re(x)


def gaussian2(x,y):
    '''
    二维的高斯估计
    x ,y-- 一维数组
    return: gaussian 估计密度值
    '''
    rt = np.vstack([x, y])
    re = sta.gaussian_kde(rt)
    return re(rt)


def p_d_a(l,fenmu):
    '''
    计算pd|a
    :param l:  二维list --存array
    fenmu : 存储密度*n  的一组数据      -----  ndarry 一维数组
    :return: pdx 的list
    '''
    # 决定分母的dex
     #将字典按照顺序输入到list中
    ldex = list()
    # for i in dexD:
    #     for i1 in range(0,len(dexD[i])):
    #         # print("ttetete",dexD[i][i1], type(dexD[i][i1])) # int
    #         ldex.append(dexD[i][i1])

    # 每个标签的 每个数据 的条件密度 p d /xi 和对应的log

    lr = list()
    dex = 0  # 遍历索引
    print("len of l",len(l))
    print("len of lk", len(l[0]))
    print("lend of fm: ",len(fenmu))
    for k in range(0, len(l)):
        dex = 0
        for k1 in range(0, len(l[k])):
            # print("fenmu",fenmu[dex])
            pdxi = l[k][k1] / fenmu[dex]
            # print(k,k1,"p",pdxi)
            dex+=1
            lr.append(pdxi)  # 每次加一个 数
            if (dex == len(fenmu)):
                break
    print("dex: ",dex)
    # print("test", lr[0], type(lr[0]))  # ndarray
    # print("lr -- pdx",lr)
    return lr


def condition_HXD(d, a, fenmu):
    '''
    计算H X|D
    :param d: list/1 array -- 类标签(跟a等长度)
    :param a: list/1 array
    fenmu :  存储密度*n  的一组数据      -----  ndarry 一维数组
    :return: 条件熵 H（D|X）
    '''
    d1 = np.unique(d)  # 将d中重复数值剔除
    # 形成字典,key:类标签值（不重复）
    dD = {}
    lD = dict.fromkeys(d1, 0)  # 计数每个类别的数个数
    dexD = {}  # 用来存储对应被分类元素的下标
    # 开始将a分类
    for i in range(0, len(a)):
        dD.setdefault(d[i], []).append(a[i])  # 将a的值逐个写入dD中
        dexD.setdefault(d[i],[]).append(i)  # a下标值写入
        lD[d[i]] += 1
    atr = np.array(a)  # ndarray
    aa2 = atr.reshape(len(a), 1)  # 2d ndarray
    # 计算数据中标签（d/xi）的条件密度  && (xi|d)分子
    # 放入list中
    l = list()
    print("lenlD: ",len(lD))
    for j in lD:
        at = dD[j];  # list
        aa = np.array(at)  # ndarray
        aa2t = aa.reshape(len(aa), 1)  # 2d ndarray
        h = h1decision(np.array(at))  # 全体连续数据的h
        print("at: ",at)
        print("h: ",h)
        pad = kde.KernelDensity(kernel='gaussian', bandwidth=h).fit(aa2t).score_samples(aa2)  # p(x,d
        # print("log_pxd",log_pad)
        pad = np.exp(pad)
        tmp = len(at) * pad  # p d|x 的分子
        # print("p",tmp)
        l.append(tmp)  # 每个标签的每个数据计算出的分子组成之一
        print(j," done")
    print("sum tmp: ", sum(tmp))
    pdx = p_d_a(l, fenmu)
    #lpdx =
    # 计算条件熵
    ree = 0

    # print("ttest",log_pad[0],type(log_pad[0]))  # float
    # print("tteste",log_pad[0][0],type(log_pad[0][0]))
    # print("ttts", pdx[0],type(pdx[0])) #ndarry
    # print("llltt",np.array(pdx[0]),type(np.array(pdx[0])))  #ndarray
    for k in range(0, len(pad)):
        nlog_pad = np.array(pad[k])
        npda = np.array(pdx[k])
        ree += npda.dot(nlog_pad)
    # print("reee",ree,type(ree))
    hxd = (-1/len(a)) * ree
    return hxd


def format_excel(name,feature):
    '''
    将传入数组以列形式传入excel
    :param name: String 为sheet的名字
            # label:第0行的标签  --ndarray 二维数组
            feature: 具体内容 -- ndarray  二维数组
    :return: wb - >在主函数中再
    使用wb.save("名字.xlsx")
    '''
    wb = Workbook()
    ws = wb.create_sheet(name)

    # label_input = []
    # for l in range(len(label)):
    #     label_input.append(label[l][0])

    # ws.append(label_input) #标签

    for f in range(len(feature[0])):
        ws.append(feature[:, f].tolist())   #写入一行
    return wb
    # wb.save("chehongshu.xlsx")

def kde2D(x, y, bandwidth):
    """
    kde计算联合概率
    :param x: 一维数组x
    :param y: y
    :param bandwidth:
    :return: 联合概率 -- np.darray
    """
    # xy_sample = np.vstack([yy.ravel(), xx.ravel()]).T
    xy_train  = np.vstack([y, x]).T
    # vstack--竖直堆叠序列中的数组（行方向），使两个数组成为一行
    # print("1:" ,np.vstack([y, x]),type(np.vstack([y, x])))
    # print("2:" ,xy_train,type(xy_train))
    # .T使得两数组y，x一一对应形成一个个数组length（x）
    # print(xy_train)
    kde_skl = KernelDensity(kernel='gaussian',bandwidth=bandwidth).fit(xy_train)
    log_P = kde_skl.score_samples(xy_train)
    P = np.exp(kde_skl.score_samples(xy_train))
    # print("log_P:",log_P)
    # print("P :",P)
    return P

def minmax(X):
    '''
    最大最小值标准化【0，1】
    :param X: 需要标准化的二维数组ndarray
    :return: res :标准化后的一维数组ndarray
    '''
    x = X.reshape(len(X), 1)
    min_max_scale = preprocessing.MinMaxScaler(feature_range=(0.00000000001, 1))
    tmp = min_max_scale.fit_transform(x)
    res = tmp.flatten()
    return res

def h1decision(b):
    '''
    计算带宽
    :param b:一维数组  -- ndarray
    :return: 返回这组数据带宽-- int
    '''
    # 这里使用样本标准差
    if(len(b)==1):
        return 1.05*0.08
    a1 = np.std(b,ddof=1)
    l = len(b)
    tmp = math.pow(l,-0.2)
    res1 = 1.05*a1*tmp
    return res1
    # logpx = kde.KernelDensity(kernel='gaussian', bandwidth=res).fit(r).score_samples(r)
#[1.07046471 1.07009261 1.10854638 ... 0.97120163 0.97120163 0.97120163]
    # res = m.minmax(np.exp(logpx))
    # logpx = kde.KernelDensity(kernel='gaussian', bandwidth=res1).fit(r).score_samples(r)
#[1.07046487 1.07009279 1.10854615 ... 0.97120172 0.97120172 0.97120172]



def h2decision(a,b):
    """
    二维变量的带宽处理
    :param a: 一维数组  -- ndarray
    :param b: 一维数组  -- ndarray
    :return: 二维数据的带宽
    """
    tmp = np.concatenate((a, b), axis=0)
    st = np.std(tmp,ddof=1)
    # print("a:",a)  # 计算样本标准差
    # l = len(a)

    # print("l: ",l," l1:",l1)
    # tmp = math.pow(l, -0.2)
    l1 = len(a) + len(b)  # 两组数据总长
    tmp1 = math.pow(l1,-0.2)
    # res = 1.05 * st * tmp
    res1 = 1.05 * st * tmp1
    # print("res:", res, "res1: ", res1)
    return res1

def dTl(x):
    '''
    dataframe转为list
    :param x: DataFrame
    :return: 一维数组
    '''
    temp = x.values
    res = temp.flatten()  #降维
    return res



def lT2n(x):
    '''
    list转二维数组
    x -- list
    return ： 二维数组
    '''
    a1 = np.array(x)
    # print("a1",type(a1),a1)
    re = a1.reshape((len(a1), 1))
    return re
