import re
from datetime import datetime
from itertools import groupby, chain


def parse_line(line):
    result = re.match(r"^\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\] (.*)\n", line)
    y, m, d, th, tm = map(int, result.group(1, 2, 3, 4, 5))
    instruction = result.group(6)
    dt = datetime(y, m, d, hour=th, minute=tm)
    return dt, instruction


def entries_to_records(entries):
    records = []
    guard_id = None
    for entry in entries:
        dt, instruction = entry
        if instruction == "falls asleep":
            records.append((dt, guard_id, "S"))
            continue
        if instruction == "wakes up":
            records.append((dt, guard_id, "W"))
            continue
        result = re.match(r"Guard #(\d+) begins shift", instruction)
        guard_id = int(result.group(1))
    return records


def get_minutes(rs):
    pairs = zip(rs[::2], rs[1::2])
    ranges = [list(range(s[0].minute, w[0].minute)) for s, w in pairs]
    return sorted(chain(*ranges))


def make_guards_to_minutes(guards_to_records):
    return {g: get_minutes(rs) for g, rs in guards_to_records.items()}


def part1(guards_to_minutes):
    guard, minutes = max(guards_to_minutes.items(), key=lambda kvp: len(kvp[1]))
    minutes_grouped = groupby(minutes)
    minutes_to_num_occurrences = {minute: len(list(occurrences)) for minute, occurrences in minutes_grouped}
    minute, _ = max(minutes_to_num_occurrences.items(), key=lambda kvp: kvp[1])
    print(f"part 1 answer: {guard * minute}")


def most_occurring_minute(minutes):
    v1 = {m: len(list(ms)) for m, ms in groupby(minutes)}
    v2 = sorted(v1.items(), key=lambda kvp: kvp[1], reverse=True)
    return v2[0]


def part2(guards_to_minutes):
    guard_to_most_occurring_minutes = {g: most_occurring_minute(m) for g, m in guards_to_minutes.items()}
    guard, (minute, _) = max(guard_to_most_occurring_minutes.items(), key=lambda kvp: kvp[1][1])
    print(f"part 2 answer: {guard * minute}")


if __name__ == "__main__":
    with open("aoc/2018/Day04/input.txt") as f:
        lines = f.readlines()
        parsed_entries = [parse_line(line) for line in lines]
        sorted_entries = sorted(parsed_entries, key=lambda entry: entry[0])
        records = entries_to_records(sorted_entries)
        guards = {g for _, g, _ in records}
        guards_to_records = {g: [r for r in records if r[1] == g] for g in guards}
        guards_to_minutes = make_guards_to_minutes(guards_to_records)
        part1(guards_to_minutes)
        part2(guards_to_minutes)
