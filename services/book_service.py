from database.db import get_connection
from models.book import Book

class BookService:

    @staticmethod
    def add_book(book: Book):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO books (title, author, available) VALUES (%s, %s, %s)",
            (book.title, book.author, book.available)
        )

        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def list_books():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, title, author, available FROM books")
        books = cur.fetchall()

        cur.close()
        conn.close()

        return books
