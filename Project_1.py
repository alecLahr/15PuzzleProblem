# Alec Lahr - ENPM661 Project 1 - 15 Puzzle Problem

import numpy as np


# ===================== CONVERSION FUNCTIONS ========================
def matToStr(mat):
    # takes in a numpy matrix state and returns the string representation
    tenList = list(mat.flatten())  # converts matrix to a list of strings
    hexString = ''  # create empty string
    for elem in tenList:  # add each element's hex conversion to the string
        hexString += hex(elem)[2]
    return hexString
    

def strToMat(strg):
    # takes in a state string and returns the state numpy matrix
    tempArray = np.array([])  # make empty array
    for char in strg:  # add the decimal version of each string element to the array, convert to type int
        tempArray = np.append(tempArray, int(char, 16)).astype(int)
    return np.reshape(tempArray, (4, 4))  # convert the array to a 4x4 matrix then return it


# ======================= SEARCH FUNCTIONS ==========================
def findZero(mat):
    # searches the state matrix for the empty space (0)
    (j, i) = np.argwhere(mat == 0)[0]
    return (i, j)  # return the i, j coordinate of 0


def checkIfDuplicate(strg):
    # checks if the input matrix is already in nodes, returns bool
    for state in nodes:  # cycle through all of nodes list
        if state[1] == strg:  # compare input to state i
            return True  # return true if match, exit for loop and function
    return False  # returns false if nothing found in for loop


def getPossibleMoves(i, j, prevMove):
    # checks which moves are possible
    # returns a list of 4 bools indicating if that direction is okay to move in
    # [Up, Down, Left, Right]
    directions = [False, False, False, False]
    if i > 0 and prevMove != 'R':
        directions[2] = True
    if i < 3 and prevMove != 'L':
        directions[3] = True
    if j > 0 and prevMove != 'D':
        directions[0] = True
    if j < 3 and prevMove != 'U':
        directions[1] = True
    return directions


# ======================= ACTION FUNCTIONS ==========================
def actionMoveLeft(mat, i, j):
    # moves the 0 tile left one
    dummyTile = mat[j][i-1]  # store the state of the tile to the left of 0
    mat[j][i-1] = 0  # overwrite the left tile
    mat[j][i] = dummyTile  # replace the 0 with the dummy tile
    return mat


def actionMoveRight(mat, i, j):
    # moves the 0 tile right one
    dummyTile = mat[j][i+1]  # store the state of the tile to the right of 0
    mat[j][i+1] = 0  # overwrite the right tile
    mat[j][i] = dummyTile  # replace the 0 with the dummy tile
    return mat


def actionMoveUp(mat, i, j):
    # moves the 0 tile up one
    dummyTile = mat[j-1][i]  # store the state of the tile to the up of 0
    mat[j-1][i] = 0  # overwrite the up tile
    mat[j][i] = dummyTile  # replace the 0 with the dummy tile
    return mat


def actionMoveDown(mat, i, j):
    # moves the 0 tile up one
    dummyTile = mat[j+1][i]  # store the state of the tile to the up of 0
    mat[j+1][i] = 0  # overwrite the up tile
    mat[j][i] = dummyTile  # replace the 0 with the dummy tile
    return mat


# ============================== MAIN =================================
# define initial state
initialState = np.array([[1, 6, 2, 3], [9,5, 7, 4], [0, 10, 11, 8] , [13, 14, 15, 12]])
testCase = 5  # test case number changes output .txt file name

# define goal state
goalState = np.array([[1, 2, 3, 4],
                      [5, 6, 7, 8],
                      [9, 10, 11, 12],
                      [13, 14, 15, 0]])
goalString = matToStr(goalState)  # get the string version of the goal matrix

# create empty nodes array
nodes = [] # each element of the nodes array takes the form: [index of parent, current state string, prev move]
# prev move element takes the form: 'U', 'D', 'L', 'R'

# add the initial state to the nodes array
nodes.append(['Start', matToStr(initialState), 'N/A'])
# first element is the only one to get a str type parent index and 0 prev move elem

# remember the index of the first and last state in nodes for the previous layer
# so that you know where to start iterating for the next layer
# Example:
#            0
#      1           2
#   3     4     5     6
#  7 8   9 10 11 12 13 14
# by this point, 7 and 14 would be remembered so that the loop knows to start the next layer from 7 to 14
layerStartIndex = 0
layerEndIndex = 0

