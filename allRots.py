#!/usr/bin/python
# For this program, we will need the root rotation systems
# from the flowers as well as a package that allows us
# to efficiently compute graph isomorphisms
import allFlowers as flow
import jgraph as igraph
import numpy as np
from copy import deepcopy as copy
# This code will generate a structure holding all rotation systems
# that minimally separate a particular genus surface. These rotation
# systems will be organized by underlying graph

# First, we will need to define a structure to hold rotation
# systems

class Rots(object):
    def __init__(self,*args):
        # self.nodes is a list of vertices. Each vertex is an
        # array of edge ends in the order they appear at that
        # vertex
        self.nodes = [];
        # self.edges is a list of edges, each edge is a tuple
        # of vertices (the two vertices to which that edge
        # is attached). We use this so we don't ever have to
        # search our vertices to see if a particular edge is
        # attached to that vertex. Edges are assumed to maintain
        # the form (x,y) with x, y vertices and x <= y.
        self.edges = [];
        if (len(args)>0):
            self.nodes = args[0]
        if (len(args)>1):
            self.edges = args[1]

    # This function will be used to rotate a rotation on
    # a single vertex this transformation of a rotation
    # system does not affect the self.edges member.
    # This seems to work
    def rotRot(self,theRot,amount):
        amount = amount % np.size(self.nodes[theRot]);
        newRot = np.concatenate((self.nodes[theRot][amount:],self.nodes[theRot][:amount]));
        self.nodes[theRot] = newRot;

    # This function will be used to swap two vetrices of a 
    # rotation. This transformation affects both the nodes
    # and the edges members. This seems to work
    # Need to test edge cases?
    def swapVert(self,firstVert,secondVert):
        temp = copy(self.edges)
        for i in range(0,np.size(self.nodes[firstVert])):
            if self.edges[self.nodes[firstVert][i]][0] == firstVert:
                temp[self.nodes[firstVert][i]][0] = secondVert
            if self.edges[self.nodes[firstVert][i]][1] == firstVert:
                temp[self.nodes[firstVert][i]][1] = secondVert
            # This if statement ensures and edge is of the form: [x,y]
            # where x < y
            if temp[self.nodes[firstVert][i]][0] > temp[self.nodes[firstVert][i]][1]:
                temp2 = temp[self.nodes[firstVert][i]][0]
                temp[self.nodes[firstVert][i]][0] = temp[self.nodes[firstVert][i]][1]
                temp[self.nodes[firstVert][i]][1] = temp2
#         if self.edges[self.nodes[firstVert][i]][0] > self.edges[self.nodes[firstVert][i]][1]:
#            temp2 = self.edges[self.nodes[firstVert[i]][0]]
#            self.edges[self.nodes[firstVert][i]][0] = self.edges[self.nodes[firstVert][i]][1]
#            self.edges[self.nodes[firstVert][i]][1] = temp2
        for i in range(0,np.size(self.nodes[secondVert])):
            if self.edges[self.nodes[secondVert][i]][0] == secondVert:
                temp[self.nodes[secondVert][i]][0] = firstVert
            if self.edges[self.nodes[secondVert][i]][1] == secondVert:
                temp[self.nodes[secondVert][i]][1] = firstVert
            # This if statement ensures and edge is of the form: [x,y]
            # where x < y
            if temp[self.nodes[secondVert][i]][0] > temp[self.nodes[secondVert][i]][1]:
                temp2 = temp[self.nodes[secondVert][i]][0]
                temp[self.nodes[secondVert][i]][0] = temp[self.nodes[secondVert][i]][1]
                temp[self.nodes[secondVert][i]][1] = temp2
