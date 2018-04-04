#TO DO:
#   FIX KDFS AND IDDFS
#   FIX NODECOUNTER ON BI-BFS

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
        '''
        if parent is None:
            self.ancestors = {}
        else:
            self.ancestors = {parent.state}
            self.ancestors = self.ancestors.union(parent.ancestors)
        '''
        self.ancestors = set()
        if parent:
            self.ancestors = parent.ancestors.copy()
            self.ancestors.add(parent.state)
        self.depth = parent.depth + 1 if parent else 0
        '''
        if self.parent == None:
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1
        '''
    def addChild(self, child):
        self.children.append(child)
    def toString(self):
        return "" + str(self.state)
    def __str__(self):
        return self.state

#HELPER METHODS
def swap(s, i, j):
    l = list(str(s))
    l[i], l[j] = l[j], l[i]
    return "".join(l)

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
    #TODO: Change
    return str[int(i) * 3 + int(j)]

def set_ij(str, i, j):
    #TODO: Change
    newStr = (str + " ")[:-1]
    str[int(i) * 3 + int(j)] = newStr

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

#FORMATTING AND PRINTING
def getLength(goalNode):
    print(goalNode.state)
    if goalNode != None:
        pointer = goalNode
        length = 0
        while pointer.parent != None:
            length += 1
            pointer = pointer.parent
        return (length)
    else:
        return -1

'''ALGORITHMS'''
#BFS
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
    return None

#DFS
def dfs(start_node):
    global NODECOUNTER
    fringe = collections.deque()
    fringe.append(start_node)
    while not len(fringe) == 0:
        v = fringe.popleft()
        if v.state == goalstate:
            return v
        dirs = "UDLR"
        for c in dirs:
            # c = str(c)
            newStr = make_move(str(v.toString()), c)
            if newStr != "INVALID" and newStr not in v.ancestors and newStr != v.toString():
                child = Node(newStr, v)
                child.dirFromParent = c + ""
                v.addChild(child)
        for c in v.children:
            fringe.appendleft(c)
            NODECOUNTER += 1
    return None

def k_dfs(start_node, depth=80):
    global NODECOUNTER
    fringe = collections.deque()
    fringe.append(start_node)
    while fringe:
        v = fringe.popleft()
        if v.toString() == goalstate:
            return v
        dirs = "UDLR"
        for c in dirs:
            newStr = make_move(v.state, c)
            if v.depth + 1 <= depth and newStr != 'INVALID' and newStr not in v.ancestors:
                child = Node(newStr, v)
                child.dirFromParent = c
                fringe.appendleft(child)
                NODECOUNTER += 1
    return None

#ID-DFS
def id_dfs(start_node, depth):
    counter = 1
    while counter <= depth:
        ans = k_dfs(start_node, counter)
        if ans is not None:
            return ans
        counter += 1
    return None

#Greedy Search
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

#Bi-Directional BFS
dict1 = {}
dict2 = {}
def bi_bfs(start_node):
    global NODECOUNTER
    global dict1
    global dict2
    fringe1 = collections.deque()
    fringe2 = collections.deque()
    visited1 = set()
    visited2 = set()
    start = Node(start_node, None)
    goal = Node(goalstate, None)
    fringe1.append(start)
    fringe2.append(goal)
    visited1.add(start_node)
    visited2.add(goalstate)
    dict1[start_node] = start
    dict2[goalstate] = goal
    while not len(fringe1) == 0 or not len(fringe2) == 0:
        if not len(fringe1) == 0:
            v1 = fringe1.popleft()
            dirs = "UDLR"
            for c in dirs:
                c = str(c)
                newStr1 = make_move(str(v1.toString()), c)
                if newStr1 != "INVALID" and newStr1 not in visited1 and newStr1 != v1.toString():
                    child1 = Node(newStr1, v1)
                    child1.dirFromParent = c + ""
                    v1.addChild(child1)
                    dict1[newStr1] = child1
            for c in v1.children:
                fringe1.append(c)
                NODECOUNTER += 1
                visited1.add(c.state)
            intersection = visited1.intersection(visited2)
            if len(intersection) != 0:
                visited1.add(start_node)
                return intersection.pop()

        if not len(fringe2) == 0:
            v2 = fringe2.popleft()
            dirs = "UDLR"
            for c in dirs:
                newStr2 = make_move(v2.state, c)
                if newStr2 != "INVALID" and newStr2 not in visited2 and newStr2 != v2.state:
                    child2 = Node(newStr2, v2)
                    child2.dirFromParent = c
                    v2.addChild(child2)
                    dict2[newStr2] = child2
            for c in v2.children:
                fringe2.append(c)
                NODECOUNTER += 1
                visited2.add(c.state)
            intersection = visited1.intersection(visited2)
            if len(intersection) != 0:
                visited1.add(start_node)
                return intersection.pop()
    return None
def bi_bfs_length(start_node):
    global NODECOUNTER
    state = bi_bfs(start_node)
    one = dict1[state]
    two = dict2[state]
    return dict1[state].depth + dict2[state].depth

