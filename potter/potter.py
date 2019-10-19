from collections import defaultdict

PC_DISCOUNTS = defaultdict(lambda: 0, {
  2: 5,
  3: 10,
  4: 20,
  5: 25
})

def filterDict(d, p):
  return {k: v for k, v in d.items() if p(k, v)}

def removeBooks(groupedBooks, setOfBooks):
  for book in setOfBooks:
    groupedBooks[book].pop()
  return filterDict(groupedBooks, lambda _, v: v)

def priceFor(setOfBooks):
  numBooks = len(setOfBooks)
  fullPrice = numBooks * 8
  pc_discount = PC_DISCOUNTS[numBooks]
  discount = fullPrice / 100 * pc_discount
  return fullPrice - discount

def chooseSetOfBooks(groupedBooks):
  lengths = [len(v) for v in groupedBooks.values()]
  lengths.sort()
  if lengths != [1, 1, 2, 2, 2]:
    return groupedBooks.keys()
  lengthOneItems = filterDict(groupedBooks, lambda _, v: len(v) == 1)
  lengthTwoItems = filterDict(groupedBooks, lambda _, v: len(v) == 2)
  lengthOneKeys = list(lengthOneItems.keys())
  lengthTwoKeys = list(lengthTwoItems.keys())
  return lengthOneKeys[:1] + lengthTwoKeys

def potter(books):
  groupedBooks = defaultdict(list)
  for book in books:
    groupedBooks[book].append(book)
  total = 0
  while groupedBooks:
    setOfBooks = chooseSetOfBooks(groupedBooks)
    total = total + priceFor(setOfBooks)
    groupedBooks = removeBooks(groupedBooks, setOfBooks)
  return total
