# 🗺️ Google Maps İşletme Veri Toplama Aracı

Bu araç Google Maps'ten işletme bilgilerini toplar ve Excel dosyasına aktarır. Tamamen ücretsiz ve sınırı olmayan bir yöntem kullanır.

## ✨ Özellikler

- 🔍 **Esnek Arama**: İstediğiniz işletme türünü ve konumu arayabilirsiniz
- 📊 **Detaylı Veri**: İşletme adı, adres, telefon, website, puan ve daha fazlası
- 📈 **Excel Export**: Toplanan veriler otomatik olarak Excel dosyasına aktarılır
- 🚀 **Hızlı ve Güvenilir**: Selenium WebDriver ile güvenilir veri toplama
- 💰 **Tamamen Ücretsiz**: Hiçbir API anahtarı veya ücret gerekmez
- 🛡️ **Anti-Bot Koruması**: Google'ın bot tespit sistemlerini aşar

## 🔧 Kurulum

### 1. Gereksinimler
- Python 3.7 veya üzeri
- Chrome tarayıcısı

### 2. Bağımlılıkları Yükle
```bash
pip install -r requirements.txt
```

### 3. Çalıştır
```bash
python main.py
```

## 📝 Kullanım

### Temel Kullanım
```bash
python main.py
```

Program size şu bilgileri soracak:
- **Arama terimi**: `restoran`, `eczane`, `market` gibi
- **Konum**: `İstanbul`, `Ankara`, `İzmir` gibi (opsiyonel)
- **Maksimum sonuç sayısı**: Toplanacak işletme sayısı
- **Görünmez mod**: Tarayıcıyı arka planda çalıştırma seçeneği
- **Dosya adı**: Excel dosyasının adı

### Örnek Kullanım
```
🔍 Aranacak işletme türü: restoran
📍 Konum: İstanbul
📊 Maksimum sonuç sayısı: 100
🖥️ Tarayıcıyı görünmez modda çalıştır? (e/h): e
⚡ Hız modu: 1=Hızlı (sadece temel), 2=Normal, 3=Detaylı: 1
💾 Excel dosya adı: istanbul_restoranlar.xlsx
```

### ⚡ Hız Modları:
- **1 - Hızlı**: Sadece temel bilgiler, çok hızlı (önerilen)
- **2 - Normal**: Temel bilgiler + ilk 2 işletme için hızlı detaylar
- **3 - Detaylı**: Tüm bilgiler + ilk 3 işletme için tam detaylar (yavaş)

## 📊 Toplanan Veriler

Excel dosyasında şu bilgiler yer alır:

### Temel Bilgiler:
| Sütun | Açıklama |
|-------|----------|
| Sıra | İşletme sıra numarası |
| İsim | İşletme adı |
| Adres | Tam adres bilgisi |
| Telefon | Telefon numarası |
| Website | Web sitesi adresi |
| Puan | Google puanı ve yıldız sayısı |
| Yorum Sayısı | Toplam yorum sayısı |
| Kategori | İşletme kategorisi |
| Açılış Saatleri | Günlük açılış saatleri |
| Durum | Açık/Kapalı durumu |
| Fiyat Seviyesi | Fiyat aralığı (₺₺₺) |

### Detaylı Bilgiler (Hız moduna göre):
| Sütun | Açıklama |
|-------|----------|
| Fotoğraf Sayısı | Google Maps'teki fotoğraf sayısı |
| İnceleme Özeti | Müşteri yorumları özeti |
| Popüler Zamanlar | En yoğun saatler |
| Hizmetler | Sunulan hizmetler listesi |
| Özellikler | WiFi, otopark, teslimat vb. |
| Koordinatlar | GPS koordinatları |
| Çalışma Saatleri Detay | Detaylı açılış saatleri |
| Menü Linki | Online menü linki |
| Rezervasyon Linki | Rezervasyon linki |
| Sosyal Medya | Sosyal medya hesapları |
| Açılış Tarihi | İşletme açılış tarihi |
| Çalışan Sayısı | Tahmini çalışan sayısı |
| Kurumsal Bilgi | Şirket bilgileri |

## 🛠️ Gelişmiş Kullanım

### Programatik Kullanım
```python
from google_maps_scraper import GoogleMapsScraper

# Scraper'ı başlat
with GoogleMapsScraper(headless=True) as scraper:
    # Hızlı arama yap
    scraper.search_businesses(
        query="restoran",
        location="İstanbul",
        max_results=50,
        speed_mode="fast"  # "fast", "normal", "detailed"
    )
    
    # Excel'e kaydet
    scraper.save_to_excel("restoranlar.xlsx")
```

### Özelleştirme Seçenekleri
```python
# Görünür modda çalıştır
scraper = GoogleMapsScraper(headless=False)

# Belirli bir işletmenin detaylarını al
detailed_info = scraper.get_detailed_info(business_index=0)
```

## ⚠️ Önemli Notlar

### Yasal Uyarı
- Bu araç Google'ın kullanım şartlarına uygun olarak tasarlanmıştır
- Sadece kamuya açık bilgileri toplar
- Ticari kullanım için Google'ın resmi API'lerini kullanmanız önerilir

### Rate Limiting
- Çok hızlı arama yapmayın (dakikada 10-20 arama yeterli)
- Büyük veri setleri için arama aralarında bekleme süreleri ekleyin
- Google'ın bot tespit sistemlerini tetiklememek için dikkatli kullanın

### Teknik Sınırlamalar
- Google Maps'in arayüz değişiklikleri scripti etkileyebilir
- İnternet bağlantısı gereklidir
- Chrome tarayıcısı otomatik olarak indirilir

## 🐛 Sorun Giderme

### Yaygın Sorunlar

**1. Chrome Driver Hatası**
```bash
# WebDriver Manager otomatik olarak Chrome driver'ı indirir
# Manuel indirme gerekmez
```

**2. Veri Toplanamıyor**
- Arama terimini değiştirin
- Konum bilgisini ekleyin
- İnternet bağlantınızı kontrol edin

**3. Excel Dosyası Açılmıyor**
- Dosya başka bir programda açık olabilir
- Dosya izinlerini kontrol edin

### Log Dosyaları
Program çalışırken konsola detaylı log bilgileri yazdırır. Hata durumunda bu logları kontrol edin.

## 📁 Proje Yapısı

```
Finmap/
├── main.py                 # Ana çalıştırma dosyası
├── google_maps_scraper.py  # Ana scraper sınıfı
├── requirements.txt        # Python bağımlılıkları
├── README.md              # Bu dosya
└── isletme_verileri.xlsx  # Çıktı dosyası (otomatik oluşur)
```

## 🤝 Katkıda Bulunma

1. Projeyi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 🆘 Destek

Sorunlarınız için:
- GitHub Issues bölümünü kullanın
- Detaylı hata mesajları ekleyin
- Kullandığınız Python ve Chrome sürümlerini belirtin

---

**Not**: Bu araç eğitim ve araştırma amaçlıdır. Ticari kullanım için Google'ın resmi API'lerini kullanmanız önerilir.
