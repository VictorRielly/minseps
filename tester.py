#!/usr/bin/python
import numpy as np
import allRots as ar
# Test graph
nodes = [0]*6;
nodes[0] = np.array([0,1,2,0,3,4,5]);
nodes[1] = np.array([1,6,7,6,8,7,9]);
nodes[2] = np.array([2,8,10,11,12,13]);
nodes[3] = np.array([10,14,14,15,16,11]);
nodes[4] = np.array([3,12,16,15,17,4]);
nodes[5] = np.array([5,18,9,13,18,17]);
# The edges provide redundant info and
# thus should just be constructed by the
# nodes array. However, the nodes array
# cannot be constructed by the edges, the
# cyclic orientation is lost.
edges = [0]*19;
edges[0] = np.array([0,0]);
edges[1] = np.array([0,1]);
edges[2] = np.array([0,2]);
edges[3] = np.array([0,4]);
edges[4] = np.array([0,4]);
edges[5] = np.array([0,5]);
edges[6] = np.array([1,1]);
edges[7] = np.array([1,1]);
edges[8] = np.array([1,2]);
edges[9] = np.array([1,5]);
edges[10] = np.array([2,3]);
edges[11] = np.array([2,3]);
edges[12] = np.array([2,4]);
edges[13] = np.array([2,5]);
edges[14] = np.array([3,3]);
edges[15] = np.array([3,4]);
edges[16] = np.array([3,4]);
edges[17] = np.array([4,5]);
edges[18] = np.array([5,5]);
myTestRot = ar.Rots(nodes,edges);
# One of these edge ends is easily distinguishable from all others
# this makes the code easy to test for this particular graph.
# Mix up the rotation system.
np.random.seed()
for i in range(0,100):
    int1 = np.random.randint(0,6)
    int2 = np.random.randint(0,6)
    if not (int1 == int2):
        myTestRot.swapVert(int1,int2)
    int3 = np.random.randint(0,19)
    int4 = np.random.randint(0,19)
    if not (int3 == int4):
        myTestRot.swapEdge(int3,int4)
    int5 = np.random.randint(0,6)
    int6 = np.random.randint(0,20)
    myTestRot.rotRot(int5,int6)

