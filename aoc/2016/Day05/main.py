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


def find_password(fn):
    number = 0
    chars = list("????????")
    index = 0
    while chars.count("?") > 0:
        md5, number = find_next_00000(number)
        char, pos = fn(md5, index)
        print(md5, number, char, pos)
        if pos is not None and chars[pos] == "?":
            chars[pos] = char
            index = index + 1
        number = number + 1
    return "".join(chars)


def part1():
    def fn(md5, index):
        return md5[5], index

    password = find_password(fn)
    print(f"part 1 answer: {password}")


def part2():
    def fn(md5, _):
        pos = int(md5[5], 16)
        char = md5[6]
        if pos < 8:
            return char, pos
        else:
            return char, None

    password = find_password(fn)
    print(f"part 2 answer: {password}")


if __name__ == "__main__":
    part1()
    part2()
