# -*-coding:utf8-*-
import datetime,math
import numpy as np
from NHKlib2 import *
"""----About ROT----
the length of test binary array is 64, running 100000 times
ROT using bitwise operations(ROT)  takes   0:00:00.119000
ROT using String  operations(ROT2) takes   0:00:00.143000
&int("1"*d,2) in ROT is to keep the binary array from being overflowed
d is the number of bits kept which is the same as N in MATLAB's function bitshift(A,K,N)
don't know how MATLAB implements the protection of overflow
but &int("1"*d,2) is the fastest way I can do in Python"""
def ROT2(str, n):
	"""return a new string which
	moves the first n bits
	to the right end """
	return str[n:].join(str[:n])

s = "0"*60+"0001"
d = "0"*60+"0110"
print"the length of test binary array: 64"

t0 = datetime.datetime.now()
for i in range(50000):
	ROT(1, 1,64)
	ROT(6, 2,64)
t1 = datetime.datetime.now()
print "\nusing bitwise operations takes " + str(t1-t0)
t2 = datetime.datetime.now()
for i in range(50000):
	ROT2(s, 1)
	ROT2(d, 2)
t3 = datetime.datetime.now()
print "using String  operations takes " + str(t3-t2) + "\n"


Graph1 = np.array([[0,1,1,1],[1,0,0,0],[1,0,0,0],[1,0,0,0]])
Graph2 = np.array([[0,1],[1,0]])  
Graphs = [Graph1,Graph2]
#Graph = {nodeid:[neighbor nodeids]} is the label of node vi in graph  
Glabel1 = {0:int('1000',2),1:int('0101',2),2:int('1100',2),3:int('0101',2)}
Glabel2 = {0:int('1000',2),1:int('1100',2)}
Glabels = [Glabel1,Glabel2]
#Glabel = {nodeid:label}
#Static_D = int(math.ceil(math.log(len(set(Glabel.values())),2)))

newG1 = NH(Graph1,Glabel1,4)
newCSG1 = CSNH(Graph1,Glabel1,4)
newG2 = NH(Graph2,Glabel2,4)
newCSG2 = CSNH(Graph2,Glabel2,4)

print "Graph1:"
for key in Glabel1.keys():
	print str(key),":",bin(Glabel1[key])[2:].zfill(4),"  ",str(key),"->",Graph1[key]
print "Graph2:"
for key in Glabel2.keys():
	print str(key),":",bin(Glabel2[key])[2:].zfill(4),"  ",str(key),"->",Graph2[key]

print "\n"+"NH1:"
for key in newG1.keys():
	print str(key),":",bin(newG1[key])[2:].zfill(4)
print "\n"+"CSNH1:"
for key in newCSG1.keys():
	print str(key),":",bin(newCSG1[key])[2:].zfill(4)

print "\n"+"NH2:"
for key in newG2.keys():
	print str(key),":",bin(newG2[key])[2:].zfill(4)
print "\n"+"CSNH2:"
for key in newCSG2.keys():
	print str(key),":",bin(newCSG2[key])[2:].zfill(4)


print "\nkernel matrix(NH):\n",Calculate_Similarity_Matrix(Graphs,Glabels,1,4,0)
print "\nkernel matrix(CSNH):\n",Calculate_Similarity_Matrix(Graphs,Glabels,1,4,1)
