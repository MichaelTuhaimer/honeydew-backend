import sqlite3


def connect_to_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


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
    print("Table created successfully")

    honeydews_seed_data = [
        ("1st honeydew", 0, "01-01-2025", "First description", 1, 3, 1),
        ("2nd honeydew", 0, "01-01-2025", "Second description", 2, 2, 1),
        ("3rd honeydew", 0, "01-01-2025", "Third description", 3, 1, 1),
    ]
    users_seed_data = [("test", "test@example.com", "password")]
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
        INSERT INTO users (name, email, password_digest)
        VALUES (?,?,?)
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


def honeydews_create(name, completed, deadline, description, priority, category_id, user_id):
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
def honeydews_update_by_id(id, name, completed, deadline, description, priority, category_id, user_id):
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


def categories_create(name):
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
def categories_update_by_id(id, name):
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
def categories_destroy_by_id(id):
    conn = connect_to_db()
    row = conn.execute(
        """
        DELETE from categories
        WHERE id = ?
        """,
        (id),
    )
    conn.commit()
    return {"message": "Category destroyed successfully"}
def categories_find_by_id(id):
    conn = connect_to_db()
    row = conn.execute(
        """
        SELECT * FROM categories
        WHERE id = ?
        """,
        (id),
    ).fetchone()
    return dict(row)
def categories_all():
    conn = connect_to_db()
    rows = conn.execute(
        """
        SELECT * FROM categories
        """
    ).fetchall()
    return [dict(row) for row in rows]


if __name__ == "__main__":
    initial_setup()
