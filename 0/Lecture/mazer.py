




class Node():
    #--Created when instance made:
    def __init__(self, state, parent, action):
        self.state = state # current location
        self.parent = parent # parent node
        self.action = action # direction moved


class StackFrontier():
    """
    Depth-First Search uses a Stack: last-in, first-out.
    - Algorithm goes as deep as possible in first direction, then returns to 2nd path (deep as possible), &c.
    """
    #
    def __init__(self):
        self.frontier = [] # empty frontier to start
    #
    def add(self, node):
        self.frontier.append(node)
    #
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    #
    def empty(self):
        #--True if frontier is empty else False
        return len(self.frontier) == 0
    #
    def remove(self):
        #--End search if frontier is empty (no possible solution):
        if self.empty():
            raise Exception("Frontier is empty!")
        else:
            #--Get LAST-IN node
            node = self.frontier[-1]
            #--Save new frontier (all minus LAST-IN)
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):
    """
    Breadth-first Search uses a Queue: first-in, first-out.
    - Algorithm is first-come, first-serve. Takes one step in each possible direction before taking a 2nd step in any direction, &c.
    """
    #
    def remove(self):
        #--End search if Frontier empty (no possible solution):
        if self.empty():
            raise Exception("Frontier is empty!")
        else:
            #--Get FIRST-IN node to use next:
            node = self.frontier[0]
            #--Save new frontier (all minus FIRST-IN node just removed):
            self.frontier = self.frontier[1:]
            return node


class Maze():
    #
    def __init__(self, maze):
        contents = maze
    #












#
