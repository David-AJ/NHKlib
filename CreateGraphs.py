#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
import numpy as np
from scipy.spatial import distance as ds
from scipy import sparse
import datetime
import scipy.io as sio



def createGraphs(matrix, window):
    global t0
    # get number
    num = len(matrix)
    Graphs = []
    # 生成hGraphs
    for i in range(num):
        temp = []
        # 利用滑动窗口生成图
        if i + window <= num:
            temp = matrix[i:i+window,:]
            # 以列向量为变量，计算各个变量间的协方差矩阵cov
            cov = np.cov(np.array(temp).T)
            cov[range(len(cov)), range(len(cov))] = 0
            sortcov = np.array(cov).reshape((cov.size, 1))
            sortcov.sort(0)
            # 取协方差为前10%的作为连通图
            index = sortcov[int(len(sortcov) * 0.9)]
            if index == 0:
                graph = np.where(cov > index, 1, 0).astype(int)
            else:
                graph = np.where(cov >= index, 1, 0).astype(int)
            # sparse
            Graphs.append(sparse.coo_matrix(graph))
            t1 = datetime.datetime.now()
            time = t1 - t0
            print "completed graph: " + "%s" % str(100 * (i + 1.0) / (num))[0:5] + '%' + ' total use: %s' % time
        else:
            break    
    return Graphs



if __name__ == '__main__':
    matrix = sio.loadmat('matrix.mat')['matrix']
    window = input("Please enter the size of window: ")
    t0 = datetime.datetime.now()
    Graphs = createGraphs(matrix, window)
    sio.savemat('Graphs',{'Graphs':np.array(Graphs)})
    # sio.savemat('/root/data/Graphs',{'Graphs':np.array(Graphs)})
    print "Done!"
