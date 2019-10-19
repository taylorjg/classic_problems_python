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

def priceFor(setOfBooks):
  numBooks = len(setOfBooks)
  fullPrice = numBooks * 8
  pc_discount = PC_DISCOUNTS[numBooks]
  discount = fullPrice / 100 * pc_discount
  return fullPrice - discount

def filterDict(d, pred):
  newDict = dict()
  for (k, v) in d.items():
    if pred(k, v):
      newDict[k] = v
  return newDict

def chooseSetOfBooks(groupedBooks):
  if len(groupedBooks) < 5:
    return groupedBooks.keys()
  else:
    items1 = filterDict(groupedBooks, lambda _, v: len(v) >= 2)
    keys1 = list(items1.keys())[:3]
    if len(keys1) < 3:
      return groupedBooks.keys()
    else:
      items2 = filterDict(groupedBooks, lambda k, _: not k in keys1)
      keys2 = items2.keys()
      return keys1 + list(keys2)[:1]

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
