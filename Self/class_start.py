class Book:
    #TODO: Properties defined at the class level are shared by all instances
    BOOK_TYPES = ("HARDCOVER","PAPERBACK","EBOOK")

    #TODO: double underscore properties are hidden from other classes

    __booklist = None

    #TODO: create a class method
    @classmethod
    def getbooktypes(cls):
        return cls.BOOK_TYPES
    #TODO: create a static method
    @staticmethod
    def getbooklist():
        if Book.__booklist == None:
            Book.__booklist  =[]
        return Book.__booklist
    #instance methods receive a specific object instance as an argument
    #and operate on data specific to that object instance

    def setTitle(self, newtitle):
        self.title = newtitle

    def __init__(self, title, booktype):
        self.title = title
        if(not booktype in Book.BOOK_TYPES):
            raise ValueError(f"{booktype} is not a valid book type")
        else:
            self.booktype = booktype

#todo: access the class attribute
print("Book types:", Book.getbooktypes())

#todo: create some book instances
b1 = Book("Title1", "HARDCOVER")
b2 = Book("Title2", "PAPERBACK")


thebooks = Book.getbooklist()
thebooks
