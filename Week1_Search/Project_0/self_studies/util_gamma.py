import heapq


class Node():
    def __init__(self, state, parent, action, cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node



class PriorityQueueFrontier:
    def __init__(self):
        self.frontier = []
        self.entry_count = 0  # To handle nodes with equal priority

    def add(self, node, priority):
        # Use a tuple of (priority, entry_count, node) to ensure FIFO order for equal priorities
        heapq.heappush(self.frontier, (priority, self.entry_count, node))
        self.entry_count += 1

    def contains_state(self, state):
        return any(node.state == state for _, _, node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty")
        _, _, node = heapq.heappop(self.frontier)
        return node
