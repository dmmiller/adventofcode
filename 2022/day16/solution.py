import re
from typing import Tuple
from collections import deque

data = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

with open("input.txt") as f:
    data = f.read()

valve_re = re.compile(
    r"Valve (?P<valve>\w+) has flow rate=(?P<rate>\d+); tunnels? leads? to valves? (?P<tunnels>.*)")

flow_rates: dict[str, int] = dict()
tunnels: dict[str, list[str]] = dict()
for line in data.splitlines():
    valve_info = valve_re.match(line)
    valve = valve_info["valve"]
    flow_rate = int(valve_info["rate"])
    tunnel_info = valve_info["tunnels"]
    if flow_rate > 0:
        flow_rates[valve] = flow_rate
    tunnels[valve] = tunnel_info.split(", ")


def score(actions: list[Tuple[str, str]]) -> int:
    location = "AA"
    total_pressure = 0
    open_pressure = 0
    open_valves: set[str] = set()

    for minute in range(30):
        total_pressure += sum(map(lambda x: flow_rates[x], open_valves))
        if minute < len(actions):
            action = actions[minute]
            if action[0] == "MOVE":
                assert action[1] in tunnels[location]
                location = action[1]
            elif action[0] == "OPEN":
                assert location == action[1]
                open_valves.add(location)
    return total_pressure


def generatePathOptions(actions: list[Tuple[str, str]]):
    location = actions[-1][1]
    paths = []
    open_valves = set()
    for action in actions:
        if action[0] == "OPEN":
            open_valves.add(action[1])
    if len(open_valves) == len(flow_rates):
        new_action = actions.copy()
        new_action.append(("NOOP", location))
        return [new_action]

    if location in flow_rates and location not in open_valves:
        new_action = actions.copy()
        new_action.append(("OPEN", location))
        paths.append(new_action)

    for tunnel in tunnels[location]:
        new_action = actions.copy()
        new_action.append(("MOVE", tunnel))
        paths.append(new_action)
    return paths


def generateOptions():
    location = "AA"
    options = deque()
    for tunnel in tunnels[location]:
        options.append([("MOVE", tunnel)])
    if location in flow_rates:
        options.append([("OPEN", location)])

    scored = False
    previous_max = 0
    pare_factor = 5
    while len(options[0]) < 30:
        if scored == False and len(options[0]) % pare_factor == 0:
            scored = True
            max_this_time = previous_max
            for i in range(len(options)):
                option = options.popleft()
                option_score = score(option)
                if option_score > previous_max:
                    options.append(option)
                if option_score > max_this_time:
                    max_this_time = option_score
            previous_max = max_this_time
        elif len(options[0]) % pare_factor != 0:
            scored = False

        option = options.popleft()
        for opt in generatePathOptions(option):
            options.append(opt)

    return options


paths = generateOptions()
print(f"Part 1 : The max pressure is {max(map(score, paths))}")
