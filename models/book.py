class Book:
    def __init__(self, title: str, author: str, available: bool = True):
        self.title = title
        self.author = author
        self.available = available
