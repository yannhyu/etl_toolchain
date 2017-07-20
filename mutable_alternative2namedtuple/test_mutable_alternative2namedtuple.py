from recordtype import recordtype

Book = recordtype('Book', 'author title genre year price instock')
books = [
   Book('Suzane Collins','The Hunger Games', 'Fiction', 2008, 6.96, 20),
   Book('J.K. Rowling', "Harry Potter and the Sorcerer's Stone", 'Fantasy', 1997, 4.78, 12)]

for book in books:
    print('Price changed from {}'.format(book.price))
    book.price *= 1.1
    print('... to {}'.format(book.price))