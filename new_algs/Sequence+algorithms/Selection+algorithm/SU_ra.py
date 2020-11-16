import pandas as pa
from sklearn import metrics
# import operator
# from functools import reduce

Hlab = 1.7345022438597424
Hcxy = []    # 二维表存放特征间联合熵
SU = []     # 二维表，特征间SU

#计算特征间SU

if __name__ == '__main__':
    nyse1 = pa.read_excel('abH.xlsx', usecols=[1])  # 特征的信息熵存放在该表格中，第一列绝对，第二列相对
    nyse2 = pa.read_excel('reH.xlsx', usecols=[1])
    temp1 = nyse1.values
    a = temp1.flatten()
    temp2 = nyse2.values
    b = temp2.flatten()
    for col1 in range(1, 21):
        #nyse = pa.read_excel('Ig-Hx&Hy.xlsx', usecols=[col1])
        nyse = pa.read_excel('raHxy.xlsx', usecols=[col1]) #联合熵表格，每一列对应一个绝对特征
        tmp = nyse.values
        tmp = tmp.flatten()
        Hcxy.append(tmp)
    # result_NMI=metrics.normalized_mutual_info_score(a, b)
    # print(entro_lab)
    for x in range(0, 20):
        sut = []
        for y in range(0, 20):
            print("a",x,": ",a[x])
            print("b", y, ": ", b[y])
            print("Hcxy", x," ",y, ": ", Hcxy[x][y])
            st = 2*(a[x]+b[y]-Hcxy[y][x])/(a[x]+b[y])
            sut.append(st)
        SU.append(sut)

    data = pa.DataFrame(SU)
    data.to_excel("SU_r&a.xlsx")
