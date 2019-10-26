from potter import price_books


class TestPotter:
    def test_zero_books(self):
        assert price_books('') == 0

    def test_one_book(self):
        assert price_books('A') == 8

    def test_two_books_same(self):
        assert price_books('AA') == 2 * 8

    def test_five_books_same(self):
        assert price_books('DDDDD') == 5 * 8

    def test_two_books_different(self):
        assert price_books('AB') == 2 * 8 * 0.95

    def test_three_books_different(self):
        assert price_books('ABC') == 3 * 8 * 0.9

    def test_four_books_different(self):
        assert price_books('ABCD') == 4 * 8 * 0.8

    def test_five_books_different(self):
        assert price_books('ABCDE') == 5 * 8 * 0.75

    def test_edge_case_1(self):
        assert price_books('ABCDEABC') == 2 * (4 * 8 * 0.8)

    def test_edge_case_2(self):
        assert price_books('ABCDEABCDEABCDEABCDEABC') == 3 * (5 * 8 * 0.75) + 2 * (4 * 8 * 0.8)
