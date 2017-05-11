#!/usr/bin/python2.7
# -*-coding:utf8-*-
"""---------------------------------使用说明---------------------------------
Python版本: Python 2.7 64bits
需要的库： Numpy 可访问http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy下载
导入本库使用 from NHKlib import *
传入参数的格式设定：
	每一个Labeled Graph数据都使用两个字典Graph,Glabel存储,存储格式

	Graph = {nodeid:[neighbor nodeids]}  Graph记录了图中各个节点的连通关系,一经输入不再改变
	Glabel = {nodeid:label}     Glabel记录了图中各个节点对应的label,初始label为原始导入数据

	Glabel会在kernel method的不同进度中不断更新

	首先利用labelMapping函数会将label更新生成初始的定长为D的二进制数组

	使用方法： Glabel = labelMapping(Glabel)

	D的获取方法： D = get_D(Glabel)

	所有的Graph存储在一个Graphs数组中    Graphs = [Graph1,Graph2,Graph3,...]
	所有更新后的Glabel存储在一个Glabels数组中 Glabels = [Glabel1,Glabel2,Glabel3,...]

计算kernel matrix的方法:
	获取上述清洗好的参数 Graphs Glabels D,传入Calculate_Similarity_Matrix()函数

	传参规范：Calculate_Similarity_Matrix(Graphs, Glabels, R, D, Hashtype)
	
	R 为想要迭代的次数, Hashtype 表示哈希方式: 0 为简单哈希(NH), 1 为计数敏感哈希(CSNH)

	该函数会返回kernel矩阵,可以直接使用print 查看结果
	print Calculate_Similarity_Matrix(Graphs, Glabels, R, D, Hashtype)

---------------------------------Copyrgiht@Jiao Yuhang---------------------------------"""



import random,math
import numpy as np

def get_D(Glabel):
	"""get th length of binary array"""
	return int(math.ceil(math.log(len(set(Glabel.values())),2)))

def Calculate_Similarity_Matrix(Graphs, Glabels, R, d, Hashtype):
    """Graphs->list of Graph
    Glabels->list of Glabel
    R->maximum order of neighborhood hash
    d->length of binary array
    Hashtype-> 0 represents Neighborhood hash
               1 represents Count-Sensitive Neighborhood hash

    return a kernel matrix"""
    kernel_matrix = np.zeros((len(Graphs),len(Graphs)))
    if Hashtype==0: # Neighborhood hash
    	for r in range(R):
            print "Calculating Similarity Matrix in ",str(r+1)," oder..."
            temp = np.eye(len(Graphs))
            templabels = []
            for i in range(len(Graphs)):
    	        Glabels[i] = NH(Graphs[i],Glabels[i],d)
    	        # Glabels[i] = CSNH(Graphs[i],Glabels[i],d)
    	        templabels.append(Glabels[i].values())
    	        sort(templabels[i],d)
    	        # each templabels represent a graph's sorted Hashed-labels
            for i in range(len(templabels)):
                for j in range(i+1,len(templabels)):
                    print "Comparing Graph ",str(i+1)," and Graph ",str(j+1),"..."
                    temp[i][j] = temp[j][i] = Compare_Labels(templabels[i],templabels[j])
            kernel_matrix += temp
    else :          # Count-Sensitive Neighborhood hash
        for r in range(R):
            print "Calculating Similarity Matrix in ",str(r+1)," oder..."
            temp = np.eye(len(Graphs))
            templabels = []
            for i in range(len(Graphs)):
    	        # Glabels[i] = NH(Graphs[i],Glabels[i],d)
    	        Glabels[i] = CSNH(Graphs[i],Glabels[i],d)
    	        templabels.append(Glabels[i].values())
    	        sort(templabels[i],d)
    	        # each templabels represent a graph's sorted Hashed-labels
            for i in range(len(templabels)):
    	        for j in range(i+1,len(templabels)):
    	            print "Comparing Graph ",str(i+1)," and Graph ",str(j+1),"..."
    	            temp[i][j] = temp[j][i] = Compare_Labels(templabels[i],templabels[j])
            kernel_matrix += temp		
    kernel_matrix = kernel_matrix/R
    print "Calculating Similarity Matrix finished!"
    return kernel_matrix

