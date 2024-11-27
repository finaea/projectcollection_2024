import heapq

class Node:
    ## node with state, parent, cost, heuristic
    def __init__(self, state, parent = None, cost = 0, heuristic = 0):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
    ## compare with lesser than between node 
    def __lt__(self, compare):
        return (self.cost + self.heuristic) < (compare.cost + compare.heuristic)

## function to get neighbor
def getNeighbor(current):
    neighbors = []
    x, y = current
    ## for coord with even row
    if y % 2 == 0:
        possibleMove = [(x , y -1), 
                        (x -1, y ),
                        (x , y +1),
                        (x +1, y +1),
                        (x +1, y),
                        (x +1, y -1)]
    ## for coord with odd row
    else:
        possibleMove = [(x -1, y -1), 
                        (x -1, y),
                        (x -1, y +1),
                        (x, y +1),
                        (x +1, y),
                        (x, y -1)]
    ## filter coord not in the rooms
    for neighbor in possibleMove:
        if neighbor in rooms:
            neighbors.append(neighbor)

    return neighbors

## test neighbor
# print("get neighbor list: ")
# print(getNeighbor((6,1)))

## function to convert offset coordinate to cube coordinate
def toCube(current):
    x, y = current
    q = y
    r = x - (y + (y&1)) /2
    return (q, r, -q-r)

## function to calculate heuristic distance between current and goal 
def getHeuristic(current, goal):
    cq, cr, cs = toCube(current)
    gq, gr, gs = toCube(goal)
    distance = max(abs(cq - gq), abs(cr - gr), abs(cs - gs))
    return (int(distance))

## test heuristic
# print(heuristic distance: )
# print(heuristic((0,0),(6,4)))


## locate the nearest rubbish room and arrange the scheduled room in order with heuristic distance
def nearestAndArrange(roomOrder, initialState):
    ## find the nearest room from current room with least heuristic distance
    least = 999
    for i in range(len(roomOrder)):
        for j in range(len(roomOrder[i])):
            temp = getHeuristic(initialState, roomOrder[i][j])
            if temp < least:
                least = temp
                nearest = roomOrder[i][j]
                coord = i, j
                
    ## put the nearest room to the first in the list
    roomOrder[coord[0]].insert(0, roomOrder[coord[0]].pop(coord[1]))
    
    ## find the nearest room from found room with least heuristic distance
    least = 999
    for i in range(1, len(roomOrder[coord[0]])):
        temp = getHeuristic(nearest, roomOrder[coord[0]][i])
        if temp < least:
            least = temp
            ## put the nearest room after the found room in the list
            roomOrder[coord[0]].insert(1, roomOrder[coord[0]].pop(i))
    ## put the nearest room in list to the first in schedule
    roomOrder.insert(0, roomOrder.pop(coord[0]))
    
    return roomOrder

## arrange the room in desending order based on volumetric weight
def sortRubbishRoom(rubbishRoom):
    roomSort = []
    volumeWeight = []
    
    ## w = weight, v = volume
    for x in rubbishRoom:
        w, v = rubbishRoom[x]
        vw = w * v
        ## when list is empty
        if roomSort == []:
            roomSort.append(x)
            volumeWeight.append(vw)
        ## sort in desending order
        else:
            insert_index = len(volumeWeight)
            for i, j in enumerate(volumeWeight):
                if vw > j:
                    insert_index = i
                    break
            volumeWeight.insert(insert_index, vw)
            roomSort.insert(insert_index, x)
    return roomSort
    ## check sorting result
    # print("Volume weight of the rubbish in room:")  
    # print(volumeWeight)
    # print("Sorted rubbish room decreasing order: ")
    # print(roomSort)

