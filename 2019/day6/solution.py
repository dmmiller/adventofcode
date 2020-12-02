class Node:
    def __init__(self, name : str) -> None:
        self.name = name
        self.parent = None
        self.orbit_distance = None
    
    def set_parent(self, parent) -> None:
        self.parent = parent

    def compute_orbit_distance(self) -> int:
        if self.orbit_distance != None:
            return self.orbit_distance
        if self.parent == None:
            self.orbit_distance = 0
        else:
            self.orbit_distance = 1 + self.parent.compute_orbit_distance()
        return self.orbit_distance

    def compute_orbital_jumps(self, other) -> int:
        self_seen = {}
        self_parent = self.parent
        while self_parent != None:
            self_seen[self_parent.name] = self_parent
            self_parent = self_parent.parent
        other_parent = other.parent
        while other_parent.name not in self_seen:
            other_parent = other_parent.parent
        common_parent = other_parent
        print ("common node is ", common_parent.name)
        self_parent = self.parent
        self_count = 0
        while self_parent != common_parent:
            self_count += 1
            self_parent = self_parent.parent
        other_count = 0
        other_parent = other.parent
        while other_parent != common_parent:
            other_count += 1
            other_parent = other_parent.parent
        return self_count + other_count


nodes = {}
file = open('input.txt')
for line in file:
    parent, child = line.strip().split(')')
    if parent not in nodes:
        parent_node = Node(parent)
        nodes[parent] = parent_node        
    if child not in nodes:
        child_node = Node(child)
        nodes[child] = child_node
    parent_node = nodes[parent]
    child_node = nodes[child]
    child_node.set_parent(parent_node)

total_orbits = 0
for node in nodes.values():
    total_orbits += node.compute_orbit_distance()

print("Total orbital distance for part 1 is ", total_orbits)

you_node = nodes["YOU"]
santa_node = nodes["SAN"]
print("Total orbital jumps for part 2 is ", you_node.compute_orbital_jumps(santa_node))