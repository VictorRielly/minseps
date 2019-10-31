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
    def __init__(self,arg*):
        if (arg[0]):
            self.nodes = arg[0]
        if (arg[1]):
            self.edges = arg[1]
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

    # This function will be used to rotate a rotation on
    # a single vertex this transformation of a rotation
    # system does not affect the self.edges member.
    def rotRot(self,theRot,amount):
        amount = amount % np.size(self.nodes[theRot]);
        newRot = np.concatenate((self.nodes[theRot][amount:],self.nodes[theRot][:amount]));
        self.nodes[theRot] = newRot;

    # This function will be used to swap two vetrices of a 
    # rotation. This transformation affects both the nodes
    # and the edges members.
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

      
         

    # This function swaps two edge labels
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

        # Initialize the number of discovered edges to 1
        self.numEdges = np.size(self.edges);

        # Now, we reorder and relabel all of the edge ends
        # and vertices based on the first vertex and edge end
        # to do this, we need to keep track of the vertices
        # as we discover them in a breadth first search and the
        # edge ends as we discover them as well.
        #vertices = np.zeros(len(self.nodes));
        edges = []
        vertices = []
        #edges = np.zeros(self.numEdges);
        # Push the first edge into edges
        edges.append(0)
        # Push the first vertex into vertices
        vertices.append(0)
      
        # lastEdge set to -1 to start the loop.
        lastEdge = -1; 
        lastVertex = 0;
        vertexOrder = 0;
        currentEdge = 0;
        currentVertex = 0;
      
        # test counter
        counter = 0      
        #while (currentEdge < self.numEdges):
        # This code works for the base case, now we need
        # to make it work for all cases in the while loop
        while ((currentEdge > lastEdge or currentVertex > lastVertex)and counter < 2):
            print(vertices);
            print(edges);
            print(self.nodes);
            print(self.edges);
            print("1 \n");
            # Relables all of the edges so they read 0,1,2,... for the
            # first vertex, and currentEdge, currentEdge+1, ... for
            # the nth vertex. 
#         for j in range(lastVertex,currentVertex+1):
            print("The current Edge is:")
            print(currentEdge)
            lastEdge = currentEdge
            for i in range(0,np.size(self.nodes[lastVertex])):
                if currentEdge < self.nodes[lastVertex][i]:
                    self.swapEdge(currentEdge,self.nodes[lastVertex][i])
                    currentEdge += 1;
                if currentEdge == self.nodes[lastVertex][i]:
                    currentEdge += 1;
            # We have overcounted by 1
            currentEdge -= 1;
#         newEdgeNum = currentEdge;
#         for i in range(0,np.size(self.nodes[lastVertex])):
#            if newEdgeNum < self.nodes[lastVertex][i]:
#               newEdgeNum += 1
#               self.swapEdge(newEdgeNum,self.nodes[lastVertex][i])         
#            if newEdgeNum == self.nodes[lastVertex][i]:
#               newEdgeNum += 1   
            lastVertex = currentVertex
            # Adds all the previously undiscovered edges in the
            # current vertex to the list of edges
#         for i in range(0,np.size(self.nodes[vertices[currentVertex]])):
#            if not (self.nodes[vertices[currentVertex]][i] in edges[lastEdge:currentEdge+1]):
#               edges.append(self.nodes[vertices[currentVertex]][i]);
#               currentEdge += 1;
            # Unnecessarily computationaly expensive, if all went right, we
            # should just be able to append currentEdge:newEdgeNum.
            for i in range(0,np.size(self.nodes[vertices[lastVertex]])):
                if not (self.nodes[vertices[lastVertex]][i] in edges):
                    edges.append(self.nodes[vertices[lastVertex]][i]);

            # Now that we have added all the new edges to our list
            # of edges, we are ready to add all the new vertices to the list
            # list of vertices.
            for i in range(lastEdge,currentEdge+1):
                if not (self.edges[edges[i]][1] in vertices):
                    vertices.append(self.edges[edges[i]][1]);
                    currentVertex += 1;
            print(vertices);
            print(edges);
            print(lastVertex);
            print(currentVertex);
            print(self.nodes);
            print(self.edges);
            print("2.5 \n");
            # Now we need to swap the vertex labels so vertices
            # reads 0,1,2,3,...
            for i in range(vertexOrder,currentVertex+1):
                if lastVertex < vertices[i]:
                    self.swapVert(i, vertices[i]);
                    # vertices is not a member of self and thus
                    # the update of vertices is not handled by
                    # self.swapVert
                    # This is a deep copy in disguise since
                    # vertices[i] is an integer. 
                    temp = vertices[i]
                    vertices[i] = i;
                    # pretty inefficient as it is a nested loop
                    # notice, we do not need to go from lastVertex
                    # to end.
                    for j in range(i+1,currentVertex+1):
                        if vertices[j] == i:
                            vertices[j] = temp;

            # All vertices up to currentVertex have been reordered.
            vertexOrder = currentVertex + 1;

            print(vertices);
            print(edges);
            print(lastVertex);
            print(currentVertex);
            print(self.nodes);
            print(self.edges);
            print("2 \n");
            # Last, but not least, for all the new vertices, we
            # rotate the vertex so the smallest edge is first.
            for i in range(lastVertex,currentVertex+1):
                # find the minimum edge
                smallestInd = 0;
                smallest = self.nodes[vertices[i]][0];
                for j in range(0,np.size(self.nodes[vertices[i]])):
                    if self.nodes[vertices[i]][j] < smallest:
                        smallest = self.nodes[vertices[i]][j];
                        smallestInd = j;
                self.rotRot(vertices[i],smallestInd);
            lastVertex += 1;
            print(vertices);
            print(edges);
            print(lastVertex);
            print(currentVertex);
            print(self.nodes);
            print(self.edges);
            print("3 \n");
#         counter += 1;
         
            

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
