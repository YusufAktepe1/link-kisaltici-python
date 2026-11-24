import pytest
from fastapi.testclient import TestClient

from app import codes, database, tracking
from app.main import app

IPHONE_SAFARI = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)
WINDOWS_CHROME = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Her test kendi geçici veritabanını kullanır; gerçek linkler.db'ye dokunulmaz
    monkeypatch.setattr(database, "DB_PATH", str(tmp_path / "test.db"))
    with TestClient(app) as c:
        yield c


def create_link(client, url="https://github.com/YusufAktepe1") -> str:
    client.post("/", data={"url": url})
    return database.recent_links()[0]["code"]


# --- Link kısaltma ve yönlendirme ---

def test_ana_sayfa_acilir(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "LinkKısaltıcı" in response.text


def test_gecersiz_link_reddedilir(client):
    response = client.post("/", data={"url": "merhaba"})
    assert response.status_code == 400
    assert "Geçerli bir link girin" in response.text


def test_link_kisaltilir_ve_yonlendirir(client):
    code = create_link(client)

    response = client.get(f"/{code}", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "https://github.com/YusufAktepe1"
    assert database.get_link(code)["click_count"] == 1


def test_olmayan_kod_404_doner(client):
    response = client.get("/yokyok")
    assert response.status_code == 404


def test_kod_uzunlugu_ve_karakterleri():
    code = codes.generate_code()
    assert len(code) == codes.LENGTH
    assert all(ch in codes.CHARS for ch in code)


# --- Tıklama kaydı ---

def test_tiklama_detaylari_kaydedilir(client):
    code = create_link(client)

    client.get(
        f"/{code}",
        headers={"User-Agent": IPHONE_SAFARI, "Referer": "https://www.instagram.com/p/abc"},
        follow_redirects=False,
    )

    click = database.click_stats(database.get_link(code)["id"])["last_clicks"][0]
    assert click["device"] == "Mobil"
    assert click["browser"] == "Mobile Safari"
    assert click["os"] == "iOS"
    assert click["referrer"] == "instagram.com"


def test_tiklamalar_gruplanir(client):
    code = create_link(client)
    for ua in (IPHONE_SAFARI, IPHONE_SAFARI, WINDOWS_CHROME):
        client.get(f"/{code}", headers={"User-Agent": ua}, follow_redirects=False)

    stats = database.click_stats(database.get_link(code)["id"])
    by_device = {row["label"]: row["total"] for row in stats["by_device"]}

    assert by_device == {"Mobil": 2, "Masaüstü": 1}
    assert stats["by_referrer"][0]["label"] == tracking.DIRECT


def test_tiklanmamis_link_sayisi_sifir(client):
    create_link(client)
    assert database.recent_links()[0]["click_count"] == 0


# --- İstatistik sayfası ---

def test_istatistik_sayfasi_acilir(client):
    code = create_link(client)
    client.get(f"/{code}", headers={"User-Agent": WINDOWS_CHROME}, follow_redirects=False)

    response = client.get(f"/stats/{code}")

    assert response.status_code == 200
    assert "Chrome" in response.text
    assert "Masaüstü" in response.text


def test_olmayan_linkin_istatistigi_404(client):
    assert client.get("/stats/yokyok").status_code == 404


# --- Yardımcı fonksiyonlar ---

@pytest.mark.parametrize(
    "referrer, expected",
    [
        ("https://www.google.com/search?q=test", "google.com"),
        ("https://t.co/xyz", "t.co"),
        ("", tracking.DIRECT),
        (None, tracking.DIRECT),
    ],
)
def test_referrer_ayristirma(referrer, expected):
    assert tracking.parse_referrer(referrer) == expected


def test_bos_user_agent_cokmez():
    device, browser, os = tracking.parse_user_agent("")
    assert browser == "Bilinmiyor"
