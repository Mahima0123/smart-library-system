from database.db import init_db
from services.book_service import BookService
from models.book import Book

def menu():
    print("\n=== Smart Library System ===")
    print("1. Add book")
    print("2. List books")
    print("3. Exit")

def main():
    init_db()

    while True:
        menu()
        choice = input("Choose option: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author: ")

            book = Book(title, author)
            BookService.add_book(book)

            print("Book added successfully!")

        elif choice == "2":
            books = BookService.list_books()

            print("\n--- Books in Library ---")
            for b in books:
                status = "Available" if b[3] else "Issued"
                print(f"{b[0]} | {b[1]} | {b[2]} | {status}")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