## best-fit desending bin packing
def binPacking(rubbishRoom):
    ## list of room schedule and it's capacity
    roomSort = sortRubbishRoom(rubbishRoom)
    roomOrder =[]
    binCapacity = []
    for x in roomSort:
        ## when roomOrder is empty
        if roomOrder == []:
            newBin = []
            newBin.append(x)
            roomOrder.append(newBin)
            w, v = rubbishRoom[x]
            binCapacity.append([w, v])
        ## iterate the list to fit rubbish
        else:
            fit = False
            for i in range(len(binCapacity)):
                totalW, totalV = binCapacity[i]
                w, v = rubbishRoom[x]
                ## if fit, put in the bin; update the binList and capacity
                if ((totalW + w) <= weightLimit) and ((totalV + v) <= volumeLimit):
                    temp = roomOrder[i]
                    temp.append(x)
                    roomOrder[i] = temp
                    binCapacity[i] = [totalW + w, totalV + v]
                    fit = True
                    break
            ## if not fit, create new bin; update the binList and capacity
            if fit == False:
                newBin = []
                newBin.append(x)
                roomOrder.append(newBin)
                w, v = rubbishRoom[x]
                binCapacity.append([w, v])
    return roomOrder
    ## check room chedule order
    # print("Rubbish room schedule order: ")
    # print(roomOrder)
    # print("Capacity of bin: ")
    # print(binCapacity)

## A * search algorithm
def aStarSearch(initialState, goalState, rooms, currentRubbishState):
    frontier  = []
    ## items in set are unique, therefore no duplicate if add
    explored = set()
    
    ## put initialState as startNode into heapq prioritize heuristic
    startNode = Node(initialState)
    startNode.heuristic = getHeuristic(initialState, goalState)
    heapq.heappush(frontier, (startNode.heuristic + startNode.cost, startNode))

    while frontier:
        currentNode = heapq.heappop(frontier)[1]
        ## if currentNode is goalState, append and return path list
        if currentNode.state == goalState:
            path = []
            while currentNode:
                path.append(currentNode.state)
                currentNode = currentNode.parent
            path.reverse()
            return path
        
        ## add currentNode to explored list
        explored.add(currentNode.state)
        
        ## get the neighbor from current node
        neighbors = getNeighbor(currentNode.state)
        
        ## iterate neighbor in the neighbors list
        for neighbor in neighbors:
            ## avoid other room with rubbish if not goal
            if neighbor in currentRubbishState and neighbor != goalState:
                continue
            ## ignore neighbor if in explored list
            elif neighbor in explored:
                continue
            ## ignore neighbor if it is an obstacle
            elif neighbor in obstacleRoom:
                continue
            ## each move increase cost by 1
            neighborCost = currentNode.cost + 1
            ## initialize neighbor node
            neighborNode = None
            ## set as neighbor node if in frontier
            for node in frontier:
                if node[1].state == neighbor:
                    neighborNode = node[1]
                    ## update the neighbor cost and parent if lesser than previous cost
                    if neighborCost < neighborNode.cost:
                        neighborNode.cost = neighborCost
                        neighborNode.parent = currentNode
                        ## replace with updated node in frontier
                        frontier = [(node[0],neighborNode) if x == node else x for x in frontier]
                        heapq.heapify(frontier)
                    break
            ## if new neighbor node set parent, cost and heuristic then put into frontier with heappush
            if neighborNode == None:
                neighborNode = Node(neighbor,
                                    parent = currentNode,
                                    cost = neighborCost,
                                    heuristic = getHeuristic(neighbor, goalState))
                heapq.heappush(frontier, (neighborNode.heuristic + neighborNode.cost, neighborNode))
    ## return None if no goal found
    return None

## function for printing the path with delimiter " -> " and checking for any disposal rooms unintentionally encountered in the path
def printPath(path):
    disposalEncounter = []
    for i in range(len(path) - 1):
        print(path[i], end="")
        if i != 0 and path[i] in currentDisposalState:
            print("(Disposal in Path)", end="")
            disposalEncounter.append(path[i])
        print(" -> ", end="")
        if (i + 1 == len(path) - 1):
            print(path[i + 1])
            return disposalEncounter