#         if self.edges[self.nodes[secondVert][i]][0] > self.edges[self.nodes[secondVert][i]][1]:
#            temp2 = self.edges[self.nodes[secondVert][i]][0]
#            self.edges[self.nodes[secondVert][i]][0] = self.edges[self.nodes[secondVert][i]][1]
#            self.edges[self.nodes[secondVert][i]][1] = temp2
        tempVert1 = copy(self.nodes[secondVert])
        self.nodes[secondVert] = self.nodes[firstVert]
        self.nodes[firstVert] = tempVert1
        self.edges = temp

      
         

    # This function swaps two edge labels. It seems to work
    # Need to test edge cases?
    def swapEdge(self,firstEdge,secondEdge):
        tempNodes = copy(self.nodes)      
        tempEdge1 = copy(self.edges[secondEdge])
        tempEdge2 = copy(self.edges[firstEdge])
        for i in range(0,np.size(self.nodes[self.edges[firstEdge][0]])):
            if self.nodes[self.edges[firstEdge][0]][i] == firstEdge:
                tempNodes[self.edges[firstEdge][0]][i] = secondEdge
        for i in range(0,np.size(self.nodes[self.edges[firstEdge][1]])):
            if self.nodes[self.edges[firstEdge][1]][i] == firstEdge:
                tempNodes[self.edges[firstEdge][1]][i] = secondEdge
        for i in range(0,np.size(self.nodes[self.edges[secondEdge][0]])):
            if self.nodes[self.edges[secondEdge][0]][i] == secondEdge:
                tempNodes[self.edges[secondEdge][0]][i] = firstEdge
        for i in range(0,np.size(self.nodes[self.edges[secondEdge][1]])):
            if self.nodes[self.edges[secondEdge][1]][i] == secondEdge:
                tempNodes[self.edges[secondEdge][1]][i] = firstEdge
        self.nodes = tempNodes
        self.edges[firstEdge] = tempEdge1
        self.edges[secondEdge] = tempEdge2

    # Ensures the labels of new edge ends in a vertex are increasing
    # in order.
    def relableEdgeEnds(self,lastKnownEdgeEnd,vertex):
        for i in range(0,len(self.nodes[vertex])):
            if self.nodes[vertex][i] > lastKnownEdgeEnd:
                lastKnownEdgeEnd += 1;
                self.swapEdge(self.nodes[vertex][i],lastKnownEdgeEnd)
        return lastKnownEdgeEnd;

    # Relabels vertices based on how they are connected to edge ends
    # also rotates the vertices to make the connecting edge the first
    # one.
    def relableVertices(self,lastKnownVertex,myVertex):
        for i in range(0,len(self.nodes[myVertex])):
            # Assumes the second entry of each end corresponds
            # to the largest vertex label
            if self.edges[self.nodes[myVertex][i]][1] > lastKnownVertex:
                lastKnownVertex += 1
                # Rotate this newly found vertex so its first edge end
                # is the one that discovered the vertex
                indexofEdgeEnd = np.where(self.nodes[self.edges[self.nodes[myVertex][i]][1]] == self.nodes[myVertex][i])[0][0]; 
                self.rotRot(self.edges[self.nodes[myVertex][i]][1],indexofEdgeEnd)
                self.swapVert(self.edges[self.nodes[myVertex][i]][1],lastKnownVertex)
        return lastKnownVertex;
   

    # This function will place the rotation system in 
    # cannonical form based on the edge end, the edge
    # end will be specified by its vertex number and 
    # edge end number on that vertex. Not completed yet?
    def setCannon(self,vertexNum,edgeNum):
        # First, we set vertex number "vertexNum" as the
        # first vertex, and edge end "edgeNum" as the first edge
        if vertexNum != 0:
            self.swapVert(0,vertexNum);
        if edgeNum != 0:
            self.rotRot(0,edgeNum);

        # Initialize the total number of edges to numEdges 
        self.numEdges = np.size(self.edges);
        self.numVertices = np.size(self.nodes);
        lastKnownEdgeEnd = -1;
        lastKnownVertex = 0;
        for i in range(0,self.numVertices):
            lastKnownEdgeEnd = self.relableEdgeEnds(lastKnownEdgeEnd,i)
            lastKnownVertex = self.relableVertices(lastKnownVertex,i)
         
    # Compares self.nodes to the rotation system of 
    # another Rots object
    def isSame(self,otherNodes):
        isSame = True;
        if len(self.nodes) == len(otherNodes):
            for  i in range(0,len(self.nodes)):
                if not np.array_equal(self.nodes[i],otherNodes[i]):
                    isSame = False;
                    break;
        return isSame;

    # Test if rotation system
    # is isomorphic (no graph isomorphism test first)
    # Lots of expensive deep copies. Need to make this more
    # efficient.
    def isIsomorphic(self,templateNodes):
        tempRot = copy(self);
        # worse case scenario, we have to try all edge ends
        # better case is to use graph isomorphism to wittle
        # down our choices in the beginning.
        areEqual = False;
        for i in range(0,len(tempRot.nodes)):
            for j in range(0,len(tempRot.nodes[i])):
                tempRot.setCannon(i,j)
                if (tempRot.isSame(templateNodes)):
                    areEqual = True;
                    return areEqual;
                tempRot = copy(self);
        return areEqual;



