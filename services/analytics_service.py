from database.db import get_connection

class AnalyticsService:

    @staticmethod
    def most_borrowed_books(limit=5):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT b.title, COUNT(t.id) AS borrow_count
            FROM transactions t
            JOIN books b ON t.book_id = b.id
            GROUP BY b.title
            ORDER BY borrow_count DESC
            LIMIT %s;
        """, (limit,))

        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    @staticmethod
    def top_users(limit=5):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT u.name, COUNT(t.id) AS total_borrows
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            GROUP BY u.name
            ORDER BY total_borrows DESC
            LIMIT %s;
        """, (limit,))

        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    @staticmethod
    def inactive_books():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT b.id, b.title
            FROM books b
            LEFT JOIN transactions t ON b.id = t.book_id
            WHERE t.id IS NULL;
        """)

        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    @staticmethod
    def monthly_trends():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT TO_CHAR(issue_date, 'YYYY-MM') AS month,
                   COUNT(*) AS total_issues
            FROM transactions
            GROUP BY month
            ORDER BY month;
        """)

        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