##go to next input based on the separator "####################"
def gotoseperation(line):
    while(True):
        if sfile[line] == "//////////\\\\\\\\\\\\\\\\\\\\":
            return line + 1
        line += 1
        

        
#########################################Program Starts Here#################################################

import subprocess
import time
from ast import literal_eval
print("Program is starting.....")
print("Opening input.txt.........")

##the program will open input.txt for the user to edit any inputs
try:
    returned = subprocess.run(["input.txt"], shell=True, capture_output=True, text=True)
    print("The file has successfully saved.")
##if there is an error, it should alert the user
except:
    print("Error! input.txt failed to open!")
    print("The program will proceed to start without making any changes to the inputs.")
    print("If you would like to make changes to the input, you may modify the input.txt using a text editor after the program is ended.")

##give the user some time to read before starting the search
for i in range(5, -1, -1):
    print("\rThe search program will start in...... %d" % i, end="")
    time.sleep(1)
print("\n")

##start measuring the time by marking the start time as the program has started
start_time = time.time()

##read the input.txt file
file = open("input.txt", "r")
##split the file into a list to remove the newlines
sfile = file.read().splitlines()
file.close()
##starting from line 0th
line = 0

try:
    ## create list of rooms with offset coordinate
    line = gotoseperation(line)
    size = literal_eval(sfile[line])
    line += 2
    rooms = []
    for i in range(size[0]):
        for j in range(size[1]):
            coord = i, j
            rooms.append(coord)

    ## check rooms
    # print("room list: ")
    # print(rooms)

    ##initialize a List for duplicate checking later
    checkUniqueList = []

    ## initialize rubbish room locations with type dictionary with weight and volume
    ## room coord : (weight, volume)
    line = gotoseperation(line)
    rubbishRoom = {}
    while (True):
        if sfile[line] == "\\\\\\\\\\\\\\\\\\\\//////////":
            line += 1
            break
        splittedLine = sfile[line].split()
        rubbishRoom[literal_eval(splittedLine[0])] = literal_eval(splittedLine[2])
        checkUniqueList.append(literal_eval(splittedLine[0]))
        line += 1

    ## current rubbish room state
    currentRubbishState = rubbishRoom.copy()

    ## initialize disposal room locations
    line = gotoseperation(line)
    disposalRoom = []
    while (True):
        if sfile[line] == "\\\\\\\\\\\\\\\\\\\\//////////":
            line += 1
            break
        disposalRoom.append(literal_eval(sfile[line]))
        line += 1
    ## current disposal room state
    currentDisposalState = disposalRoom.copy()
        
    ## initialize obstacle room locations
    line = gotoseperation(line)
    obstacleRoom = []
    while (True):
        if sfile[line] == "\\\\\\\\\\\\\\\\\\\\//////////":
            line += 1
            break
        obstacleRoom.append(literal_eval(sfile[line]))
        line += 1

    ## start point of the hexa maze
    line = gotoseperation(line)
    initialState = literal_eval(sfile[line])
    line += 2

    ## Ronny and bin capacity
    line = gotoseperation(line)
    weightLimit = int(sfile[line])
    volumeLimit = int(sfile[line + 1])

except Exception as error:
    print("\nAn error occurred:", error)
    print("\nUnable to read the input.txt correctly")
    print("Please ensure that you follow the instructions and format correctly in readme.txt")
    exit()

## initialize bin weight, bin volume, distance travel and disposal room usage
binW = 0
binV= 0 
totaDistance = 0
disposalUsage = 0

## bin packing and schedule room to visit for Ronny  
roomOrder = binPacking(rubbishRoom)
roomArr = nearestAndArrange(roomOrder, initialState)

## maze clearing status
proceed = True
roomStop = ()
overallPath = [initialState] 

##check for any duplication of the rooms with the same row and column
checkUniqueList.extend(currentDisposalState)
checkUniqueList.extend(obstacleRoom)
checkUniqueList.append(initialState)
if len(checkUniqueList) != len(set(checkUniqueList)):
    print("Error! There is a duplication in the inputs!")
    print("Make sure each input is an unique room.")
    proceed = False

