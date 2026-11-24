# 🔗 LinkKısaltıcı (Python)

Uzun linkleri kısa, paylaşılabilir linklere dönüştüren ve her tıklamanın hangi cihazdan, hangi tarayıcıdan ve hangi siteden geldiğini takip eden bir web uygulaması.

## Özellikler

- **Link kısaltma:** Uzun bir adresi `http://localhost:8000/aB3xYz` gibi 6 karakterlik kısa bir linke dönüştürür.
- **Yönlendirme:** Kısa linke tıklayan ziyaretçi asıl adrese yönlendirilir.
- **Ayrıntılı tıklama kaydı:** Her tıklamanın zamanı, cihaz türü (mobil/masaüstü/tablet), tarayıcısı, işletim sistemi ve geldiği site (Instagram, Google vb.) kaydedilir.
- **İstatistik sayfası:** Her link için toplam tıklama, cihaz / tarayıcı / işletim sistemi / kaynak site dağılımı (yüzdeli çubuklarla), günlük tıklama sayısı ve son tıklamalar listesi.
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
| **SQLite** (`sqlite3`) | Link ve tıklama verilerinin saklandığı veritabanı (JOIN, GROUP BY, yabancı anahtar) |
| **user-agents** | Tarayıcı bilgisinden cihaz, tarayıcı ve işletim sistemini çıkarma |
| **Jinja2** | HTML şablonları (şablon kalıtımı ve makrolar) |
| **Bootstrap 5** | Sayfa tasarımı |
| **pytest** | Otomatik testler |

Tüm teknolojiler açık kaynak ve ücretsizdir. Uygulama hiçbir harici servise veya API'ye bağlanmaz; tüm veriler yerel veritabanında tutulur.

## Veritabanı Yapısı

```
links                         clicks
─────────────                 ──────────────────
id          (PK)  ◄────────┐  id          (PK)
code        (UNIQUE)       └─ link_id     (FK → links.id)
url                           clicked_at
created_at                    device, browser, os
                              referrer
```

Bir linkin birden çok tıklaması olabilir (bire-çok ilişki). Tıklama sayıları `LEFT JOIN` + `COUNT` + `GROUP BY` ile hesaplanır.

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
│   ├── main.py          # Web sayfaları, form işleme, yönlendirme ve istatistik sayfası
│   ├── database.py      # SQLite tabloları ve SQL sorguları
│   ├── tracking.py      # Cihaz, tarayıcı ve kaynak site tespiti
│   ├── codes.py         # Benzersiz kısa kod üretimi
│   └── templates/
│       ├── base.html    # Ortak sayfa iskeleti
│       ├── index.html   # Ana sayfa
│       └── stats.html   # İstatistik sayfası
├── tests/
│   └── test_app.py      # Otomatik testler
├── run.py               # Uygulamayı başlatan dosya
└── requirements.txt     # Gerekli Python paketleri
```

## Yol Haritası

- [x] Tıklama detayları (tarih, cihaz, tarayıcı, yönlendiren site)
- [x] İstatistik sayfası
- [ ] Grafikli istatistik paneli
- [ ] QR kod üretme
- [ ] UTM parametresi ekleme
- [ ] Kullanıcı girişi
- [ ] Canlıya yayınlama

## Geliştirici

**Yusuf Aktepe** · [GitHub](https://github.com/YusufAktepe1) · [LinkedIn](https://www.linkedin.com/in/yusuf-aktepe-20935a325)
