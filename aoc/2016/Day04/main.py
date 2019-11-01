from itertools import groupby
from operator import itemgetter
import re


def find_real_rooms(lines):
    real_rooms = []
    for line in lines:
        result = re.match(r"^(.*)-(\d+)\[(.*)\]", line)
        name, sector_id, expected_checksum = result.group(1, 2, 3)
        letters = sorted(name.replace('-', ''))
        grouped_1 = groupby(letters)
        grouped_2 = [(k, -len(list(v))) for k, v in grouped_1]
        grouped_3 = sorted(grouped_2, key=itemgetter(1, 0))
        grouped_4 = [k for k, _ in grouped_3[:5]]
        calculated_checksum = ''.join(grouped_4)
        if calculated_checksum == expected_checksum:
            room = name, int(sector_id)
            real_rooms.append(room)
    return real_rooms


def part1(lines):
    real_rooms = find_real_rooms(lines)
    total = sum([sector_id for _, sector_id in real_rooms])
    print(f"part 1 answer: {total}")


def decrypt_room_name(room):
    encrypted_name, sector_id = room
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    cipher = {letter: alphabet[(index + sector_id) % 26] for index, letter in enumerate(alphabet)}
    cipher["-"] = " "
    decrypted_name = "".join([cipher[letter] for letter in encrypted_name])
    return decrypted_name


def part2(lines):
    real_rooms = find_real_rooms(lines)
    decrypted_room_names = [decrypt_room_name(real_room) for real_room in real_rooms]
    desired_room = next(filter(lambda name: "north" in name, decrypted_room_names))
    desired_room_index = decrypted_room_names.index(desired_room)
    _, desired_sector_id = real_rooms[desired_room_index]
    print(f"part 2 answer: {desired_sector_id}")


if __name__ == "__main__":
    with open("aoc/2016/Day04/input.txt") as f:
        lines = f.readlines()
        part1(lines)
        part2(lines)