def ROT(label, n, d):
    """label->the integer
    n->the length of offset
          d->the length of binary array

    return a new label which
    moves the first n bits
    to the right end """
    return (label << n) + (label >> d - n) & int("1" * d, 2)

def sort(nlist, d):
    """nlist->the list of original neighborhood labels
    d->the length of binary array

    turn the original labels into the sorted labels"""
    bucket = [[] for i in range(2)]
    for i in range(1, d + 1):  # loop for d times
        for value in nlist:
            bucket[value % (2**i) / (2**(i - 1))
                   ].append(value)  # sort on i bit
        del nlist[:]
        for each in bucket:
            nlist.extend(each)  # combine each bucket
        bucket = [[] for i in range(2)]
    del bucket

# count unique neighborhood labels


def UNL(nlist, d):
    """nlist->original neighborhood labels list
    d->the length of binary array

    return a dictionary of the
    unique neighborhood labels and thier numbers"""
    sort(nlist, d)
    dic = {}
    for i in range(len(nlist)):
        if i == 0:
            dic[nlist[i]] = 1
        elif nlist[i] == nlist[i - 1]:
            dic[nlist[i]] += 1
        else:
            dic[nlist[i]] = 1
    return dic

# replace original label with a binary array
def labelMapping(Glabel):
    nlabels = []
    mapping = {}
    newGlabel = {}
    while len(nlabels) < len(set(Glabel.values())):
        nlabel = random.randint(1, len(set(Glabel.values())))
        if nlabel not in nlabels:
            nlabels.append(nlabel)
    for i in range(len(set(Glabel.values()))):
        mapping[Glabel.values()[i]] = nlabels[i]
    for nodeid in Glabel.keys():
        newGlabel[nodeid] = mapping[Glabel[nodeid]]
    del nlabels
    del mapping
    return newGlabel


def NH(Graph, Glabel, d):
    """Graph->{nodeid:[neighbor nodeids]}
    Glabel->{nodeid:label}
    d->the length of binary array

    return a new Glabel with N-Hashed label"""
    newGlabel = {}
    for Vi in Glabel.keys():
    	# print "Updating NH Labels..."
        # update node Vi's label
        label = ROT(Glabel[Vi], 1, d)
        for neighbor in Graph[Vi]:
            label = label ^ Glabel[neighbor]
        newGlabel[Vi] = label
    # print "Updating NH Labels finished!"
    return newGlabel


def CSNH(Graph, Glabel, d):
    """Graph->{nodeid:[neighbor nodeids]}
    Glabel->{nodeid:label}
    d->the length of binary array

    return a new Glabel with CSN-Hashed label"""
    newGlabel = {}
    for Vi in Glabel.keys():
    	# print "Updating CSNH Labels..."
        # update node Vi's label; ROT1(l(Vi))
        label = ROT(Glabel[Vi], 1, d)
        neighbor = [Glabel[i] for i in Graph[Vi]]
        # count the unique neighborhood labels
        # newNeighbor = {uniquelabel:number of occurrences}
        newNeighbor = UNL(neighbor, d)
        for ulabel in newNeighbor.keys():
            # ROT1(l(Vi)) ^ l'(vadj); l'(vadj) =  ROTo(l(vadj) ^ o)
            label = label ^ ROT(ulabel ^ newNeighbor[
                                ulabel], newNeighbor[ulabel], d)
        newGlabel[Vi] = label
    # print "Updating CSNH Labels finished!"
    return newGlabel

def Compare_Labels(labels1, labels2):
    """labels1->sorted label list of the graph1
    labels2->sorted label list of the graph2

    return a similarity value of two graphs"""
    na = len(labels1)
    nb = len(labels2)
    c = 0.0
    i = j = 0
    while i < na and j < nb:
        if labels1[i] == labels2[j]:
            c += 1
            i += 1
            j += 1
        elif labels1[i] < labels2[j]:
            i += 1
        else:
            j += 1
    return c / (na + nb - c)

