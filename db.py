import sqlite3
import bcrypt
import jwt
import datetime

# Secret key for encoding and decoding JWT tokens
SECRET_KEY = "peterjingles"


def connect_to_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(stored_password, provided_password):
    return bcrypt.checkpw(
        provided_password.encode("utf-8"), stored_password.encode("utf-8")
    )


def create_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(hours=2),  # Token expires in 2 hours
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def initial_setup():
    conn = connect_to_db()
    conn.execute("DROP TABLE IF EXISTS honeydews;")
    conn.execute("DROP TABLE IF EXISTS users;")
    conn.execute("DROP TABLE IF EXISTS categories;")

    conn.execute(
        """
        CREATE TABLE honeydews (
          id INTEGER PRIMARY KEY NOT NULL,
          name TEXT,
          completed INTEGER,
          deadline TEXT,
          description TEXT,
          priority INTEGER,
          category_id INTEGER,
          user_id INTEGER
        );
    """
    )

    conn.execute(
        """
        CREATE TABLE users (
          id INTEGER PRIMARY KEY NOT NULL,
          name TEXT,
          username TEXT,
          email TEXT,
          password_digest TEXT
        );
    """
    )

    conn.execute(
        """
        CREATE TABLE categories (
          id INTEGER PRIMARY KEY NOT NULL,
          name TEXT
        );
    """
    )

    conn.commit()
    print("Tables created successfully")

    honeydews_seed_data = [
        ("1st honeydew", 0, "01-01-2025", "First description", 1, 3, 1),
        ("2nd honeydew", 0, "01-01-2025", "Second description", 2, 2, 1),
        ("3rd honeydew", 0, "01-01-2025", "Third description", 3, 1, 1),
    ]
    users_seed_data = [
        ("test", "test13", "test@example.com", hash_password("password"))
    ]
    categories_seed_data = [
        ("category 1",),
        ("category 2",),
        ("category 3",),
    ]
    conn.executemany(
        """
        INSERT INTO honeydews (name, completed, deadline, description, priority, category_id, user_id)
        VALUES (?,?,?,?,?,?,?)
    """,
        honeydews_seed_data,
    )

    conn.executemany(
        """
        INSERT INTO users (name, username, email, password_digest)
        VALUES (?,?,?,?)
    """,
        users_seed_data,
    )

    conn.executemany(
        """
        INSERT INTO categories (name)
        VALUES (?)
    """,
        categories_seed_data,
    )

    conn.commit()
    print("Seed data created successfully")
    conn.close()


# Authentication-related functions
def login(username, password):
    conn = connect_to_db()
    user = conn.execute(
        """
        SELECT * FROM users WHERE username = ?
    """,
        (username,),
    ).fetchone()

    if user and check_password(user["password_digest"], password):
        token = create_jwt(user["id"])
        return {"token": token}
    else:
        return {"error": "Invalid credentials"}


# Protected Honeydew functions
def honeydews_create(
    name, completed, deadline, description, priority, category_id, token
):
    user_id = verify_jwt(token)
    if user_id:
        conn = connect_to_db()
        row = conn.execute(
            """
            INSERT INTO honeydews (name, completed, deadline, description, priority, category_id, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            RETURNING *
        """,
            (name, completed, deadline, description, priority, category_id, user_id),
        ).fetchone()
        conn.commit()
        return dict(row)
    else:
        return {"error": "Invalid or expired token"}


def honeydews_update_by_id(
    id, name, completed, deadline, description, priority, category_id, token
):
    user_id = verify_jwt(token)
    if user_id:
        conn = connect_to_db()
        row = conn.execute(
            """
            UPDATE honeydews SET name = ?, completed = ?, deadline = ?, description = ?, priority = ?, category_id = ?, user_id = ?
            WHERE id = ?
            RETURNING *
        """,
            (
                name,
                completed,
                deadline,
                description,
                priority,
                category_id,
                user_id,
                id,
            ),
        ).fetchone()
        conn.commit()
        return dict(row)
    else:
        return {"error": "Invalid or expired token"}


def honeydews_destroy_by_id(id, token):
    user_id = verify_jwt(token)
    if user_id:
        conn = connect_to_db()
        conn.execute(
            """
            DELETE from honeydews WHERE id = ?
        """,
            (id,),
        )
        conn.commit()
        return {"message": "Honeydew destroyed successfully"}
    else:
        return {"error": "Invalid or expired token"}


def honeydews_find_by_id(id, token):
    user_id = verify_jwt(token)
    if user_id:
        conn = connect_to_db()
        row = conn.execute(
            """
            SELECT * FROM honeydews WHERE id = ?
        """,
            (id,),
        ).fetchone()
        return dict(row)
    else:
        return {"error": "Invalid or expired token"}


def honeydews_all(token):
    user_id = verify_jwt(token)
    if user_id:
        conn = connect_to_db()
        rows = conn.execute(
            """
            SELECT * FROM honeydews
        """
        ).fetchall()
        return [dict(row) for row in rows]
    else:
        return {"error": "Invalid or expired token"}


# Protected Category functions
def categories_create(name, token):
    user_id = verify_jwt(token)
    if user_id:
        conn = connect_to_db()
        row = conn.execute(
            """
            INSERT INTO categories (name)
            VALUES (?)
            RETURNING *
        """,
            (name,),
        ).fetchone()
        conn.commit()
        return dict(row)
    else:
        return {"error": "Invalid or expired token"}


def categories_update_by_id(id, name, token):
    user_id = verify_jwt(token)
    if user_id:
        conn = connect_to_db()
        row = conn.execute(
            """
            UPDATE categories SET name = ?
            WHERE id = ?
            RETURNING *
        """,
            (name, id),
        ).fetchone()
        conn.commit()
        return dict(row)
    else:
        return {"error": "Invalid or expired token"}


def categories_destroy_by_id(id, token):
    user_id = verify_jwt(token)
    if user_id:
        conn = connect_to_db()
        conn.execute(
            """
            DELETE from categories WHERE id = ?
        """,
            (id,),
        )
        conn.commit()
        return {"message": "Category destroyed successfully"}
    else:
        return {"error": "Invalid or expired token"}


def categories_find_by_id(id, token):
    user_id = verify_jwt(token)
    if user_id:
        conn = connect_to_db()
        row = conn.execute(
            """
            SELECT * FROM categories WHERE id = ?
        """,
            (id,),
        ).fetchone()
        return dict(row)
    else:
        return {"error": "Invalid or expired token"}


def categories_all(token):
    user_id = verify_jwt(token)
    if user_id:
        conn = connect_to_db()
        rows = conn.execute(
            """
            SELECT * FROM categories
        """
        ).fetchall()
        return [dict(row) for row in rows]
    else:
        return {"error": "Invalid or expired token"}


if __name__ == "__main__":
    initial_setup()
