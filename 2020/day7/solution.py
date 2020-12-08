import re

bag_re = re.compile(r"(?P<count>\d+) (?P<color>\w+ \w+) bag.*")

def parse_line(line : str):
    bag, rhs = line.split(" bags contain ")
    bags = []
    for b in rhs.split(", "):
        match = bag_re.match(b)
        if match != None:
            bags.append((match.group('color'), int(match.group('count'))))
    return (bag, bags)

def get_enclosing_bags_recursive(bag_map, bag):
    if bag not in bag_map:
        return set()
    valid_set = set()
    for item in bag_map[bag]:
        valid_set.add(item)
        valid_set = valid_set.union(get_enclosing_bags_recursive(bag_map, item))
    return valid_set

def get_bag_counts_recursive(bag_map, bag):
    count = 0
    for b, c in bag_map[bag]:
        innercount = get_bag_counts_recursive(bag_map, b)
        count += (c * (1 + innercount))
    return count

def build_bag_maps(lines):
    bag_map = {}
    forward_map = {}
    for line in lines:
        bag, contains = parse_line(line.strip())
        forward_map[bag] = contains
        for b in contains:
            if b[0] not in bag_map:
                bag_map[b[0]] = set()
            bag_map[b[0]].add(bag)
    return bag_map, forward_map

with open('input.txt') as f:
    enclosing_map, forward_map = build_bag_maps(f)
    outer_bags = get_enclosing_bags_recursive(enclosing_map, "shiny gold")
    print(f"shiny gold can be enclosed by {len(outer_bags)} bags")
    bag_count = get_bag_counts_recursive(forward_map, "shiny gold")
    print(f"shiny gold has {bag_count} inside")
