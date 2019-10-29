import hashlib
import itertools

secret_key = "bgvyzdsv"


def calc_md5(number):
    arg = secret_key + str(number)
    m = hashlib.md5()
    m.update(arg.encode())
    return m.hexdigest()


def mint_coin(part, prefix_len):
    prefix = "0" * prefix_len
    for number in itertools.count(1):
        if calc_md5(number).startswith(prefix):
            print(f"part {part} answer: {number}")
            break


if __name__ == "__main__":
    mint_coin(1, 5)
    mint_coin(2, 6)
