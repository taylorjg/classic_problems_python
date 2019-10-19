from potter import potter

class TestPotter:
  def test_zero_books(self):
    assert potter('') == 0

  def test_one_book(self):
    assert potter('A') == 8

  def test_two_books_same(self):
    assert potter('AA') == 2 * 8

  def test_five_books_same(self):
    assert potter('DDDDD') == 5 * 8

  def test_two_books_different(self):
    assert potter('AB') == 2 * 8 * 0.95

  def test_three_books_different(self):
    assert potter('ABC') == 3 * 8 * 0.9

  def test_four_books_different(self):
    assert potter('ABCD') == 4 * 8 * 0.8

  def test_five_books_different(self):
    assert potter('ABCDE') == 5 * 8 * 0.75

  def test_two_fours_is_better_than_one_five_and_one_three(self):
    assert potter('ABCDEABC') == 2 * (4 * 8 * 0.8)
