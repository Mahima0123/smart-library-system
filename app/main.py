from database.db import init_db
from services.book_service import BookService
from models.book import Book
from services.user_service import UserService
from services.transaction_service import TransactionService
from models.user import User
from services.analytics_service import AnalyticsService
from services.recommendation_service import RecommendationService
from services.visual_analytics_service import VisualAnalyticsService

def menu():
    print("\n=== Smart Library System ===")
    print("1. Add book")
    print("2. List books")
    print("3. Add user")
    print("4. List users")
    print("5. Issue book")
    print("6. Return book")
    print("7. View analytics dashboard")
    print("8. Get book recommendations")
    print("9. View analytics charts")
    print("10. Exit")


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
            name = input("Enter user name: ")
            user = User(name)
            UserService.add_user(user)
            print("User added successfully!")

        elif choice == "4":
            users = UserService.list_users()
            print("\n--- Users ---")
            for u in users:
                print(f"{u[0]} | {u[1]}")

        elif choice == "5":
            book_id = int(input("Enter book ID: "))
            user_id = int(input("Enter user ID: "))

            success = TransactionService.issue_book(book_id, user_id)
            if success:
                print("Book issued successfully!")
            else:
                print("Book is not available or invalid ID.")

        elif choice == "6":
            book_id = int(input("Enter book ID to return: "))
            TransactionService.return_book(book_id)
            print("Book returned successfully!")
        elif choice == "7":
            print("\n--- Analytics Dashboard ---")

            print("\nMost Borrowed Books:")
            for title, count in AnalyticsService.most_borrowed_books():
                print(f"{title} -> {count} times")

            print("\nTop Users:")
            for name, count in AnalyticsService.top_users():
                print(f"{name} -> {count} books")

            print("\nInactive Books:")
            inactive = AnalyticsService.inactive_books()
            if inactive:
                for bid, title in inactive:
                    print(f"{bid} | {title}")
            else:
                print("None")

            print("\nMonthly Borrowing Trends:")
            for month, total in AnalyticsService.monthly_trends():
                print(f"{month} -> {total}")

        elif choice == "8":
            book_id = int(input("Enter book ID: "))

            recs = RecommendationService.recommend_books(book_id)

            if not recs:
                print("No recommendations available yet.")
            else:
                print("\nRecommended Books:")
                for bid, title in recs:
                    print(f"{bid} | {title}")

        elif choice == "9":
            print("1. Top borrowed books chart")
            print("2. Monthly trend chart")

            sub = input("Choose: ")

            if sub == "1":
                VisualAnalyticsService.top_books_chart()
            elif sub == "2":
                VisualAnalyticsService.monthly_trend_chart()

        elif choice == "10":
            print("Goodbye!")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
