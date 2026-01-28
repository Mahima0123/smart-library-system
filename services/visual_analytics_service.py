import pandas as pd
import matplotlib.pyplot as plt
from database.db import get_connection

class VisualAnalyticsService:

    @staticmethod
    def top_books_chart():
        conn = get_connection()

        df = pd.read_sql("""
            SELECT b.title, COUNT(t.id) AS borrow_count
            FROM transactions t
            JOIN books b ON t.book_id = b.id
            GROUP BY b.title
            ORDER BY borrow_count DESC
            LIMIT 5;
        """, conn)

        conn.close()

        if df.empty:
            print("Not enough data to generate chart.")
            return

        plt.figure(figsize=(8, 5))
        plt.bar(df["title"], df["borrow_count"])
        plt.title("Top Borrowed Books")
        plt.xlabel("Book")
        plt.ylabel("Borrows")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def monthly_trend_chart():
        conn = get_connection()

        df = pd.read_sql("""
            SELECT TO_CHAR(issue_date, 'YYYY-MM') AS month,
                   COUNT(*) AS total
            FROM transactions
            GROUP BY month
            ORDER BY month;
        """, conn)

        conn.close()

        if df.empty:
            print("Not enough data to generate chart.")
            return

        plt.figure(figsize=(8, 5))
        plt.plot(df["month"], df["total"], marker='o')
        plt.title("Monthly Borrowing Trend")
        plt.xlabel("Month")
        plt.ylabel("Total Borrows")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
