#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Maps İşletme Veri Toplama Aracı - Modern GUI
Bu script Google Maps'ten işletme bilgilerini toplar ve Excel dosyasına aktarır.
"""

import os
import sys
from tkinter import messagebox

def main():
    """Ana fonksiyon - Loading ekranını başlat"""
    try:
        # Loading ekranını import et ve başlat
        from loading_screen import main as loading_main
        loading_main()
        
    except ImportError as e:
        # GUI import edilemezse konsol moduna geç
        print("=" * 60)
        print("🗺️  GOOGLE MAPS İŞLETME VERİ TOPLAMA ARACI")
        print("=" * 60)
        print()
        print("❌ Modern GUI başlatılamadı!")
        print(f"   Hata: {e}")
        print()
        print("💡 Çözüm önerileri:")
        print("   1. tkinter kurulu olduğundan emin olun")
        print("   2. modern_gui.py dosyasının mevcut olduğunu kontrol edin")
        print("   3. Gerekli kütüphanelerin kurulu olduğunu kontrol edin")
        print()
        
        # Konsol modu için basit arayüz
        run_console_mode()
        
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        messagebox.showerror("Hata", f"Uygulama başlatılamadı: {e}")

def run_console_mode():
    """Konsol modu - basit arayüz"""
    from google_maps_scraper import GoogleMapsScraper
    import logging
    
    print("🖥️  KONSOL MODU")
    print("-" * 40)
    
    # Kullanıcıdan bilgileri al
    query = input("🔍 Aranacak işletme türü (örn: restoran, eczane, market): ").strip()
    if not query:
        print("❌ Arama terimi boş olamaz!")
        return
    
    location = input("📍 Konum (örn: İstanbul, Ankara, İzmir) [opsiyonel]: ").strip()
    
    try:
        max_results = int(input("📊 Maksimum sonuç sayısı (varsayılan: 20): ") or "20")
        if max_results <= 0:
            max_results = 20
    except ValueError:
        max_results = 20
    
    headless_input = input("🖥️  Tarayıcıyı görünmez modda çalıştır? (e/h) [varsayılan: e]: ").strip().lower()
    headless = headless_input in ['e', 'evet', 'y', 'yes'] or headless_input == ''
    
    filename = input("💾 Excel dosya adı (varsayılan: isletme_verileri.xlsx): ").strip()
    if not filename:
        filename = "isletme_verileri.xlsx"
    if not filename.endswith('.xlsx'):
        filename += '.xlsx'
    
    print()
    print("🚀 Arama başlatılıyor...")
    print(f"   Arama terimi: {query}")
    print(f"   Konum: {location if location else 'Belirtilmedi'}")
    print(f"   Maksimum sonuç: {max_results}")
    print(f"   Mod: DETAYLI (tüm bilgiler)")
    print(f"   Dosya adı: {filename}")
    print()
    
    # Scraper'ı başlat
    try:
        with GoogleMapsScraper(headless=headless) as scraper:
            # Arama yap - sadece detaylı mod
            success = scraper.search_businesses(
                query=query,
                location=location,
                max_results=max_results,
                detailed_info=True
            )
            
            if success and scraper.business_data:
                print(f"✅ {len(scraper.business_data)} işletme verisi toplandı!")
                print()
                
                # Excel'e kaydet
                print("💾 Veriler Excel dosyasına kaydediliyor...")
                # Eğer filename verilmemişse otomatik oluştur
                if not filename or filename == "isletme_verileri.xlsx":
                    filename = scraper.generate_filename()
                    print(f"📝 Otomatik dosya ismi: {filename}")
                
                if scraper.save_to_excel(filename):
                    print(f"✅ Veriler başarıyla '{filename}' dosyasına kaydedildi!")
                    print()
                    
                    # Özet bilgiler
                    print("📊 TOPLAMA ÖZETİ:")
                    print("-" * 30)
                    print(f"Toplanan işletme sayısı: {len(scraper.business_data)}")
                    print(f"Kayıt dosyası: {os.path.abspath(filename)}")
                    
                    # İlk birkaç işletmeyi göster
                    if scraper.business_data:
                        print()
                        print("🔍 İLK 5 İŞLETME:")
                        print("-" * 30)
                        for i, business in enumerate(scraper.business_data[:5], 1):
                            print(f"{i}. {business.get('Ad', 'Bilinmiyor')}")
                            if business.get('Adres'):
                                print(f"   📍 {business['Adres']}")
                            if business.get('Telefon'):
                                print(f"   📞 {business['Telefon']}")
                            if business.get('Puan/Yorum'):
                                print(f"   ⭐ {business['Puan/Yorum']}")
                            print()
                else:
                    print("❌ Excel dosyası kaydedilemedi!")
            else:
                print("❌ Hiç işletme verisi toplanamadı!")
                print("   Lütfen arama kriterlerinizi kontrol edin.")
    
    except KeyboardInterrupt:
        print("\n⏹️  İşlem kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n❌ Beklenmeyen bir hata oluştu: {e}")
        logging.error(f"Ana program hatası: {e}")

def show_help():
    """Yardım menüsünü göster"""
    print("=" * 60)
    print("📖 KULLANIM KILAVUZU")
    print("=" * 60)
    print()
    print("Bu araç Google Maps'ten işletme bilgilerini toplar ve Excel'e aktarır.")
    print()
    print("🔧 KURULUM:")
    print("   1. pip install -r requirements.txt")
    print("   2. python main.py")
    print()
    print("📝 KULLANIM:")
    print("   - Arama terimi: 'restoran', 'eczane', 'market' gibi")
    print("   - Konum: 'İstanbul', 'Ankara' gibi (opsiyonel)")
    print("   - Sonuç sayısı: Toplanacak maksimum işletme sayısı")
    print()
    print("📊 TOPLANAN VERİLER:")
    print("   - İşletme adı")
    print("   - Adres")
    print("   - Telefon numarası")
    print("   - Website")
    print("   - Puan ve yorum sayısı")
    print("   - Kategori")
    print("   - Açılış saatleri")
    print("   - Durum (açık/kapalı)")
    print()
    print("⚠️  ÖNEMLİ NOTLAR:")
    print("   - Bu araç tamamen ücretsizdir")
    print("   - Google'ın kullanım şartlarına uygun kullanın")
    print("   - Çok hızlı arama yapmayın (rate limiting)")
    print("   - Tarayıcı görünmez modda çalışabilir")
    print()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
    else:
        main()
