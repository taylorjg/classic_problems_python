from collections import defaultdict

PC_DISCOUNTS = defaultdict(lambda: 0, {
  2: 5,
  3: 10,
  4: 20,
  5: 25
})

def removeEmptyValues(groupedBooksOld):
  groupedBooksNew = dict()
  for (k, v) in groupedBooksOld.items():
    if v: groupedBooksNew[k] = v
  return groupedBooksNew

def removeBooks(groupedBooks, setOfBooks):
  for book in setOfBooks:
    groupedBooks[book] = groupedBooks[book][1:]
  return removeEmptyValues(groupedBooks)

def calcPrice(setOfBooks):
  numBooks = len(setOfBooks)
  fullPrice = numBooks * 8
  pc_discount = PC_DISCOUNTS[numBooks]
  discount = fullPrice / 100 * pc_discount
  return fullPrice - discount

# A: [A, A]
# B: [B, B]
# C: [C, C]
# D: [D]
# E: [E]

def potter(books):
  groupedBooks = defaultdict(list)
  for book in books:
    groupedBooks[book].append(book)
  total = 0
  while groupedBooks:
    setOfBooks = groupedBooks.keys()
    total = total + calcPrice(setOfBooks)
    groupedBooks = removeBooks(groupedBooks, setOfBooks)
    # if len group is < 5 then remove set of books adding discounted price to total
    # if there are 2 groups of 4 available then remove a set of 4 else remove a set of 5
    #    (the set of 4 that is removed needs to include the 3 items with values of length >= 3)
    # to check for 2 groups of 4 available:
    #   we know there is a group of 5 due to earlier check
    #   for there to be 2 groups of 4, there needs to be 3 items with values of length >= 2
  return total
