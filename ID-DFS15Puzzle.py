import random
import collections
from time import time

goalstate = "ABCDEFGHIJKLMNOZ"
NODECOUNTER = 0

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

def lim_dfs(start_node, depth):
    global NODECOUNTER
    fringe = collections.deque()
    fringe.appendleft(start_node)
    visited = set()
    i = 0
    while not len(fringe) == 0:
        v = fringe.popleft()
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
            if c.depth <= depth:
                fringe.appendleft(c)
                visited.add(c.state)
                NODECOUNTER += 1
        i += 1
    return None

def id_dfs(start_node):
    count = 1
    while True:
        result = lim_dfs(start_node, count)
        if result is not None:
            return result
        count += 1

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

def generateState(i):
    state = goalstate
    dirs = "UDLR"
    count = 0
    visited = set()
    while count <= int(i):
        newState = make_move(state, dirs[random.randrange(0, 4)])
        if newState != "INVALID" and newState not in visited:
            visited.add(newState)
            count += 1
            state = newState
    print(state)

def getLength(start_node):
    goalNode = id_dfs(start_node)
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
        return ((len(path)))
    else:
        return -1

def printPath(start_node):
    goalNode = id_dfs(start_node)
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
    generateState(15)
    start = input("Enter the String.\t")
    tic = time()
    #print("LENGTH:", getLength(Node(start, None)))
    print("# OF MOVES:", getLength(Node(start, None)) - 1)  # you need to subtract 1 because it includes the starting node
    print("# OF NODES:", NODECOUNTER)
    toc = time()
    print("EXECUTION TIME: %5.2f seconds" % (toc - tic))
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