class ChemicalQuantity:
    def __init__(self, chemical, quantity):
        self.chemical = chemical
        self.quantity = quantity

    def __str__(self):
        return f"{self.quantity} {self.chemical}"


class Reaction:
    def __init__(self, input_chemicals, output_chemical):
        self.input_chemicals = input_chemicals
        self.output_chemical = output_chemical

    def __str__(self):
        ics = [str(ic) for ic in self.input_chemicals]
        return f"{', '.join(ics)} => {self.output_chemical}"


def part1(reactions):
    for reaction in reactions:
        print(reaction)
    print(f"part 1 answer: {0}")


def parse_chemical_quantity(s):
    [q, c] = s.strip().split(" ")
    return ChemicalQuantity(c, int(q))


def parse_line(line):
    [left_str, out_str] = line.split("=>")
    in_strs = left_str.split(",")
    input_chemicals = [parse_chemical_quantity(in_str) for in_str in in_strs]
    output_chemical = parse_chemical_quantity(out_str)
    return Reaction(input_chemicals, output_chemical)


if __name__ == "__main__":
    with open("aoc/2019/Day14/input.txt") as f:
        lines = f.readlines()
        reactions = [parse_line(line) for line in lines]
        part1(reactions)
