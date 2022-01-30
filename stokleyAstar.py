import math

data=[[4, "G", 4, 6],
      [2, 9, 9, 6],
      [1, 4, "S", 3]]

class Node:
    def __init__(self, coordinates, orientation, cumulative_cost):
        self.coordinates = coordinates
        self.orientation = orientation
        self.cumulative_cost = cumulative_cost
        self.path = []

class PaFinder:

    def __init__(self, map):
        self.map = map
        self.goal = [0, 0]
        self.current = [0, 0]
        self.frontier = []
        self.exploring = []
        self.visited = []
        self.counter = 0

        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == "S":
                    self.current = [x, y]
                    self.exploring = [x, y]
                elif self.map[y][x] == "G":
                    self.goal = [x, y]

    def get_turn_cost(self):
        turn_cost = self.map[self.current[1]][self.current[0]]
        if turn_cost == 'S':
            turn_cost = 1
        turn_cost = math.ceil((turn_cost/2))
        return turn_cost

    def forward_cost(self):
        forward_cost = self.map[self.exploring[1]][self.exploring[0]]
        if forward_cost == 'S' or forward_cost == 'G':
            forward_cost = 1
        return forward_cost

    def dictionary_holder(self, action_needed, creation):
        if action_needed == "TURNING" and creation == True:
            return {
                "None": 0,
                "Left": self.get_turn_cost(),
                "Right": self.get_turn_cost(),
                "Reverse": (2 * self.get_turn_cost()),
            }
        if action_needed == "TURNING" and creation != True:
            return {
                "None": 0,
                "Left": self.get_turn_cost(),
                "Right": self.get_turn_cost(),
            }
        if action_needed == "MOVE":
            return {
                "Forward": self.forward_cost(),
                "Bash": (self.forward_cost() + 3),
            }

    def dictionary_holder_empty(self, action_needed, creation):
        if action_needed == "TURNING" and creation == True:
            return {
                "None": 0,
                "Left": 0,
                "Right": 0,
                "Reverse": 0,
            }
        if action_needed == "TURNING" and creation != True:
            return {
                "None": 0,
                "Left": 0,
                "Right": 0,
            }
        if action_needed == "MOVE":
            return {
                "Forward": 0,
                "Bash": 0,
            }

    # takes self and returns a frontier
    def create_frontier(self):
        self.counter += 1
        parent_node = Node(self.current, 0, 1)
        for turn in self.dictionary_holder_empty("TURNING", True).keys():
            holder = []
            new_orientation = []
            for move in self.dictionary_holder_empty("MOVE", True).keys():
                self.exploring = []
                # Orientation was set to Zero because we know it is north
                newx, newy = self.result(self.current, turn, move, 0)[0]
                new_orientation = self.result(self.current, turn, move, 0)[1]
                if newy in range(len(self.map)) and newx in range(len(self.map[newy])):
                    self.exploring = [newx, newy]

                    temp_cost = self.dictionary_holder("TURNING", True)[turn] + self.dictionary_holder("MOVE", True)[move]
                    #TODO temp_cost + heuristic 
                    new_node = Node(self.exploring, new_orientation, temp_cost)
                    if turn == "None":
                        new_node.path = (('%s')%(move))
                    elif turn != "None":
                        new_node.path = (('%s %s')%(turn, move))
                    self.frontier.append(new_node)
                    self.visited.append(self.current)

    def orientation_finder(self, turn, orientation):
        new_orientation = 700
        if turn.count("Right"):
            new_orientation = orientation + 90
        if turn.count("Left"):
            new_orientation = orientation - 90
        if turn.count("None"):
            new_orientation = orientation
        if turn.count("Reverse"):
            new_orientation = orientation + 180
        if new_orientation <= -360:
            new_orientation = new_orientation + 360
        if new_orientation >= 360:
            new_orientation = new_orientation - 360
        return new_orientation

    def result(self, position, turn, move, orientation):
        x, y = position
        new_orientation = []
        holder = []
        turn = turn
        orientation = orientation
        new_orientation = self.orientation_finder(turn, orientation)
        if new_orientation == 0:
            if move.count("Forward"):
                y -= 1
            if move.count("Bash"):
                y -= 2
        if new_orientation == 180 or new_orientation == -180:
            if move.count("Forward"):
                y += 1
            if move.count("Bash"):
                y += 2
        if new_orientation == 90 or new_orientation == -270:
            if move.count("Forward"):
                x += 1
            if move.count("Bash"):
                x += 2
        if new_orientation == 270 or new_orientation == -90:
            if move.count("Forward"):
                x -= 1
            if move.count("Bash"):
                x -= 2
        new_position = (x, y)
        holder = [new_position, new_orientation]
        return holder

    def cheapest_node(self):
        lowest_cost = 1000
        lowest_node = []
        for node in self.frontier:
            if node.cumulative_cost < lowest_cost:
                lowest_cost = node.cumulative_cost
                lowest_node = node
        return lowest_node

    def not_visited(self, value):
        for item in self.visited:
            if item == value:
                return False
        return True

    def expand_frontier(self):
        parent_node = self.cheapest_node()
        self.current = parent_node.coordinates

        for turn in self.dictionary_holder_empty("TURNING", False).keys():
            holder = []
            new_orientation = []
            for move in self.dictionary_holder_empty("MOVE", False).keys():
                self.exploring = []
                newx, newy = self.result(parent_node.coordinates, turn, move, parent_node.orientation)[0]
                new_orientation = self.result(parent_node.coordinates, turn, move, parent_node.orientation)[1]

                if newy in range(len(self.map)) \
                        and newx in range(len(self.map[newy])) \
                        and self.not_visited([newx, newy]):

                    self.exploring = [newx, newy]

                    temp_cost = self.dictionary_holder("TURNING", False)[turn] + self.dictionary_holder("MOVE", False)[move]
                    #TODO temp_cost + heuristic
                    new_node = Node(self.exploring, new_orientation, (parent_node.cumulative_cost + temp_cost))
                    new_node.path.append(parent_node.path)
                    if turn == "None":
                        new_node.path.append(('%s')%(move))
                    elif turn != "None":
                        new_node.path.append(('%s %s')%(turn, move))
                    self.frontier.append(new_node)
                    self.visited.append(self.current)

    def iterator(self):
        cheapest_node = self.cheapest_node()
        if cheapest_node.coordinates != self.goal:
            self.counter += 1
            self.expand_frontier()
            self.frontier.remove(cheapest_node)
            self.iterator()
        if cheapest_node.coordinates == self.goal:
            print(cheapest_node.path, cheapest_node.cumulative_cost, self.counter)


test = PaFinder(data)

test.create_frontier()

test.iterator()