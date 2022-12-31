class Book:
    def __init__(self,title):
        self.title = title

class Newspaper:
    def __init__(self, name):
        self.name = name

#Create some instances of the classes
b1 = Book("The catcher of the rye")
b2 = Book("The Grapes of wrath")
n1 = Newspaper("The Washington Post")
n2 = Newspaper("The New York Times")

#TODO: use type() to inspect the object type
#
# print(type(b1))
# print(type(n1))

#TODO: Compare two types together

# print(type(b1) == type(b2))
# print(type (b1) == type(n2))

#TODO: use isinstance to compare a specific instance to a known type
print(isinstance(b1, Book))
print(isinstance(n1,Newspaper))
print(isinstance(n2,Book))
print(isinstance(n2, object))