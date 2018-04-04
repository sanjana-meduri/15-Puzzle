import random
import heapq
from time import time

goalstate = "ABCDEFGHIJKLMNOZ"
NODECOUNTER = 0

def n2ij(i):
    return [i // 4, i % 4]

goal = {"A": [0, 0], "B": [0, 1], "C": [0, 2], "D": [0, 3], "E": [1, 0], "F": [1, 1], "G": [1, 2], "H": [1, 3],
        "I": [2, 0], "J": [2, 1], "K": [2, 2], "L": [2, 3], "M": [3, 0], "N": [3, 1], "O": [3, 2], "Z": [3, 3]}

class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.children = []
        self.dirFromParent = ""
        if self.parent == None:
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1
    def addChild(self, child):
        self.children.append(child)
    def toString(self):
        return "" + str(self.state)

def swap(s, i, j):
    l = list(str(s))
    l[i], l[j] = l[j], l[i]
    return "".join(l)

def manhattanDistance(node):
    sum = 0
    for i in range(0, 16):
        if node.state[i] is not "Z":
            sum += (abs((i // 4) - goal[node.state[i]][0]) + abs((i % 4) - goal[node.state[i]][1]))
    return sum + node.depth
#ABCDEFGHMIJKZNOL

def bfs(start_node):
    global NODECOUNTER
    fringe = []
    visited = set()
    heapq.heappush(fringe, start_node)
    entry = 0
    while not len(fringe) == 0:
        v = heapq.heappop(fringe)
        if type(v) is list:
            v = v[2]
        visited.add(v.state)
        if v.toString() == goalstate:
            return v
        dirs = "UDLR"
        for c in dirs:
            c = str(c)
            newStr = make_move(str(v.toString()), c)
            if newStr != "INVALID" and newStr not in visited and newStr != v.toString():
                child = Node(newStr, v)
                child.dirFromParent = c + ""
                v.addChild(child)
        for c in v.children:
            heapq.heappush(fringe,[manhattanDistance(c), entry, c])
            NODECOUNTER += 1
            entry += 1
    return None

def make_move(str, dir):
    if dir == "U" and str.index("Z") > 3:
        return swap(str, str.index("Z"), str.index("Z") - 4)
    if dir == "D" and str.index("Z") < 12:
        return swap(str, str.index("Z"), str.index("Z") + 4)
    if dir == "R" and (str.index("Z") - 3) % 4 != 0:
        return swap(str, str.index("Z"), str.index("Z") + 1)
    if dir == "L" and str.index("Z") % 4 != 0:
        return swap(str, str.index("Z"), str.index("Z") - 1)
    return "INVALID"

def goal_test(str):
    return str == goalstate

def get_ij(str, i, j):
    return str[int(i) * 3 + int(j)]     #CHANGE LAST

def set_ij(str, i, j):
    newStr = (str + " ")[:-1]
    str[int(i) * 3 + int(j)] = newStr       #CHANGE LAST

def makeMatrix(s):
    s = str(s)
    s = s.replace("Z", "_")
    return " ".join(list(s[:3])) + "\n" + " ".join(s[3:6]) + "\n" + " ".join(s[6:]) + "\n" #CHANGE LAST

def generaterRanState():
    state = goalstate
    dirs = "UDRL"
    rep = random.randrange(0, 5)
    for x in range(0, rep):
        newState = make_move(state, dirs[random.randrange(0, 4)])
        if newState != "INVALID":
            state = str(newState)
    print(state)
    print("# of shuffles:", rep)

def generateState():
    state = goalstate
    dirs = "UDLR"
    count = 0
    visited = set()
    while count <= random.randrange(0, 30):
        newState = make_move(state, dirs[random.randrange(0, 4)])
        if newState != "INVALID" and newState not in visited:
            visited.add(newState)
            count += 1
            state = newState
    print(state)

def getLength(start_node):
    goalNode = bfs(start_node)
    moves = ""
    if goalNode != None:
        pointer = goalNode
        path = []
        while pointer.parent != None:
            path.append(pointer.parent.toString())
            moves += (pointer.dirFromParent + ", ")
            pointer = pointer.parent
        path.reverse()
        path.append(goalNode.toString())
        return (len(path))
    else:
        return -1

def printPath(start_node):
    goalNode = bfs(start_node)
    moves = ""
    if goalNode != None:
        pointer = goalNode
        path = []
        while pointer.parent != None:
            path.append(pointer.parent.toString())
            moves += (pointer.dirFromParent + ", ")
            pointer = pointer.parent
        path.reverse()
        path.append(goalNode.toString())
        print("Path: ")
        for s in path:
            print(makeMatrix(s))
        print("Length of path:", len(path))
        if len(moves[:-2]) == 0:
            print("# of moves:", 0)
            print("List of moves: NO MOVES")
        else:
            print("# of moves:", len(moves[:-2].split(", ")))
            print("List of moves:", moves[:-2])
    else:
        print("There are no solutions to the puzzle you entered.")

def main():
    generateState()
    start = input("Enter the String.\t")
    bfs(Node(start, None))
    tic = time()
    #print("LENGTH:", getLength(Node(start, None)))
    print("# OF MOVES:", getLength(Node(start, None)) - 1) #you need to subtract 1 because it includes the starting node
    print("# OF NODES:", NODECOUNTER)
    toc = time()
    print("EXECUTION TIME: %10.10f seconds" % (toc - tic))
    '''''
    file = open("puzzles.txt", "r")
    for line in file:
        print(line.strip())
        tic = time()
        print("PATH LENGTH: " + getLength(Node(line.strip(), None)))
        toc = time()
        print("EXECUTION TIME: %5.2f seconds" % (toc - tic))
        print()
    '''

if __name__ == "__main__":
    main()

#14 - ABZCEGHDIFLOMKJN
#17 - AJFCENZDIGBHMOKL
#19 - ABCDEJZHMOFKNILG