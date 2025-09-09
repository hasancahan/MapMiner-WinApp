# 🗺️ Google Maps İşletme Veri Toplama Aracı

## 📋 Özellikler

- **Google Maps'ten işletme verilerini toplama**
- **Excel formatında kaydetme** (otomatik isimlendirme)
- **WhatsApp otomatik mesaj gönderme**
- **Modern ve kullanıcı dostu arayüz**
- **Profesyonel loading ekranı**
- **Toplu mesaj gönderme sistemi**

## 🚀 Kurulum

### Gereksinimler
- Windows 10/11
- Chrome tarayıcı
- İnternet bağlantısı

### Çalıştırma
1. `GoogleMaps_Scraper_Final.exe` dosyasını çalıştırın
2. Loading ekranı 5 saniye gösterilecek
3. Ana uygulama otomatik açılacak

## 📖 Kullanım

### 1. Veri Toplama
- **İşletme türü** girin (örn: "restoran", "berber")
- **Şehir** seçin
- **Maksimum sonuç** sayısını belirleyin
- **"Ara"** butonuna tıklayın

### 2. Excel Kaydetme
- Veriler toplandıktan sonra **"Excel'e Kaydet"** butonuna tıklayın
- Dosya otomatik isimlendirilir: `İşletme_Şehir_Raporu_Tarih.xlsx`

### 3. WhatsApp Mesaj Gönderme
- **"Toplu Mesaj Gönder"** butonuna tıklayın
- Excel dosyasını seçin
- Mesaj şablonunu düzenleyin
- **"Otomatik Gönder"** ile başlatın

## 📱 WhatsApp Mesaj Şablonu

```
Merhaba {isim},

{isletme_adi} işletmeniz için özel teklifimiz var!

📍 Adres: {adres}
⭐ Puan: {puan}
📞 Telefon: {telefon}

Detaylar için iletişime geçin.

İyi günler!
```

## 🎨 Arayüz Özellikleri

- **Modern tasarım** - Profesyonel görünüm
- **Renkli butonlar** - Hover efektleri
- **İlerleme çubuğu** - Gerçek zamanlı güncelleme
- **Responsive tasarım** - Tüm ekran boyutlarında uyumlu

## 📊 Excel Çıktısı

- **İşletme adı**
- **Adres**
- **Telefon**
- **Puan**

## ⚙️ Teknik Detaylar

- **Python 3.13** tabanlı
- **Tkinter** GUI framework
- **Selenium** web scraping
- **Pandas** veri işleme
- **OpenPyXL** Excel işleme
- **PyAutoGUI** otomasyon

## 🔧 Sorun Giderme

### Chrome Hatası
- Chrome tarayıcısının güncel olduğundan emin olun
- Uygulamayı yönetici olarak çalıştırın

### WhatsApp Hatası
- WhatsApp Web'in açık olduğundan emin olun
- QR kodu tarayın
- 15 saniye bekleyin

## 📞 Destek

**HDynamicX** tarafından geliştirilmiştir.

---

*© 2024 HDynamicX - Tüm hakları saklıdır.*