def bi_bfs_path(start_node):
    path = []
    if start_node is not None:
        pointer = dict1[start_node]
        while pointer.parent is not None:
            path.append(pointer.parent.state)
            pointer = pointer.parent
        path = path.reverse()
        pointer = dict2[start_node]
        while pointer.parent is not None:
            path.append(pointer.parent.state)
            pointer = pointer.parent
    return path

def main():
    start = ""
    global NODECOUNTER
    while start != "-1":
        start = Node(input("Enter the String.\t"), None)
        print("RUNNING: K_DFS")
        tic = time()
        answer = bi_bfs(start)
        toc = time()
        print(answer.state)
        #print("# OF MOVES:", answer.depth)
        #print("# OF NODES:", NODECOUNTER)
        #print("EXECUTION TIME: %10.10f seconds" % (toc - tic))
        #print("NODES/SEC: %10.10f nodes/second" % (NODECOUNTER/(toc - tic)))
        NODECOUNTER = 0
        print()

def file_main():
    global NODECOUNTER
    file = open("testcases", "r")
    for line in file:
        state = Node(line.strip(), None)
        print("----> Solving\t", state.state)
        tic = time()
        answer = bfs(state)
        toc = time()
        print("Solved. %10s %8i Nodes\t %4i Steps\t %5.5f secs\t %6.0f N/s" % ("BFS", NODECOUNTER, answer.depth, toc-tic, NODECOUNTER / (toc-tic)))
        tic = time()
        NODCOUNTER = 0
        answer = bi_bfs_length(state.state)
        toc = time()
        print("Solved. %10s %8i Nodes\t %4i Steps\t %5.5f secs\t %6.0f N/s" % ("bi_BFS", NODECOUNTER, answer, toc-tic, NODECOUNTER / (toc-tic)))
        tic = time()
        NODECOUNTER = 0
        answer = id_dfs(state, 22)
        toc = time()
        print("Solved. %10s %8i Nodes\t %4i Steps\t %5.5f secs\t %6.0f N/s" % ("IDDFS", NODECOUNTER, answer.depth, toc-tic, NODECOUNTER / (toc-tic)))
        tic = time()
        NODECOUNTER = 0
        answer = greedySearch(state)
        toc = time()
        print("Solved. %10s %8i Nodes\t %4i Steps\t %5.5f secs\t %6.0f N/s\n" % ("Best_FS", NODECOUNTER, answer.depth, toc-tic, NODECOUNTER / (toc-tic)))
    print("DONE.")
       





def bi_bfs_main():
    print(bi_bfs_length(input("Enter node.\t")))
    print("----> Solving", )

def bi_bfs_file_main():
    global NODECOUNTER
    file = open("testcases", "r")
    for line in file:
        state = Node(line.strip(), None)
        print("----> Solving", state.state)
        tic = time()
        ans = bfs(state)
        toc = time()
        print("Solved.\t BFS\t", NODECOUNTER, "Nodes\t", ans.depth, "Steps\t%10.10f secs" % (toc - tic))
        print(state.state)
        tic = time()
        ans = bi_bfs_length(state.state)
        toc = time()
        print("# OF NODES:", NODECOUNTER)
        print("# OF MOVES:", ans)
        print("EXECUTION TIME: %10.10f seconds" % (toc - tic))
        print("NODES/SEC: %10.10f nodes/second" % (NODECOUNTER / (toc - tic)))
        NODECOUNTER = 0
        print()
    print("DONE.")

def test_method(f, args, verbose = 1):
    global NODE_COUNTER
    NODE_COUNTER = 0

    tic = time()
    sol = f(*args)
    toc = time()

    if verbose == 1:
        print("\n------Testing %s ------- \n" % f.__name__)
        if sol is not None:
            print("Solution Found")
            print("Node count: %i" % NODE_COUNTER)
            print("Length: %i steps, Time: %5.4f" % (sol.depth, toc-tic))
            #print_steps(sol)
        else:
            print("Unsolvable")

    elif verbose == 0:
        if sol is not None:
            print("Solved. %10s %8i Nodes\t %4i Steps\t %5.5f secs\t %6.0f N/s" % (f.__name__, NODE_COUNTER, sol.depth, toc-tic, \
                                                                                  NODE_COUNTER / (toc-tic)))
        else:
            print("Unsolv. %10s %8i Nodes\t %4i Steps\t %5.5f secs\t %6.0f N/s" % (f.__name__, NODE_COUNTER, 0, toc-tic, \
                                                                                  NODE_COUNTER / (toc-tic)))

def multi_solver(start_state = None):
        state = start_state
        print("\n---->Solving ", state)

        test_method(bfs, (Node(state, None),), 0)
        test_method(bi_bfs, (state,), 0)
        test_method(k_dfs, (Node(state, None),22), 0)
        test_method(id_dfs, (Node(state, None),22), 0)
        test_method(greedySearch, (Node(state, None),), 0)



if __name__ == "__main__":
    file_main()