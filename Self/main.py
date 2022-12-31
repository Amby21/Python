# TODO: create a basic class

class Book:
    def __init__(self, title, author, pages, price):
        self.title = title
        self.author = author
        self.pages = pages
        self.price = price
        self.__secret = "this is a secret attribute"

#TODO: create instance methods

    def getPrice(self):
        if hasattr(self,"_discount"):
            return self.price - (self.price * self._discount)
        else:
            return self.price

    def setdiscount(self, amount):
        self._discount = amount

#TODO: Create some book instances

b1 = Book("War and Peace", "Leo TolStoy", 1225, 39.95)
b2 = Book("the catcher in the rye","JD salinger", 234, 29.95)

#TODO: print the class and property
print(b1.getPrice())

print(b2.getPrice())
b2.setdiscount(0.25)
print(b2.getPrice())
print(b2._Book__secret)