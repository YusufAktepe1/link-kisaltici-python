import pytest
from fastapi.testclient import TestClient

from app import codes, database
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Her test kendi geçici veritabanını kullanır; gerçek linkler.db'ye dokunulmaz
    monkeypatch.setattr(database, "DB_PATH", str(tmp_path / "test.db"))
    with TestClient(app) as c:
        yield c


def test_ana_sayfa_acilir(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "LinkKısaltıcı" in response.text


def test_gecersiz_link_reddedilir(client):
    response = client.post("/", data={"url": "merhaba"})
    assert response.status_code == 400
    assert "Geçerli bir link girin" in response.text


def test_link_kisaltilir_ve_yonlendirir(client):
    client.post("/", data={"url": "https://github.com/YusufAktepe1"})
    code = database.recent_links()[0]["code"]

    response = client.get(f"/{code}", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "https://github.com/YusufAktepe1"
    assert database.recent_links()[0]["click_count"] == 1


def test_olmayan_kod_404_doner(client):
    response = client.get("/yokyok")
    assert response.status_code == 404


def test_kod_uzunlugu_ve_karakterleri():
    code = codes.generate_code()
    assert len(code) == codes.LENGTH
    assert all(ch in codes.CHARS for ch in code)
