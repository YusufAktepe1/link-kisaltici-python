# 🔗 LinkKısaltıcı (Python)

Uzun linkleri kısa, paylaşılabilir linklere dönüştüren ve her linkin kaç kez tıklandığını takip eden bir web uygulaması.

## Özellikler

- **Link kısaltma:** Uzun bir adresi `http://localhost:8000/aB3xYz` gibi 6 karakterlik kısa bir linke dönüştürür.
- **Yönlendirme:** Kısa linke tıklayan ziyaretçi asıl adrese yönlendirilir.
- **Tıklama sayacı:** Her kısa linkin kaç kez tıklandığı kaydedilir.
- **Son linkler tablosu:** Oluşturulan son 10 link, tıklama sayıları ve tarihleriyle listelenir.
- **Link doğrulama:** Geçersiz adresler (`http://` veya `https://` ile başlamayanlar) reddedilir.
- **Tek tıkla kopyalama:** Oluşturulan kısa link tek tuşla panoya kopyalanır.
- **Okunaklı kodlar:** Karıştırılabilen karakterler (`0/O`, `1/l/I`) kısa kodlarda kullanılmaz.

## Kullanılan Teknolojiler

| Teknoloji | Kullanım amacı |
|---|---|
| **Python 3.11+** | Programlama dili |
| **FastAPI** | Web çatısı (sayfalar, form ve yönlendirme) |
| **Uvicorn** | Uygulamayı çalıştıran web sunucusu |
| **SQLite** (`sqlite3`) | Linklerin saklandığı veritabanı |
| **Jinja2** | HTML şablonları |
| **Bootstrap 5** | Sayfa tasarımı |
| **pytest** | Otomatik testler |

Tüm teknolojiler açık kaynak ve ücretsizdir.

## Kurulum ve Çalıştırma

> Gereksinim: Bilgisayarınızda [Python 3.11 veya üstü](https://www.python.org/downloads/) kurulu olmalı.

**1. Projeyi indirin ve klasörüne girin**

```powershell
git clone https://github.com/YusufAktepe1/link-kisaltici-python.git
cd link-kisaltici-python
```

**2. Sanal ortam oluşturun ve paketleri kurun**

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**3. Uygulamayı başlatın**

```powershell
.\.venv\Scripts\python.exe run.py
```

> VS Code kullanıyorsanız: sağ alttan Python yorumlayıcısı olarak `.venv` ortamını seçin, ardından `run.py` dosyasını açıp ▶ **Run** butonuna basın.

**4. Tarayıcıda açın:** http://localhost:8000

Veritabanı dosyası (`linkler.db`) ilk çalıştırmada otomatik oluşturulur.

## Testleri Çalıştırma

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Testler her seferinde geçici bir veritabanı kullanır; gerçek verilerinize dokunmaz.

## Proje Yapısı

```
LinkKisaltici-Py/
├── app/
│   ├── main.py          # Web sayfaları, form işleme ve yönlendirme
│   ├── database.py      # SQLite tablosu ve SQL sorguları
│   ├── codes.py         # Benzersiz kısa kod üretimi
│   └── templates/
│       └── index.html   # Ana sayfa tasarımı
├── tests/
│   └── test_app.py      # Otomatik testler
├── run.py               # Uygulamayı başlatan dosya
└── requirements.txt     # Gerekli Python paketleri
```

## Yol Haritası

- [ ] Tıklama detayları (tarih, cihaz, tarayıcı, yönlendiren site)
- [ ] Grafikli istatistik paneli
- [ ] QR kod üretme
- [ ] UTM parametresi ekleme
- [ ] Kullanıcı girişi
- [ ] Canlıya yayınlama

## Geliştirici

**Yusuf Aktepe** · [GitHub](https://github.com/YusufAktepe1) · [LinkedIn](https://www.linkedin.com/in/yusuf-aktepe-20935a325)
