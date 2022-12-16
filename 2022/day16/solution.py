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
    previous_location = None if len(actions) == 1 else actions[-2][1]
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
        if tunnel != previous_location:
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
    pare_factor = 7
    while len(options[0]) < 30:
        if scored == False and len(options[0]) % pare_factor == 0:
            scored = True
            max_this_time = previous_max
            seen = set()
            for i in range(len(options)):
                option = options.popleft()
                option_score = score(option)
                if option_score > previous_max:
                    location = option[-1][1]
                    item = (option_score, location)
                    if item not in seen:
                        options.append(option)
                        seen.add(item)
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


def elephantScore(actions: list[Tuple[str, str]]) -> int:
    location = "AA"
    elephant_location = "AA"
    total_pressure = 0
    open_pressure = 0
    open_valves: set[str] = set()

    for minute in range(26):
        total_pressure += sum(map(lambda x: flow_rates[x], open_valves))
        if 2 * minute < len(actions):
            action = actions[2 * minute]
            if action[0] == "MOVE":
                assert action[1] in tunnels[location]
                location = action[1]
            elif action[0] == "OPEN":
                assert location == action[1]
                open_valves.add(location)
            elephant_action = actions[2 * minute + 1]
            if elephant_action[0] == "EMOVE":
                assert elephant_action[1] in tunnels[elephant_location]
                elephant_location = elephant_action[1]
            elif elephant_action[0] == "EOPEN":
                assert elephant_location == elephant_action[1]
                open_valves.add(elephant_location)
    return total_pressure


def generateElephantPathOptions(actions: list[Tuple[str, str]]):
    previous_location = None if len(actions) == 2 else actions[-4][1]
    previous_elephant_location = None if len(actions) == 2 else actions[-3][1]
    location = actions[-2][1]
    elephant_location = actions[-1][1]
    people_options = []
    elephant_options = []
    open_valves = set()
    for action in actions:
        if action[0] == "OPEN" or action[0] == "EOPEN":
            open_valves.add(action[1])
    if len(open_valves) == len(flow_rates):
        new_action = actions.copy()
        new_action.append(("NOOP", location))
        new_action.append(("ENOOP", elephant_location))
        return [new_action]

    if location in flow_rates and location not in open_valves:
        people_options.append(("OPEN", location))
    for tunnel in tunnels[location]:
        if tunnel != previous_location:
            people_options.append(("MOVE", tunnel))

    if elephant_location in flow_rates and elephant_location not in open_valves:
        elephant_options.append(("EOPEN", elephant_location))
    for tunnel in tunnels[elephant_location]:
        if tunnel != previous_elephant_location:
            elephant_options.append(("EMOVE", tunnel))

    paths = []
    for people_option in people_options:
        for elephant_option in elephant_options:
            new_action = actions.copy()
            new_action.append(people_option)
            new_action.append(elephant_option)
            paths.append(new_action)
    return paths


def generateElephantOptions():
    location = "AA"
    initial_options = deque()
    elephant_options = deque()
    for tunnel in tunnels[location]:
        initial_options.append([("MOVE", tunnel)])
        elephant_options.append(("EMOVE", tunnel))
    if location in flow_rates:
        initial_options.append([("OPEN", location)])
        elephant_options.append(("EOPEN", location))

    options = deque()
    for option in initial_options:
        for elephant_option in elephant_options:
            new_option = option.copy()
            new_option.append(elephant_option)
            options.append(new_option)

    scored = False
    previous_max = 0
    pare_factor = 8
    while len(options[0]) < 52:
        if scored == False and len(options[0]) % pare_factor == 0:
            scored = True
            max_this_time = previous_max
            option_at_max = options[0]
            seen = set()
            for i in range(len(options)):
                option = options.popleft()
                option_score = elephantScore(option)
                if option_score > previous_max:
                    item = (option_score, option[-1][1], option[-2][1])
                    if item not in seen:
                        options.append(option)
                        seen.add(item)
                if option_score == previous_max:
                    option_at_max = option
                if option_score > max_this_time:
                    max_this_time = option_score
            previous_max = max_this_time
            if len(options) == 0:
                options.append(option_at_max)
        elif len(options[0]) % pare_factor != 0:
            scored = False

        option = options.popleft()
        for opt in generateElephantPathOptions(option):
            options.append(opt)

    return options


paths = generateElephantOptions()
print(
    f"Part 2: The max pressure with elephant is {max(map(elephantScore, paths))}")
