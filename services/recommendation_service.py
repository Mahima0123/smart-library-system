from database.db import get_connection
from collections import defaultdict

class RecommendationService:

    @staticmethod
    def recommend_books(book_id: int, limit=5):
        conn = get_connection()
        cur = conn.cursor()

        # Get all users who borrowed this book
        cur.execute("""
            SELECT DISTINCT user_id
            FROM transactions
            WHERE book_id = %s
        """, (book_id,))
        users = [row[0] for row in cur.fetchall()]

        if not users:
            cur.close()
            conn.close()
            return []

        # Get other books those users borrowed
        cur.execute("""
            SELECT book_id
            FROM transactions
            WHERE user_id = ANY(%s) AND book_id != %s
        """, (users, book_id))

        books = [row[0] for row in cur.fetchall()]

        # Count frequency
        freq = defaultdict(int)
        for b in books:
            freq[b] += 1

        if not freq:
            cur.close()
            conn.close()
            return []

        # Sort by frequency
        sorted_books = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:limit]
        book_ids = [b[0] for b in sorted_books]

        # Get titles
        cur.execute("""
            SELECT id, title FROM books WHERE id = ANY(%s)
        """, (book_ids,))

        results = cur.fetchall()

        cur.close()
        conn.close()

        return results
