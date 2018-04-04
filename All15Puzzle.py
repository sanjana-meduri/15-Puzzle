import random
import heapq
import collections
from time import time

goalstate = "ABCDEFGHIJKLMNO."
NODECOUNTER = 0

goal = {"A": [0, 0], "B": [0, 1], "C": [0, 2], "D": [0, 3], "E": [1, 0], "F": [1, 1], "G": [1, 2], "H": [1, 3],
        "I": [2, 0], "J": [2, 1], "K": [2, 2], "L": [2, 3], "M": [3, 0], "N": [3, 1], "O": [3, 2], ".": [3, 3]}

class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.children = []
        self.dirFromParent = ""
        if parent is None:
            self.ancestors = {}
        else:
            self.ancestors = {parent.state}
            self.ancestors = self.ancestors.union(parent.ancestors)
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

#BFS START
def bfs(start_node):
    global NODECOUNTER
    fringe = collections.deque()
    visited = set()
    fringe.append(start_node)
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
            fringe.append(c)
            NODECOUNTER += 1
            visited.add(c.state)
#BFS END

#GREEDY SEARCH START
def manhattanDistance(node):
    sum = 0
    for i in range(0, 16):
        if node.state[i] is not ".":
            sum += (abs((i // 4) - goal[node.state[i]][0]) + abs((i % 4) - goal[node.state[i]][1]))
    return sum + node.depth

def greedySearch(start_node):
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
#GREEDY SERACH END

#DFS START
def dfs(start_node):
    global NODECOUNTER
    fringe = collections.deque()
    fringe.appendleft(start_node)
    visited = set()
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
            fringe.appendleft(c)
            visited.add(c.state)
            NODECOUNTER += 1
    return None
'''
def k_dfs(start_node, depth):
    global NODECOUNTER
    fringe = collections.deque()
    fringe.appendleft(start_node)
    while not len(fringe) == 0:
        v = fringe.popleft()
        if v.toString() == goalstate:
            return v
        dirs = "UDLR"
        for c in dirs:
            c = str(c)
            newStr = make_move(str(v.toString()), c)
            if newStr != "INVALID" and newStr not in v.ancestors and newStr != v.toString():
                child = Node(newStr, v)
                child.dirFromParent = c + ""
                v.addChild(child)
                print("Depth:", child.depth)
                print("Ancestors:", len(child.ancestors))
        for c in v.children:
            if c.depth <= depth:
                fringe.appendleft(c)
                NODECOUNTER += 1
    return None
'''
#DFS END

#ITERATIVE DEPTH-DFS START
'''
def lim_dfs(start_node, depth):
    global NODECOUNTER
    fringe = collections.deque()
    fringe.appendleft(start_node)
    while not len(fringe) == 0:
        v = fringe.popleft()
        if v.toString() == goalstate:
            return v
        dirs = "UDLR"
        for c in dirs:
            c = str(c)
            newStr = make_move(str(v.toString()), c)
            if newStr != "INVALID" and newStr not in v.ancestors and newStr != v.toString():
                child = Node(newStr, v)
                child.dirFromParent = c + ""
                v.addChild(child)
        for c in v.children:
            if c.depth <= depth:
                fringe.appendleft(c)
                NODECOUNTER += 1
    return None
'''
def k_DFS(start_node, depth):
    global NODECOUNTER
    fringe = collections.deque()
    fringe.appendleft(start_node)
    while not len(fringe) == 0:
        v = fringe.popleft()
        if v.toString() == goalstate:
            return v
        dirs = "UDLR"
        for c in dirs:
            c = str(c)
            newStr = make_move(str(v.toString()), c)
            if newStr != "INVALID" and newStr not in v.ancestors and newStr != v.toString():
                child = Node(newStr, v)
                child.dirFromParent = c + ""
                v.addChild(child)
        for c in v.children and c.depth <= depth:
            fringe.appendleft(c)
            NODECOUNTER += 1
    return None

def id_dfs(start_node, depth):
    count = 1
    while count <= depth:
        result = k_DFS(start_node, count)
        if result is not None:
            return result
        count += 1
    return None
#ITERATIVE DEPTH-DFS END

#BILATERIAL BFS START
#BILATERAL BFS END

#HELPER METHODS START
def make_move(str, dir):
    if dir == "U" and str.index(".") > 3:
        return swap(str, str.index("."), str.index(".") - 4)
    if dir == "D" and str.index(".") < 12:
        return swap(str, str.index("."), str.index(".") + 4)
    if dir == "R" and (str.index(".") - 3) % 4 != 0:
        return swap(str, str.index("."), str.index(".") + 1)
    if dir == "L" and str.index(".") % 4 != 0:
        return swap(str, str.index("."), str.index(".") - 1)
    return "INVALID"

def goal_test(str):
    return str == goalstate

def get_ij(str, i, j):
    return str[int(i) * 3 + int(j)]     #CHANGE

def set_ij(str, i, j):
    newStr = (str + " ")[:-1]
    str[int(i) * 3 + int(j)] = newStr       #CHANGE

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
    return state
#HELPER METHODS END

#FORMATTING AND PRINTING METHODS START
def makeMatrix(s):
    s = str(s)
    s = s.replace(".", "_")
    return " ".join(list(s[:3])) + "\n" + " ".join(s[3:6]) + "\n" + " ".join(s[6:]) + "\n" #CHANGE LAST


def getLength(goalNode):
    if goalNode != None:
        pointer = goalNode
        length = 0
        while pointer.parent != None:
            length += 1
            pointer = pointer.parent
        return (length)
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
#FORMATTING AND PRINTING METHODS END


def main():
    start = ""
    global NODECOUNTER
    while start != "-1":
        #print(generateState())
        start = input("Enter the String.\t")
        print("RUNNING: BFS")
        tic = time()
        answer = bfs(Node(start, None))
        toc = time()
        #print("LENGTH:", getLength(Node(start, None)))
        print("# OF MOVES:", getLength(answer)) #you need to subtract 1 because it includes the starting node
        print("# OF NODES:", NODECOUNTER)
        print("EXECUTION TIME: %10.10f seconds" % (toc - tic))
        print("NODES/SEC: %10.10f nodes/second" % (NODECOUNTER/(toc - tic)))
        NODECOUNTER = 0
        print()

def file_main():
    global NODECOUNTER
    file = open("testcases", "r")
    for line in file:
        state = Node(line.strip(), None)
        print(state.state)
        tic = time()
        answer = id_dfs(state, 25)
        toc = time()
        print("# OF NODES:", NODECOUNTER)
        print("# OF MOVES:", getLength(answer))  # you need to subtract 1 because it includes the starting node
        print("EXECUTION TIME: %10.10f seconds" % (toc - tic))
        print("NODES/SEC: %10.10f nodes/second" % (NODECOUNTER / (toc - tic)))
        NODECOUNTER = 0
        print()
    print("DONE.")

if __name__ == "__main__":
    file_main()

#14 - ABZCEGHDIFLOMKJN
#17 - AJFCENZDIGBHMOKL
#19 - ABCDEJZHMOFKNILG