## maze clearing process in scheduled order
## proceed if only there is room in scheduled list and proceed is true
while roomArr and proceed:
    ## break process if fail
    if proceed:
        ## clear list of rubbish rooms in schedule
        cleanRoom = roomArr.pop(0)
        for roomToClean in cleanRoom:
            path = aStarSearch(initialState, roomToClean, rooms, currentRubbishState)
            ## return fail message if unable to find rubbish rooom
            if path == None:
                print("Warning!!! Unable to find rubbish room at "+ str(roomToClean))
                print("The program will proceed onto the next room instead.")
                print("")
                continue
            ##save the path to the overall
            for x in range(1, len(path)):
                overallPath.append(path[x])
            totaDistance += len(path) -1
            # check any rubbish pickup along the path or any disposal room unintentionally encountered
            for i in range(len(path)):
                if path[i] in currentRubbishState:
                    rubbish = currentRubbishState.pop(path[i])
                    binW += rubbish[0]
                    binV += rubbish[1]
                    ## return fail message if Ronny or bin exceed maximum capacity
                    if binW > weightLimit or binV > volumeLimit:
                        roomStop = path[i]
                        proceed = False
                        break
                ## clear weight/volume of bin due to unintentional encounter of disposal path during travelling, also increase disposalUsage
                if i > 0 and i < len(path) - 1 and path[i] in currentDisposalState:
                    binW = 0
                    binV = 0
                    disposalUsage += 1
            ## display status process of Ronny
            if proceed:
                print("Path travelled: ")
                disposalEncounter = printPath(path)
                print("Action: ")
                print("Pick up rubbish at room " + str(roomToClean))
                print("Bin status: ")
                print("Weight "  + str(binW) + "kg, Volume " + str(binV) + "m^3")
                print("Total travelled distance: " + str(totaDistance))
                if (disposalEncounter != []):
                    print("Total number of disposal room usage increased due to unintentional encounter of disposal room at:")
                    print(disposalEncounter)
                print("Total number of disposal room usage: " + str(disposalUsage))
                print()
                ## set current goal as start point 
                initialState = roomToClean
            else:
                print("Path travelled: ")
                printPath(path[:path.index(roomStop)+1])
                if binW > weightLimit:
                    print("Failed...Ronny unable to move the bin")
                elif binV > volumeLimit:
                    print("Failed...Bin reached maximum capacity and unable to move")
                print("Action: ")
                print("Stop at room " + str(roomStop))
                print("Bin status: ")
                print("Weight "  + str(binW) + "kg, Volume " + str(binV) + "m^3")
    
    ## break process if fail
    if proceed:
        ##this loop is created specifically to ensure there is an available disposal room that is not blocked
        while (True):
            ## when rubbish rooms were cleared in schedule
            ## locate the nearest disposal room from current room to clear rubbish
            roomDistance = []
            for room in currentDisposalState:
                roomDistance.append(getHeuristic(initialState, room))
            nearestDisposal = currentDisposalState[roomDistance.index(min(roomDistance))]
            path = aStarSearch(initialState, nearestDisposal, rooms, currentRubbishState)
            ## return fail message if unable to find disposal room
            if path == None:
                print("Warning!!! Unable to find disposal room at "+ str(roomToClean))
                print("The program will proceed to find another nearest disposal room instead.")
                print("")
                ##remove this unavailable disposal room from the list so that it is ignored
                currentDisposalState.pop(roomDistance.index(min(roomDistance)))
                if currentDisposalState == []:
                    proceed = False
                    break
                continue
            for x in range(1, len(path)):
                overallPath.append(path[x])
            totaDistance += len(path) -1
            # check any rubbish pickup along the path or any disposal room unintentionally encountered
            for i in range(len(path)):
                if path[i] in currentRubbishState:
                    rubbish = currentRubbishState.pop(path[i])
                    binW += rubbish[0]
                    binV += rubbish[1]
                    ## return fail message if Ronny or bin exceed maximum capacity
                    if binW > weightLimit or binV > volumeLimit:
                        roomStop = path[i]
                        proceed = False
                        break
                ## clear weight/volume of bin due to unintentional encounter of disposal path during travelling, also increase disposalUsage
                if i > 0 and i < len(path) - 1 and path[i] in currentDisposalState:
                    binW = 0
                    binV = 0
                    disposalUsage += 1
            ## reset bin weight and volume capacity
            binW = 0
            binV = 0 
            ## record disposal room usage
            disposalUsage += 1
            ## display status process of Ronny
            if proceed:
                print("Path travelled: ")
                disposalEncounter = printPath(path)
                print("Action: ")
                print("Clear all rubbish in bin at disposal room " + str(nearestDisposal))
                print("Bin status: ")
                print("Weight "  + str(binW) + "kg, Volume " + str(binV) + "m^3")
                print("Total travelled distance: " + str(totaDistance))
                if (disposalEncounter != []):
                    print("Total number of disposal room usage increased due to unintentional encounter of disposal room at:")
                    print(disposalEncounter)
                print("Number of disposal room usage: " + str(disposalUsage))
                print()
                ## set current goal as start point 
                initialState = nearestDisposal
                ## arrange next schedule with current room based on heuristic
                if roomArr != []:
                    roomArr = nearestAndArrange(roomArr, initialState)
                break
            else:
                print("Path travelled: ")
                printPath(path[:path.index(roomStop)+1])
                if binW > weightLimit:
                    print("Failed...Ronny unable to move the bin")
                elif binV > volumeLimit:
                    print("Failed...Bin reached maximum capacity and unable to move")
                print("Action: ")
                print("Stop at room " + str(roomStop))
                print("Bin status: ")
                print("Weight "  + str(binW) + "kg, Volume " + str(binV) + "m^3")
                break
        ##exit if the available disposal rooms are empty
        if currentDisposalState == []:
            print("Program halted... There is no available disposal room for use!")
            break
            

