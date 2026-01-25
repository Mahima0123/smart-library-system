from database.db import get_connection
from models.user import User

class UserService:

    @staticmethod
    def add_user(user: User):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (name) VALUES (%s)",
            (user.name,)
        )

        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def list_users():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, name FROM users")
        users = cur.fetchall()

        cur.close()
        conn.close()

        return users
