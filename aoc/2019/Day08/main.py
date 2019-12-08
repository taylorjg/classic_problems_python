WIDTH = 25
HEIGHT = 6


def split_list_every(xs, n):
    num_layers = len(xs) // n
    for idx in range(num_layers):
        start_idx = idx * n
        end_idx = start_idx + n
        yield xs[start_idx:end_idx]


def part1(layers):
    v1 = [(layer.count(0), idx) for (idx, layer) in enumerate(layers)]
    v2 = sorted(v1, key=lambda t: t[0])
    layer_idx = v2[0][1]
    num_ones = layers[layer_idx].count(1)
    num_twos = layers[layer_idx].count(2)
    answer = num_ones * num_twos
    print(f"part 1 answer: {answer}")


def decode_image(layers):
    image = []
    for pixel_idx in range(WIDTH * HEIGHT):
        pixel = None
        for layer_idx in range(len(layers)):
            value = layers[layer_idx][pixel_idx]
            if value != 2:
                pixel = value
                break
        image.append(pixel)
    return image


def print_layer(layer):
    rows = split_list_every(layer, WIDTH)

    def interpret_pixel(pixel):
        return '.' if pixel == 1 else ' '

    for row in rows:
        print("".join([interpret_pixel(pixel) for pixel in row]))


def part2(layers):
    image = decode_image(layers)
    print_layer(image)


if __name__ == "__main__":
    with open("aoc/2019/Day08/input.txt") as f:
        line = f.read()
        digits = [int(c) for c in line.rstrip()]
        layers = list(split_list_every(digits, WIDTH * HEIGHT))
        part1(layers)
        part2(layers)
