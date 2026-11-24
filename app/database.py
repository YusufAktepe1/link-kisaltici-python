"""SQLite veritabanı işlemleri. Python'un kendi sqlite3 modülü kullanılır (ek paket yok)."""
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

# Veritabanı dosyası proje klasöründe durur (uygulama nereden çalıştırılırsa çalıştırılsın)
DB_PATH = str(Path(__file__).parent.parent / "linkler.db")

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"  # Sıralanabilir format (SQLite tarih fonksiyonları bunu anlar)


@contextmanager
def connect():
    """Bağlantı açar, iş bitince kaydeder (commit) ve kapatır."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # satırlara row["url"] şeklinde erişebilmek için
    conn.execute("PRAGMA foreign_keys = ON")  # SQLite'ta yabancı anahtar kontrolü varsayılan olarak kapalı
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
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                code       TEXT    NOT NULL UNIQUE,
                url        TEXT    NOT NULL,
                created_at TEXT    NOT NULL
            )
            """
        )
        # Her tıklama ayrı bir satır. link_id, links tablosundaki id'ye bağlanır (yabancı anahtar).
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS clicks (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                link_id    INTEGER NOT NULL REFERENCES links(id) ON DELETE CASCADE,
                clicked_at TEXT    NOT NULL,
                device     TEXT    NOT NULL,
                browser    TEXT    NOT NULL,
                os         TEXT    NOT NULL,
                referrer   TEXT    NOT NULL
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_clicks_link_id ON clicks(link_id)")


def add_link(code: str, url: str) -> None:
    with connect() as conn:
        # "?" yer tutucuları SQL injection saldırısını önler
        conn.execute(
            "INSERT INTO links (code, url, created_at) VALUES (?, ?, ?)",
            (code, url, datetime.now().strftime(DATE_FORMAT)),
        )


def code_exists(code: str) -> bool:
    with connect() as conn:
        row = conn.execute("SELECT 1 FROM links WHERE code = ?", (code,)).fetchone()
        return row is not None


def register_click(code: str, device: str, browser: str, os: str, referrer: str) -> str | None:
    """Tıklamayı kaydeder ve asıl adresi döndürür. Kod yoksa None döner."""
    with connect() as conn:
        link = conn.execute("SELECT id, url FROM links WHERE code = ?", (code,)).fetchone()
        if link is None:
            return None
        conn.execute(
            """
            INSERT INTO clicks (link_id, clicked_at, device, browser, os, referrer)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (link["id"], datetime.now().strftime(DATE_FORMAT), device, browser, os, referrer),
        )
        return link["url"]


# Bir linki tıklama sayısıyla birlikte getiren ortak sorgu parçası.
# LEFT JOIN: hiç tıklanmamış linkler de gelsin (sayısı 0 olur).
_LINKS_WITH_COUNT = """
    SELECT l.id, l.code, l.url, l.created_at, COUNT(c.id) AS click_count
    FROM links AS l
    LEFT JOIN clicks AS c ON c.link_id = l.id
"""


def recent_links(limit: int = 10) -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute(
            _LINKS_WITH_COUNT + " GROUP BY l.id ORDER BY l.id DESC LIMIT ?",
            (limit,),
        ).fetchall()


def get_link(code: str) -> sqlite3.Row | None:
    with connect() as conn:
        return conn.execute(
            _LINKS_WITH_COUNT + " WHERE l.code = ? GROUP BY l.id",
            (code,),
        ).fetchone()


def _count_by(conn: sqlite3.Connection, column: str, link_id: int) -> list[sqlite3.Row]:
    # column değeri sadece aşağıdaki sabit listeden gelir; kullanıcı girdisi değildir.
    assert column in ("device", "browser", "os", "referrer")
    return conn.execute(
        f"""
        SELECT {column} AS label, COUNT(*) AS total
        FROM clicks
        WHERE link_id = ?
        GROUP BY {column}
        ORDER BY total DESC
        """,
        (link_id,),
    ).fetchall()


def click_stats(link_id: int) -> dict:
    """Bir linkin tüm istatistiklerini tek seferde toplar."""
    with connect() as conn:
        return {
            "by_device": _count_by(conn, "device", link_id),
            "by_browser": _count_by(conn, "browser", link_id),
            "by_os": _count_by(conn, "os", link_id),
            "by_referrer": _count_by(conn, "referrer", link_id),
            "by_day": conn.execute(
                """
                SELECT date(clicked_at) AS day, COUNT(*) AS total
                FROM clicks
                WHERE link_id = ?
                GROUP BY day
                ORDER BY day DESC
                LIMIT 14
                """,
                (link_id,),
            ).fetchall(),
            "last_clicks": conn.execute(
                """
                SELECT clicked_at, device, browser, os, referrer
                FROM clicks
                WHERE link_id = ?
                ORDER BY id DESC
                LIMIT 10
                """,
                (link_id,),
            ).fetchall(),
        }
