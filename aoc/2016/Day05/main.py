import hashlib

door_id = "reyedfim"


def calc_md5(number):
    arg = door_id + str(number)
    m = hashlib.md5()
    m.update(arg.encode())
    return m.hexdigest()


def find_next_00000(number):
    md5 = calc_md5(number)
    while md5[:5] != "00000":
        number = number + 1
        md5 = calc_md5(number)
    return md5, number


def part1():
    number = 0
    password = ""
    for _ in range(8):
        md5, number = find_next_00000(number)
        char = md5[5]
        print(f"number: {number}; md5: {md5}; char: {char}")
        password = password + char
        number = number + 1
    print(f"part 1 answer: {password}")


def part2():
    number = 0
    pos_char_map = dict()
    while len(pos_char_map) < 8:
        md5, number = find_next_00000(number)
        pos = int(md5[5], 16)
        if pos < 8 and pos not in pos_char_map:
            char = md5[6]
            print(f"number: {number}; md5: {md5}; pos: {pos}; char: {char}")
            pos_char_map[pos] = char
        number = number + 1
    password = "".join([pos_char_map[pos] for pos in sorted(pos_char_map)])
    print(f"part 2 answer: {password}")


if __name__ == "__main__":
    part1()
    part2()