failedMessage = ''

# keep looping until goalState is found
goalFound = False
layer = 0
while not goalFound:
    # loop through each state from the previous layer
    layer += 1
    # print('Layer', layer)
    for n in range(layerStartIndex, layerEndIndex + 1):
        currentString = nodes[n][1]  # get the current state string
        currentMat = strToMat(currentString)  # convert string state to matrix state
        i, j = findZero(currentMat)  # get the location of the 0, store it in i, j
        dirs = getPossibleMoves(i, j, nodes[n][2])  # [Up, Down, Left, Right] with bool
        
        if dirs[0]:  # if possible, move up
            childState = actionMoveUp(np.copy(currentMat), i, j)  # move up and store new state
            childString = matToStr(childState)  # get string version of child state
            dup = checkIfDuplicate(childString)  # check if the new state is a duplicate state
            if dup == False:
                nodes.append([n, childString, 'U'])  # add new state and its parent to nodes list
            if np.array_equal(childString, goalString):  # check if the child reached the goal
                goalFound = True  # exit the for loop and stop while loop
                break
            
        if dirs[1]:  # if possible, move down
            childState = actionMoveDown(np.copy(currentMat), i, j)  # move down and store new state
            childString = matToStr(childState)  # get string version of child state
            dup = checkIfDuplicate(childString)  # check if the new state is a duplicate state
            if dup == False:
                nodes.append([n, childString, 'D'])  # add new state and its parent to nodes list
            if np.array_equal(childString, goalString):  # check if the child reached the goal
                goalFound = True  # exit the for loop and stop while loop
                break
            
        if dirs[2]:  # if possible, move left
            childState = actionMoveLeft(np.copy(currentMat), i, j)  # move left and store new state
            childString = matToStr(childState)  # get string version of child state
            dup = checkIfDuplicate(childString)  # check if the new state is a duplicate state
            if dup == False:
                nodes.append([n, childString, 'L'])  # add new state and its parent to nodes list
            if np.array_equal(childString, goalString):  # check if the child reached the goal
                goalFound = True  # exit the for loop and stop while loop
                break
            
        if dirs[3]:  # if possible, move right
            childState = actionMoveRight(np.copy(currentMat), i, j)  # move right and store new state
            childString = matToStr(childState)  # get string version of child state
            dup = checkIfDuplicate(childString)  # check if the new state is a duplicate state
            if dup == False:
                nodes.append([n, childString, 'R'])  # add new state and its parent to nodes list
            if np.array_equal(childString, goalString):  # check if the child reached the goal
                goalFound = True  # exit the for loop and stop while loop
                break
            
        # update the start and end indexes for use in the next layer
        layerStartIndex = layerEndIndex
        if n == layerEndIndex:
            layerEndIndex = len(nodes)-1
            
        # stop the program after 1,000,000 nodes searched
        if len(nodes) > 1000000:
            goalFound = True
            print("Search Failed")
            failedMessage = "Search Failed - Terminated after 1000000 nodes"
            break
    if len(nodes) > 1000000:
        break
            
# exited while loop
    
indexes = [len(nodes) - 1]  # create array to hold indexes. start with last elem in nodes
moves = []  # create array to hold moves toward solution

# get indices and moves list of parents of solution
while nodes[indexes[-1]][0] != 'Start':  # go until you get back to start
    moves.append(nodes[indexes[-1]][2])    
    indexes.append(nodes[indexes[-1]][0])

# reverse order of indexes and moves: now it goes from initial to goal
indexes.reverse()
moves.reverse()

# write solution to text file titled with initial state
f = open("nodePath_TestCase" + str(testCase),"w+")  # create .txt file
for n, i in enumerate(indexes):  # loop through list of solution indexes
    strg = np.array2string(strToMat(nodes[i][1]))  # get the matrix state at a position and convert to string
    direction = nodes[i][2]  # get the direction the piece moved
    # add the info to the .txt file
    f.write('Node Index: ' + str(i) + '\nMove Direction: ' + direction + '\n'+ strg + '\r\n\n')
f.write(failedMessage + '\r')  # adds a failed message if search failed
print('New file created: nodePath_TestCase' + str(testCase) + '.txt')
f.close() 








