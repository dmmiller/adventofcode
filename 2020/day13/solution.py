def find_next_bus_time(start, buses):
    x = start
    buses = list(buses)
    while True:
        for bus in buses:
            if x % bus == 0:
                return bus, x
        x += 1
    return -1, -1

def find_earliest_sync_point(buses):
    offset_map = {x : ind for ind, x in enumerate(buses) if x != 'x'}
    offset_value = max(offset_map.keys())
    t = - offset_map[offset_value]
    offset_map.pop(offset_value)
    while len(offset_map) > 0:
        t += offset_value
        for k, v in offset_map.items():
            if t % k == (k - v) % k:
                offset_value *= k
                offset_map.pop(k)
                break
    return t

with open('input.txt') as f:
    start_time = int(f.readline().strip())
    buses = [int(b) if b != 'x' else b for b in f.readline().strip().split(',')]

next_bus, at_time = find_next_bus_time(start_time, filter(lambda x : x != 'x', buses))
print(f"Take bus {next_bus} at {at_time} with answer {next_bus * (at_time - start_time)}")

sync_point = find_earliest_sync_point(buses)
print(f"The earliest point at which buses match offsets is {sync_point}")
