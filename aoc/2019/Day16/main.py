from collections import defaultdict


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


# def need(reactions_dict, totals, chemical, quantity):
#     if chemical == "ORE": return
#     totals[chemical] += quantity
#     reaction = reactions_dict[chemical]
#     for input_chemical in reaction.input_chemicals:
#         c = input_chemical.chemical
#         q = input_chemical.quantity
#         need(reactions_dict, totals, c, q * quantity)


# def apply_rounding(reactions_dict, totals):
#     for c, q in totals.items():
#         reaction = reactions_dict[c]
#         oq = reaction.output_chemical.quantity
#         totals[c] = ((q + oq - 1) // oq) * oq


# def expand_ores(reactions_dict, totals):
#     totals["ORE"] = 0
#     for c, q in totals.items():
#         if c == "ORE": continue
#         reaction = reactions_dict[c]
#         if len(reaction.input_chemicals) == 1:
#             ic = reaction.input_chemicals[0]
#             oc = reaction.output_chemical
#             if ic.chemical == "ORE":
#                 totals["ORE"] += (q // oc.quantity * ic.quantity)

def build_tree(reactions_dict, ores, root_node):
    for ic in root_node[1]:
        if ic.chemical == "ORE":
            ores.append(root_node[0])
        else:
            reaction = reactions_dict[ic.chemical]
            node = reaction.output_chemical, reaction.input_chemicals, []
            root_node[2].append(node)
            build_tree(reactions_dict, ores, node)


def part1(reactions):
    reactions_dict = {reaction.output_chemical.chemical: reaction for reaction in reactions}
    # totals = defaultdict(int)
    # need(reactions_dict, totals, "FUEL", 1)
    # apply_rounding(reactions_dict, totals)
    # expand_ores(reactions_dict, totals)
    # print(totals)
    ores = []
    reaction = reactions_dict["FUEL"]
    node = reaction.output_chemical, reaction.input_chemicals, []
    build_tree(reactions_dict, ores, node)
    for ore in ores:
        print(ore)
    # print(node)
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
    with open("aoc/2019/Day14/test3.txt") as f:
        lines = f.readlines()
        reactions = [parse_line(line) for line in lines]
        part1(reactions)
