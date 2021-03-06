import argparse
import os
import re
import sys
import time

# Command line arguments
parser=argparse.ArgumentParser(description='Calculate the shortest path between all pairs of vertices in a graph')
parser.add_argument('--algorithm',default='a',\
    help='Algorithm: Select the algorithm to run, default is all. (a)ll, (b)ellman-ford only or (f)loyd-warshall only')
parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('--profile',action='store_true')
parser.add_argument('filename',metavar='<filename>',help='Input file containing graph')

graphRE=re.compile("(\\d+)\\s(\\d+)")
edgeRE=re.compile("(\\d+)\\s(\\d+)\\s(-?\\d+)")

vertices=[]
edges=[]

def BellmanFord(G):
    # The pathPairs list will contain the 2D array of shortest paths between all pairs of vertices 
    # [[w(1,1),w(1,2),...]
    #  [w(2,1),w(2,2),...]
    #  [w(3,1),w(3,2),...]
    #   ...]
    pathPairs = []
    tmpPathPairs = []
    numNodes = len(G[0])
    nodeEdges = []
    nodeIterator = []

    for z in range(numNodes):
        startNode = G[0][z]
        #set up a list to iterate over all nodes with a specific starting point that isn't always 0
        del nodeIterator[:]
        for i in G[0][startNode:]:
            nodeIterator.append(i)
        if startNode != 0:
            for i in G[0][:startNode]:
                nodeIterator.append(i)
    
        #Initialize tmpPathPairs to infinity
        del tmpPathPairs[:]
        for i in range(numNodes):
            tmpPathPairs.append(float("inf"))

        #Set distance for node being analyzed to zero since the distance from 
        #a node to itself is 0
        tmpPathPairs[startNode] = 0

        for i in range(numNodes): #iterate numNodes - 1 times
            for j in nodeIterator: #once per node

                #Current node must have a value already otherwise go to next node
                if tmpPathPairs[j] != float("inf"):
                    #Get location of edges and save in nodeEdges[]
                    del nodeEdges[:]
                    for k in range(numNodes):
                        if G[1][j][k] != float("inf"):
                            nodeEdges.append(k)


                    #for every edge a node has, visit it and update its distance from the start node
                    #print("For node " + str(j + 1) + " we are using edges ")
                    for edge in nodeEdges:
                        #print(str(edge + 1))
                        #if current node value + weight to sink < value of sink
                        if (tmpPathPairs[j] + float(G[1][j][edge])) < float(tmpPathPairs[edge]):
                            tmpPathPairs[edge] = int(tmpPathPairs[j] + float(G[1][j][edge]))
            if i == numNodes - 1:
                pathPairs.append(tmpPathPairs[:])
            #end for
        #end for

    #end for loop

    return pathPairs

def FloydWarshall(G):
    # TODO: Fill in your Floyd-Warshall algorithm here
    # The pathPairs list will contain the 2D array of shortest paths between all pairs of vertices 
    # [[w(1,1),w(1,2),...]
    #  [w(2,1),w(2,2),...]
    #  [w(3,1),w(3,2),...]
    #   ...]
    pathPairs=[]
    nodeEdges = []
    
    #get number of nodes
    numNodes = len(vertices)
    numEdges = len(edges)

    #initialize 2D array to "inf"
    for i in range(numNodes):
        pathPairs.append([float("inf")] * numNodes)

    #set distance to 0 for each node that travels to itself
    for i in range(numNodes):
        pathPairs[i][i] = 0

    for i in range(numNodes):
        for j in range(numNodes):
            if float(G[1][i][j]) != float("inf"):
                pathPairs[i][j] = G[1][i][j]

    for i in range(numNodes):
        for j in range(numNodes):
            for k in range(numNodes):
                if (pathPairs[j][k] != float("inf")) and (pathPairs[j][i] != float("inf")) and (pathPairs[i][k] != float("inf")):
                    if int(pathPairs[j][k]) > int(pathPairs[j][i]) + int(pathPairs[i][k]):
                        pathPairs[j][k] = int(int(pathPairs[j][i]) + int(pathPairs[i][k])) 
                elif (pathPairs[j][k] == float("inf")) and (pathPairs[j][i] != float("inf")) and (pathPairs[i][k] != float("inf")):
                        pathPairs[j][k] = int(pathPairs[j][i]) + int(pathPairs[i][k]) 


    return pathPairs

def readFile(filename):
    global vertices
    global edges
    # File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>
    # ...
    inFile=open(filename,'r')
    line1=inFile.readline()
    graphMatch=graphRE.match(line1)
    if not graphMatch:
        print(line1+" not properly formatted")
        quit(1)
    vertices=list(range(int(graphMatch.group(1))))
    edges=[]
    for i in range(len(vertices)):
        row=[]
        for j in range(len(vertices)):
            row.append(float("inf"))
        edges.append(row)
    for line in inFile.readlines():
        line = line.strip()
        edgeMatch=edgeRE.match(line)
        if edgeMatch:
            source=edgeMatch.group(1)
            sink=edgeMatch.group(2)
            if int(source) > len(vertices) or int(sink) > len(vertices):
                print("Attempting to insert an edge between "+source+" and "+sink+" in a graph with "+vertices+" vertices")
                quit(1)
            weight=edgeMatch.group(3)
            edges[int(source)-1][int(sink)-1]=weight
    G = (vertices,edges)
    return (vertices,edges)

def matrixEquality(a,b):
    if len(a) == 0 or len(b) == 0 or len(a) != len(b): return False
    if len(a[0]) != len(b[0]): return False
    for i,row in enumerate(a):
        for j,value in enumerate(b):
            if a[i][j] != b[i][j]:
                return False
    return True


def main(filename,algorithm):
    G=readFile(filename)
    pathPairs = []
    # G is a tuple containing a list of the vertices, and a list of the edges
    # in the format ((source,sink),weight)
    if algorithm == 'b' or algorithm == 'B':
        # TODO: Insert timing code here
        t0 = time.time()
        pathPairs = BellmanFord(G)
        t1 = time.time()
        print("Time elapased BellmanFord is: " + str(t1 - t0))
        print("Result: ")

    if algorithm == 'f' or algorithm == 'F':
        # TODO: Insert timing code here
        t0 = time.time()
        pathPairs = FloydWarshall(G)
        t1 = time.time()
        print("Time elapased FloydWarshall is: " + str(t1 - t0))
        print("Result: ")

    if algorithm == 'a':
        print('running both') 
        t0 = time.time()
        pathPairsBellman = BellmanFord(G)
        t1 = time.time()
        print("BellmanFord: " + str(t1 - t0))
        t0 = time.time()
        pathPairsFloyd = FloydWarshall(G)
        t1 = time.time()
        print("FloydWarshal: " + str(t1 - t0))
        pathPairs = pathPairsBellman
        if matrixEquality(pathPairsBellman,pathPairsFloyd):
            print('Floyd-Warshall and Bellman-Ford did not produce the same result')
    with open(os.path.splitext(filename)[0]+'_shortestPaths.txt','w') as f:
        for row in pathPairs:
            for weight in row:
                f.write(str(weight)+' ')
            f.write('\n')

if __name__ == '__main__':
    args=parser.parse_args()
    main(args.filename,args.algorithm)

