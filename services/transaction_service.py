from datetime import datetime
from database.db import get_connection

class TransactionService:

    @staticmethod
    def issue_book(book_id: int, user_id: int):
        conn = get_connection()
        cur = conn.cursor()

        # Check availability
        cur.execute("SELECT available FROM books WHERE id = %s", (book_id,))
        result = cur.fetchone()

        if not result or not result[0]:
            cur.close()
            conn.close()
            return False

        # Insert transaction
        cur.execute("""
            INSERT INTO transactions (book_id, user_id, issue_date)
            VALUES (%s, %s, %s)
        """, (book_id, user_id, datetime.now()))

        # Mark book as unavailable
        cur.execute("UPDATE books SET available = FALSE WHERE id = %s", (book_id,))

        conn.commit()
        cur.close()
        conn.close()
        return True

    @staticmethod
    def return_book(book_id: int):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE transactions
            SET return_date = %s
            WHERE book_id = %s AND return_date IS NULL
        """, (datetime.now(), book_id))

        cur.execute("UPDATE books SET available = TRUE WHERE id = %s", (book_id,))

        conn.commit()
        cur.close()
        conn.close()
