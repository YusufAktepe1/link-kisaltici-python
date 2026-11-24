"""SQLite veritabanı işlemleri. Python'un kendi sqlite3 modülü kullanılır (ek paket yok)."""
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

# Veritabanı dosyası proje klasöründe durur (uygulama nereden çalıştırılırsa çalıştırılsın)
DB_PATH = str(Path(__file__).parent.parent / "linkler.db")


@contextmanager
def connect():
    """Bağlantı açar, iş bitince kaydeder (commit) ve kapatır."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # satırlara row["url"] şeklinde erişebilmek için
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS links (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                code        TEXT    NOT NULL UNIQUE,
                url         TEXT    NOT NULL,
                click_count INTEGER NOT NULL DEFAULT 0,
                created_at  TEXT    NOT NULL
            )
            """
        )


def add_link(code: str, url: str) -> None:
    with connect() as conn:
        # "?" yer tutucuları SQL injection saldırısını önler
        conn.execute(
            "INSERT INTO links (code, url, created_at) VALUES (?, ?, ?)",
            (code, url, datetime.now().strftime("%d.%m.%Y %H:%M")),
        )


def code_exists(code: str) -> bool:
    with connect() as conn:
        row = conn.execute("SELECT 1 FROM links WHERE code = ?", (code,)).fetchone()
        return row is not None


def register_click(code: str) -> str | None:
    """Tıklama sayısını 1 artırır ve asıl adresi döndürür. Kod yoksa None döner."""
    with connect() as conn:
        conn.execute("UPDATE links SET click_count = click_count + 1 WHERE code = ?", (code,))
        row = conn.execute("SELECT url FROM links WHERE code = ?", (code,)).fetchone()
        return row["url"] if row else None


def recent_links(limit: int = 10) -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute(
            "SELECT code, url, click_count, created_at FROM links ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
