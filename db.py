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
        CREATE TABLE honeydews (
          id INTEGER PRIMARY KEY NOT NULL,
          name TEXT,
          description TEXT,
          priority INTEGER
        );
        """
    )
    conn.commit()
    print("Table created successfully")

    honeydews_seed_data = [
        ("1st honeydew", "First description", 1),
        ("2nd honeydew", "Second description", 2),
        ("3rd honeydew", "Third description", 3),
    ]
    conn.executemany(
        """
        INSERT INTO honeydews (name, description, priority)
        VALUES (?,?,?)
        """,
        honeydews_seed_data,
    )
    conn.commit()
    print("Seed data created successfully")

    conn.close()


def honeydews_create(name, description, priority):
    conn = connect_to_db()
    row = conn.execute(
        """
        INSERT INTO honeydews (name, description, priority)
        VALUES (?, ?, ?)
        RETURNING *
        """,
        (name, description, priority),
    ).fetchone()
    conn.commit()
    return dict(row)


def honeydews_update_by_id(id, name, description, priority):
    conn = connect_to_db()
    row = conn.execute(
        """
        UPDATE honeydews SET name = ?, description = ?, priority = ?
        WHERE id = ?
        RETURNING *
        """,
        (name, description, priority, id),
    ).fetchone()
    conn.commit()
    return dict(row)


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
