import argparse
import os
import sys
import time
import profile
from math import sqrt
import time

# Command line arguments
parser=argparse.ArgumentParser(description='Calculate the nearest two points on a plan')
parser.add_argument('--algorithm',default='a',\
    help='Algorithm: Select the algorithm to run, default is all. (a)ll, (b)ruteforce only or (d)ivide and conquer only')
parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('--profile',action='store_true')
parser.add_argument('filename',metavar='<filename>',\
    help='Input dataset of points')




#=================================================================================================
def bruteForce(points):
    minimum_distance = 0;
    distance = 0;
    point1 = (-1,-1)
    point2 = (-1,-1)
    for num in range(0, len(points)):
        for nestedNum in range(num + 1, len(points)):
            tmp_point1 = (points[num][0], points[num][1])
            tmp_point2 = (points[nestedNum][0], points[nestedNum][1])

            distance = sqrt(((tmp_point1[0] - tmp_point2[0])**2) + ((tmp_point1[1] - tmp_point2[1])**2))
            if num == 0 and nestedNum == 1: # this means that it is the first distance calculated
                minimum_distance = distance
            else:
                if distance < minimum_distance:
                    minimum_distance = distance
                    point1 = (tmp_point1[0], tmp_point1[1])
                    point2 = (tmp_point2[0], tmp_point2[1])
    return (minimum_distance,point1,point2)
#end def brute_force_nearest_neighbor(points):
#================================================================================================

#Divide and conquer version of the nearest neighbor algorithm
#Input: points := unsorted array of (x,y) coordinates
#Output: tuple of smallest distance and coordinates (distance,(x1,y1),(x2,y2))
def divideAndConquerNearestNeighbor(points):
    #minimum_distance = 0;
    #point1 = (-1,-1)
    #point2 = (-1,-1)
    #TODO: Complete this function

    points.sort() #sorts by x-coordinate
    if len(points) <= 3:
        return bruteForce(points)
    middle = int(len(points)/2)
    midpoint = points[middle][0]

    L = points[:middle]
    R = points[middle:]

    minimum_distanceL = divideAndConquerNearestNeighbor(L)
    minimum_distanceR = divideAndConquerNearestNeighbor(R)

    if minimum_distanceL[0] <= minimum_distanceR[0]:
        minimum_distance = minimum_distanceL
        #print("The my min dist is: " + str(minimum_distanceL[0]))
        #return minimum_distanceL
    else:
        minimum_distance = minimum_distanceR
        #print("The my min dist is: " + str(minimum_distanceR[0]))
        #return minimum_distanceR

    for point in points:
        if point[0] < midpoint - minimum_distance[0] or point[0] > midpoint + minimum_distance[0]:
            del(point)
    borderMinDist = bruteForce(points)
    
    #print("Divide and Conquer algorithm is incomplete")
    if minimum_distance[0] <= borderMinDist[0]:
        #print("The following is the minimum distance: " + str(minimum_distance[0]))
        return minimum_distance
    else:   
        #print("The following is the minimum distance: " + str(borderMinDist[0]))
        return borderMinDist
#end def divide_and_conquer(points):
#=================================================================================================




#=================================================================================================
#Brute force version of the nearest neighbor algorithm
#Input: points := unsorted array of (x,y) coordinates 
#   [(x,y),(x,y),...,(x,y)]
#Output: tuple of smallest distance and coordinates (distance,(x1,y1),(x2,y2))
def bruteForceNearestNeighbor(points):
    minimum_distance = 0;
    distance = 0;
    point1 = (-1,-1)
    point2 = (-1,-1)
    #TODO: Complete this function

    for num in range(0, len(points)):
        for nestedNum in range(num + 1, len(points)):
            #code used to keep track of progress (made algorithm take significantly longer)
            #sys.stdout.write('\033[F')
            #sys.stdout.write('\033[K') 
            #print(str(int(num/len(points) * 100)) + "%")            

            #find distance between point at index num and nestedNum
            #first set up points to perform distance calculation
            tmp_point1 = (points[num][0], points[num][1])
            tmp_point2 = (points[nestedNum][0], points[nestedNum][1])

            distance = sqrt(((tmp_point1[0] - tmp_point2[0])**2) + ((tmp_point1[1] - tmp_point2[1])**2))
            
            if num == 0 and nestedNum == 1: # this means that it is the first distance calculated
                minimum_distance = distance
            else:
                if distance < minimum_distance:
                    minimum_distance = distance
                    point1 = (tmp_point1[0], tmp_point1[1])
                    point2 = (tmp_point2[0], tmp_point2[1])
                    #print("The new min distance is " + str(minimum_distance))
                    #print("Using points " + str(point1) + " and " + str(point2))
                #end if
            #end if-else
        #end nested for
    #end for
            #print(point1)
            #print(nestedNum, end = " ")
        #print("\n")
    #print("The following is the minimum distance: " + str(minimum_distance))

    print("Brute force algorithm is incomplete")
    return (minimum_distance,point1,point2)
#end def brute_force_nearest_neighbor(points):
#================================================================================================




#Parse the input file
#Input: filename := string of the name of the test case
#Output: points := unsorted array of (x,y) coordinates
#   [(x,y),(x,y),...,(x,y)]
def parseFile(filename):
    points = []
    f = open(filename,'r') 
    lines = f.readlines()
    for line in lines:
        coordinate = line.split(' ')
        points.append((float(coordinate[0]),float(coordinate[1])))
    return points
#end def parse_file(filename):

#Main
#Input: filename  := string of the name of the test case
#       algorithm := flag for the algorithm to run, 'a': all 'b': brute force, 'd': d and c
def main(filename,algorithm):
    points = parseFile(filename)
    result = bruteForceResult = divideAndConquerResult = None
    if algorithm == 'a' or algorithm == 'b':
        #TODO: Insert timing code here
        t0 = time.time()
        bruteForceResult = bruteForceNearestNeighbor(points)
        t1 = time.time()

        print("Time elapsed(brute force): " + str(t1-t0))        

    if algorithm == 'a' or algorithm == 'd':
        #TODO: Insert timing code here
        
        t0 = time.time()
        divideAndConquerResult = divideAndConquerNearestNeighbor(points)
        t1 = time.time()
        print("Time elapsed(divide and conquer): " + str(t1-t0))
        #print("The following is the minimum distance: " + str(divideAndConquerResult[0]))
     
    if algorithm == 'a': # Print whether the results are equal (check)
        #if args.verbose:
        print('Brute force result: '+str(bruteForceResult))
        print('Divide and conquer result: '+str(divideAndConquerResult))
        print('Algorithms produce the same result? '+str(bruteForceResult == divideAndConquerResult))
        result = bruteForceResult if bruteForceResult == divideAndConquerResult else ('Error','N/A','N/A')
    else:  
        result = bruteForceResult if bruteForceResult is not None else divideAndConquerResult
    with open(os.path.splitext(filename)[0]+'_distance.txt','w') as f:
        f.write(str(result[1])+'\n')
        f.write(str(result[2])+'\n')
        f.write(str(result[0])+'\n')
#end def main(filename,algorithm):

if __name__ == '__main__':
    args=parser.parse_args()
    main(args.filename,args.algorithm)
#end if __name__ == '__main__':

