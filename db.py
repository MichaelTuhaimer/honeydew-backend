import sqlite3
import bcrypt


def connect_to_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def initial_setup():
    conn = connect_to_db()
    conn.execute(
        """
        DROP TABLE IF EXISTS honeydews;
        """
    )
    conn.execute(
        """
        DROP TABLE IF EXISTS users;
        """
    )
    conn.execute(
        """
        DROP TABLE IF EXISTS categories;
        """
    )
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


def honeydews_create(
    name, completed, deadline, description, priority, category_id, user_id
):
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


def honeydews_update_by_id(
    id, name, completed, deadline, description, priority, category_id, user_id
):
    conn = connect_to_db()
    row = conn.execute(
        """
        UPDATE honeydews SET name = ?, completed = ?, deadline = ?, description = ?, priority = ?, category_id = ?, user_id = ?
        WHERE id = ?
        RETURNING *
        """,
        (name, completed, deadline, description, priority, category_id, user_id, id),
    ).fetchone()
    conn.commit()
    return dict(row)


def honeydews_destroy_by_id(id):
    conn = connect_to_db()
    row = conn.execute(
        """
        DELETE from honeydews
        WHERE id = ?
        """,
        (id,),
    )
    conn.commit()
    return {"message": "Honeydew destroyed successfully"}


def honeydews_find_by_id(id):
    conn = connect_to_db()
    row = conn.execute(
        """
        SELECT * FROM honeydews
        WHERE id = ?
        """,
        (id,),
    ).fetchone()
    return dict(row)


def honeydews_all():
    conn = connect_to_db()
    rows = conn.execute(
        """
        SELECT * FROM honeydews
        """
    ).fetchall()
    return [dict(row) for row in rows]


if __name__ == "__main__":
    initial_setup()
