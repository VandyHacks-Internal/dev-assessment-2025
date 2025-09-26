import sqlite3
from contextlib import contextmanager
from typing import Iterator, Optional, Tuple, List

DB_PATH = "swagtrackr.db"

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    quantity INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS checkouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    recipient TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
);

CREATE TRIGGER IF NOT EXISTS trg_items_updated_at
AFTER UPDATE ON items
FOR EACH ROW
BEGIN
  UPDATE items SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;
"""


def initialize_database(db_path: str = DB_PATH) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.executescript(SCHEMA_SQL)
        conn.commit()


@contextmanager
def get_connection(db_path: str = DB_PATH) -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(db_path)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def get_item_by_name(conn: sqlite3.Connection, name: str) -> Optional[Tuple[int, str, int]]:
    cur = conn.execute("SELECT id, name, quantity FROM items WHERE name = ?", (name,))
    return cur.fetchone()


def create_or_update_item(conn: sqlite3.Connection, name: str, quantity_delta: int) -> Tuple[int, int]:
    row = get_item_by_name(conn, name)
    if row is None:
        conn.execute("INSERT INTO items(name, quantity) VALUES(?, ?)", (name, max(0, quantity_delta)))
        cur = conn.execute("SELECT id, quantity FROM items WHERE name = ?", (name,))
        item_id, qty = cur.fetchone()
        return item_id, qty
    item_id, _name, qty = row
    new_qty = max(0, qty + quantity_delta)
    conn.execute("UPDATE items SET quantity = ? WHERE id = ?", (new_qty, item_id))
    return item_id, new_qty


def set_item_quantity(conn: sqlite3.Connection, name: str, quantity: int) -> Tuple[int, int]:
    row = get_item_by_name(conn, name)
    if row is None:
        conn.execute("INSERT INTO items(name, quantity) VALUES(?, ?)", (name, max(0, quantity)))
        cur = conn.execute("SELECT id, quantity FROM items WHERE name = ?", (name,))
        item_id, qty = cur.fetchone()
        return item_id, qty
    item_id, _name, _qty = row
    new_qty = max(0, quantity)
    conn.execute("UPDATE items SET quantity = ? WHERE id = ?", (new_qty, item_id))
    return item_id, new_qty


def list_items(conn: sqlite3.Connection) -> List[Tuple[int, str, int]]:
    cur = conn.execute("SELECT id, name, quantity FROM items ORDER BY name ASC")
    return cur.fetchall()


def delete_item(conn: sqlite3.Connection, name: str) -> bool:
    row = get_item_by_name(conn, name)
    if row is None:
        return False
    item_id, _name, _qty = row
    conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    return True


def checkout_item(conn: sqlite3.Connection, name: str, amount: int, recipient: Optional[str]) -> Tuple[int, int]:
    if amount <= 0:
        raise ValueError("Amount must be positive")
    row = get_item_by_name(conn, name)
    if row is None:
        raise ValueError("Item not found")
    item_id, _name, qty = row
    if qty < amount:
        raise ValueError("Insufficient stock")
    new_qty = qty - amount
    conn.execute("UPDATE items SET quantity = ? WHERE id = ?", (new_qty, item_id))
    conn.execute(
        "INSERT INTO checkouts(item_id, amount, recipient) VALUES(?, ?, ?)",
        (item_id, amount, recipient),
    )
    return item_id, new_qty