if proceed == True:
    print("Search Algorithm completed successfully!\n")

    print("------------------------The Maze--------------------------\n")
    
    ## turn rooms into list of rows of list of column
    roomsView = []
    odd = 1
    even = 0
    for i in range(0,len(rooms),size[1]):
        temp = []
        for j in range(i, i + size[1]):
            if j % 2 == odd:
                temp.append(rooms[j])
        roomsView.append(temp)
        temp = []
        for j in range(i, i + size[1]):
            if j % 2 == even:
                temp.append(rooms[j])
        roomsView.append(temp)
        ##when the column is odd, swap the values of odd and even with each other
        if size[1] % 2 == 1:
            odd, even = even, odd
    
    ## display the 2d view of the maze
    i = 0
    for row in roomsView:
        if i % 2 == 0:
            print("", end="      ")
        for col in row:
            if col in rubbishRoom:
                print("R", end="")
            elif col in disposalRoom:
                print("D", end="")
            elif col in obstacleRoom:
                print("O", end ="")
            elif col == initialState:
                print("S", end="")
            else:
                print("E", end="")
            print(col, end = "      ")
        print()
        i += 1
    print("\nS: Start, E: Empty, R: Rubbish, D: Disposal, O: Obstacle\n")
    
    print("------------------------Results---------------------------\n")
    print("Overall Path: ", end="")
    for i in range(len(overallPath)):
        if overallPath[i] in disposalRoom:
            print("D", end="")
        if overallPath[i] in rubbishRoom:
            print("R", end="")
        print(overallPath[i], end="")
        if (i + 1 == len(overallPath)):
            print("\n")
            continue
        print(" -> ", end="")
    print("Total travel distance: " + str(totaDistance))
    print("Number of disposal room usage: " + str(disposalUsage))
    print("Total Time Execution: %.5fseconds" % (time.time() - start_time))