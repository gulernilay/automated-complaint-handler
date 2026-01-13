# Müşteri Şikayetleri Yönetim Sistemi

Bu proje, bir müşteri şikayetleri yönetim sistemidir. Excel dosyasındaki değişiklikleri izler, yeni şikayetleri veritabanına ekler ve ilgili kişilere e-posta gönderir.

## Özellikler

- **Excel İzleme**: Belirtilen klasördeki Excel dosyasındaki değişiklikleri gerçek zamanlı olarak izler.
- **Veri İşleme**: Excel verilerini ön işler ve veritabanına güvenli bir şekilde ekler.
- **E-posta Bildirimi**: Yeni şikayetler için otomatik e-posta gönderir.
- **Günlük Tutma**: Tüm işlemleri detaylı bir şekilde loglar.
- **Çiftleme Önleme**: Aynı verilerin tekrar eklenmesini önler (RowHash tabanlı).

## Gereksinimler

- Python 3.11+
- SQL Server veritabanı
- Gerekli Python paketleri: [`requirements.txt`](requirements.txt) dosyasında listelenmiştir.

## Kurulum

1. **Depoyu Klonlayın**:

   ```bash
   git clone <repo-url>
   cd Müşteri_Şikayetleri
   ```

2. **Sanal Ortam Oluşturun** (İsteğe bağlı ama önerilir):

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Bağımlılıkları Yükleyin**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Ortam Değişkenlerini Ayarlayın**:
   [`.env`](.env) dosyasını düzenleyin. Örnek:

   ```
   WATCH_FOLDER=\\192.168.2.212\ofisdata\KALITE GUVENCE\yapay zeka
   EXCEL_FILE=FR 05 Müşteri Geri Bildirimleri Takip Formu.xlsx
   TARGET_TABLE=musteri_sikayetleri

   SQL_DRIVER=ODBC Driver 17 for SQL Server
   SQL_SERVER=192.168.2.214
   SQL_DATABASE=ChefsAI
   SQL_USERNAME=NilayTest
   SQL_PASSWORD=1Y11m5egIoy13A

   MAIL_SENDER=notification@chefseasons.com
   MAIL_PASSWORD=gtyo feid mvdo urql
   MAIL_RECEIVER=nilay@chefseasons.com

   LOG_FILE=C:\Users\nilay\Documents\GitHub\Müşteri_Şikayetleri\logs\musteri_sikayet.log
   DELAY_MINUTES=1
   ```

## Kullanım

### Uygulamayı Çalıştırma

Windows için [`bat10.bat`](bat10.bat) dosyasını çalıştırın veya doğrudan Python ile:

```bash
python main.py
```

Bu komut, Excel dosyasındaki değişiklikleri izlemeye başlar.

## Dosya Yapısı

```
.
├── .env                    # Ortam değişkenleri
├── bat10.bat               # Windows başlatma scripti
├── config.py               # Yapılandırma ayarları
├── db.py                   # Veritabanı işlemleri
├── excel_processor.py      # Excel işleme mantığı
├── logger.py               # Günlük tutma
├── mail_body.py            # E-posta gövdesi oluşturma
├── mailer.py               # E-posta gönderme
├── main.py                 # Ana giriş noktası
├── preprocess.py           # Veri ön işleme
├── requirements.txt        # Python bağımlılıkları
├── watcher.py              # Dosya izleme
├── .github/
│   └── workflows/
│       └── python-ci.yml   # CI/CD pipeline
├── logs/                   # Günlük dosyaları
└── __pycache__/            # Python cache
```

## Yapılandırma

### Veritabanı Tablosu

SQL Server'da aşağıdaki tablo yapısını oluşturun:

```sql
CREATE TABLE musteri_sikayetleri (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Şikayet_Tarihi DATE,
    Ay INT,
    Yıl INT,
    Şikayeti_Yapan_Müşteri_Adı NVARCHAR(255),
    Ürün_Grubu NVARCHAR(255),
    Ürün_İsmi NVARCHAR(255),
    Ürün_Üretim_Yılı NVARCHAR(255),
    Parti_No NVARCHAR(255),
    STT_TETT NVARCHAR(255),
    Şikayet_Konu_Grubu NVARCHAR(255),
    Şikayet_Konusu NVARCHAR(MAX),
    Şikayet_Çözümü NVARCHAR(MAX),
    Şikayete_Dönüş_Tarihi DATE,
    Döf_No NVARCHAR(255),
    Şikayete_Dönüş_Süresi_Gün INT,
    Sonuç NVARCHAR(255),
    Üretim_Hatalı NVARCHAR(255),
    RowHash NVARCHAR(64) UNIQUE
);
```

### E-posta Ayarları

Gmail SMTP kullanıyorsanız, uygulama şifresi oluşturun ve [`.env`](.env)'de [`MAIL_PASSWORD`](config.py) olarak ayarlayın.

## Katkıda Bulunma

1. Fork edin.
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`).
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`).
4. Push edin (`git push origin feature/yeni-ozellik`).
5. Pull Request oluşturun.

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.

## İletişim

Sorularınız için [gulernilay088@gmail.com](mailto:gulernilay088@gmail.com) adresine e-posta gönderin.
