from collections import defaultdict

PC_DISCOUNTS = defaultdict(lambda: 0, {
    2: 5,
    3: 10,
    4: 20,
    5: 25
})


def filter_dict(d, p):
    return {k: v for k, v in d.items() if p(k, v)}


def remove_books(grouped_books, set_of_books):
    for book in set_of_books:
        grouped_books[book].pop()
    return filter_dict(grouped_books, lambda _, v: v)


def price_for(set_of_books):
    num_books = len(set_of_books)
    full_price = num_books * 8
    pc_discount = PC_DISCOUNTS[num_books]
    discount = full_price / 100 * pc_discount
    return full_price - discount


def choose_books(grouped_books):
    lengths = [len(v) for v in grouped_books.values()]
    lengths.sort()
    if lengths != [1, 1, 2, 2, 2]:
        return grouped_books.keys()
    length_one_items = filter_dict(grouped_books, lambda _, v: len(v) == 1)
    length_two_items = filter_dict(grouped_books, lambda _, v: len(v) == 2)
    length_one_keys = list(length_one_items.keys())
    length_two_keys = list(length_two_items.keys())
    return length_one_keys[:1] + length_two_keys


def potter(books):
    grouped_books = defaultdict(list)
    for book in books:
        grouped_books[book].append(book)
    total = 0
    while grouped_books:
        set_of_books = choose_books(grouped_books)
        total = total + price_for(set_of_books)
        grouped_books = remove_books(grouped_books, set_of_books)
    return total
