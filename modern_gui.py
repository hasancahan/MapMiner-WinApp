#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern GUI for Google Maps Business Scraper
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import os
from google_maps_scraper import GoogleMapsScraper
import webbrowser
import time
import pandas as pd
import pyautogui

class ModernScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🗺️ Google Maps İşletme Veri Toplama Aracı")
        self.root.geometry("900x800")
        self.root.configure(bg='#f0f0f0')
        self.root.minsize(800, 700)  # Minimum boyut
        
        # Modern renk paleti
        self.colors = {
            'primary': '#2E86AB',      # Mavi
            'secondary': '#A23B72',    # Pembe
            'success': '#28A745',      # Yeşil
            'warning': '#FFC107',      # Sarı
            'danger': '#DC3545',       # Kırmızı
            'light': '#F8F9FA',        # Açık gri
            'dark': '#343A40',         # Koyu gri
            'white': '#FFFFFF',        # Beyaz
            'border': '#DEE2E6'        # Kenarlık
        }
        
        # Scraper instance
        self.scraper = None
        self.is_running = False
        
        self.setup_ui()
    
    def center_window(self, window):
        """Pencereyi ekranın ortasında konumlandır - EXE uyumlu"""
        window.update_idletasks()
        
        # Sabit pencere boyutları (EXE'de güvenilir)
        window_width = 900
        window_height = 800
        
        # Ekran boyutlarını al
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Ortalama koordinatlarını hesapla
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Negatif koordinatları önle
        x = max(0, x)
        y = max(0, y)
        
        # Pencereyi ortala - sabit boyutlarla
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        window.update()
        
    def setup_ui(self):
        """Modern UI'yi oluştur"""
        
        # Ana container
        main_frame = tk.Frame(self.root, bg=self.colors['light'], padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Başlık
        self.create_header(main_frame)
        
        # Arama formu
        self.create_search_form(main_frame)
        
        # İlerleme çubuğu
        self.create_progress_section(main_frame)
        
        # Sonuçlar alanı
        self.create_results_section(main_frame)
        
        # Alt butonlar
        self.create_footer_buttons(main_frame)
        
    def create_header(self, parent):
        """Başlık bölümünü oluştur"""
        header_frame = tk.Frame(parent, bg=self.colors['light'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Ana başlık
        title_label = tk.Label(
            header_frame,
            text="🗺️ Google Maps İşletme Veri Toplama",
            font=('Segoe UI', 24, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['light']
        )
        title_label.pack()
        
        # Alt başlık
        subtitle_label = tk.Label(
            header_frame,
            text="Modern ve hızlı işletme verisi toplama aracı",
            font=('Segoe UI', 12),
            fg=self.colors['dark'],
            bg=self.colors['light']
        )
        subtitle_label.pack(pady=(5, 0))
        
    def create_search_form(self, parent):
        """Arama formunu oluştur"""
        form_frame = tk.LabelFrame(
            parent,
            text="🔍 Arama Kriterleri",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['light'],
            padx=15,
            pady=15
        )
        form_frame.pack(fill='x', pady=(0, 20))
        
        # İşletme türü
        tk.Label(
            form_frame,
            text="İşletme Türü:",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['light']
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        self.query_var = tk.StringVar(value="restoran")
        query_entry = tk.Entry(
            form_frame,
            textvariable=self.query_var,
            font=('Segoe UI', 10),
            width=30,
            relief='flat',
            bd=1
        )
        query_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # Konum
        tk.Label(
            form_frame,
            text="Konum:",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['light']
        ).grid(row=1, column=0, sticky='w', pady=5)
        
        self.location_var = tk.StringVar(value="İstanbul")
        location_entry = tk.Entry(
            form_frame,
            textvariable=self.location_var,
            font=('Segoe UI', 10),
            width=30,
            relief='flat',
            bd=1
        )
        location_entry.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # Maksimum sonuç
        tk.Label(
            form_frame,
            text="Maksimum Sonuç:",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['light']
        ).grid(row=2, column=0, sticky='w', pady=5)
        
        self.max_results_var = tk.StringVar(value="20")
        max_results_entry = tk.Entry(
            form_frame,
            textvariable=self.max_results_var,
            font=('Segoe UI', 10),
            width=30,
            relief='flat',
            bd=1
        )
        max_results_entry.grid(row=2, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # Görünmez mod seçeneği kaldırıldı - her zaman görünür mod
        
        # Sütun ağırlıklarını ayarla
        form_frame.columnconfigure(1, weight=1)
        
    def create_progress_section(self, parent):
        """İlerleme bölümünü oluştur"""
        progress_frame = tk.LabelFrame(
            parent,
            text="📊 İlerleme",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['light'],
            padx=15,
            pady=15
        )
        progress_frame.pack(fill='x', pady=(0, 20))
        
        # İlerleme çubuğu
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(fill='x', pady=(0, 10))
        
        # İlerleme çubuğu stilini yeşil yap
        style = ttk.Style()
        style.theme_use('clam')  # Tema değiştir
        style.configure("Green.Horizontal.TProgressbar", 
                       background='#28A745',  # Yeşil renk
                       troughcolor='#E9ECEF',  # Açık gri arka plan
                       borderwidth=0,
                       lightcolor='#28A745',
                       darkcolor='#28A745')
        self.progress_bar.configure(style="Green.Horizontal.TProgressbar")
        
        # Durum etiketi
        self.status_label = tk.Label(
            progress_frame,
            text="Hazır",
            font=('Segoe UI', 10),
            fg=self.colors['dark'],
            bg=self.colors['light']
        )
        self.status_label.pack()
        
        # Bulunan işletme sayısı
        self.count_label = tk.Label(
            progress_frame,
            text="Bulunan işletme: 0",
            font=('Segoe UI', 10, 'bold'),
            fg=self.colors['success'],
            bg=self.colors['light']
        )
        self.count_label.pack(pady=(5, 0))
        
    def create_results_section(self, parent):
        """Sonuçlar bölümünü oluştur"""
        results_frame = tk.LabelFrame(
            parent,
            text="📋 Sonuçlar",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['light'],
            padx=15,
            pady=15
        )
        results_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Log alanı
        self.log_text = scrolledtext.ScrolledText(
            results_frame,
            height=8,
            font=('Consolas', 9),
            bg='#2C3E50',
            fg='#ECF0F1',
            insertbackground='white',
            relief='flat',
            bd=0
        )
        self.log_text.pack(fill='both', expand=True)
        
    def create_footer_buttons(self, parent):
        """Alt butonları oluştur"""
        button_frame = tk.Frame(parent, bg=self.colors['light'], pady=10)
        button_frame.pack(fill='x')
        
        # Başlat butonu - modern ve şık
        self.start_button = tk.Button(
            button_frame,
            text="BAŞLAT",
            font=('Segoe UI', 11, 'bold'),
            bg='#E8F5E8',    # Soft yeşil (başlatma)
            fg='#2D5A2D',    # Koyu yeşil yazı
            relief='flat',
            bd=1,            # İnce border
            padx=25,         # Daha geniş padding (radius efekti)
            pady=12,         # Daha yüksek padding
            command=self.start_search,
            cursor='hand2',
            activebackground='#D4F4D4',  # Daha koyu soft yeşil hover
            activeforeground='#1A3D1A'
        )
        self.start_button.pack(side='left', padx=(0, 8))
        
        # Durdur butonu - modern ve şık
        self.stop_button = tk.Button(
            button_frame,
            text="DURDUR",
            font=('Segoe UI', 11, 'bold'),
            bg='#FFE8E8',    # Soft kırmızı (durdurma)
            fg='#8B2A2A',    # Koyu kırmızı yazı
            relief='flat',
            bd=1,            # İnce border
            padx=25,         # Daha geniş padding (radius efekti)
            pady=12,         # Daha yüksek padding
            command=self.stop_search,
            state='disabled',
            cursor='hand2',
            activebackground='#FFD4D4',  # Daha koyu soft kırmızı hover
            activeforeground='#6B1A1A'
        )
        self.stop_button.pack(side='left', padx=(0, 8))
        
        # Excel'e kaydet butonu - modern ve şık
        self.save_button = tk.Button(
            button_frame,
            text="KAYDET",
            font=('Segoe UI', 11, 'bold'),
            bg='#E8F4FF',    # Soft mavi (kaydetme)
            fg='#2A5A8B',    # Koyu mavi yazı
            relief='flat',
            bd=1,            # İnce border
            padx=25,         # Daha geniş padding (radius efekti)
            pady=12,         # Daha yüksek padding
            command=self.save_to_excel,
            state='disabled',
            cursor='hand2',
            activebackground='#D4E8FF',  # Daha koyu soft mavi hover
            activeforeground='#1A3D6B'
        )
        self.save_button.pack(side='left', padx=(0, 8))
        
        # Toplu mesaj gönder butonu - modern ve şık
        self.bulk_message_button = tk.Button(
            button_frame,
            text="TOPLU MESAJ",
            font=('Segoe UI', 11, 'bold'),
            bg='#FFF4E8',    # Soft turuncu (mesaj gönderme)
            fg='#8B5A2A',    # Koyu turuncu yazı
            relief='flat',
            bd=1,            # İnce border
            padx=25,         # Daha geniş padding (radius efekti)
            pady=12,         # Daha yüksek padding
            command=self.open_bulk_message_window,
            cursor='hand2',
            activebackground='#FFE8D4',  # Daha koyu soft turuncu hover
            activeforeground='#6B3D1A'
        )
        self.bulk_message_button.pack(side='right')
        
        # Butonlara modern efektler ekle
        self.add_button_effects()
        
    def add_button_effects(self):
        """Butonlara modern efektler ekle"""
        try:
            # Butonlara hover efekti ekle - soft renkler
            self.start_button.bind("<Enter>", lambda e: self.start_button.config(bg='#D4F4D4'))
            self.start_button.bind("<Leave>", lambda e: self.start_button.config(bg='#E8F5E8'))
            
            self.stop_button.bind("<Enter>", lambda e: self.stop_button.config(bg='#FFD4D4'))
            self.stop_button.bind("<Leave>", lambda e: self.stop_button.config(bg='#FFE8E8'))
            
            self.save_button.bind("<Enter>", lambda e: self.save_button.config(bg='#D4E8FF'))
            self.save_button.bind("<Leave>", lambda e: self.save_button.config(bg='#E8F4FF'))
            
            self.bulk_message_button.bind("<Enter>", lambda e: self.bulk_message_button.config(bg='#FFE8D4'))
            self.bulk_message_button.bind("<Leave>", lambda e: self.bulk_message_button.config(bg='#FFF4E8'))
            
        except Exception as e:
            # Efekt ekleme başarısız olursa devam et
            pass
        
    def log_message(self, message, level='info'):
        """Log mesajı ekle"""
        colors = {
            'info': '#3498DB',
            'success': '#2ECC71',
            'warning': '#F39C12',
            'error': '#E74C3C'
        }
        
        self.log_text.insert(tk.END, f"[{level.upper()}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def start_search(self):
        """Aramayı başlat"""
        if self.is_running:
            return
            
        # Form verilerini al
        query = self.query_var.get().strip()
        location = self.location_var.get().strip()
        
        try:
            max_results = int(self.max_results_var.get())
        except ValueError:
            messagebox.showerror("Hata", "Maksimum sonuç sayısı geçerli bir sayı olmalıdır!")
            return
            
        if not query:
            messagebox.showerror("Hata", "İşletme türü boş olamaz!")
            return
            
        # UI'yi güncelle
        self.is_running = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.save_button.config(state='disabled')
        
        # Log'u temizle
        self.log_text.delete(1.0, tk.END)
        
        # Aramayı thread'de başlat
        search_thread = threading.Thread(
            target=self.run_search,
            args=(query, location, max_results),
            daemon=True
        )
        search_thread.start()
        
    def run_search(self, query, location, max_results):
        """Arama işlemini çalıştır"""
        try:
            self.log_message(f"Arama başlatılıyor: '{query}' in '{location}'", 'info')
            self.update_status("Arama başlatılıyor...")
            
            # İlerleme çubuğunu sıfırla
            self.progress_var.set(0)
            self.update_count(0)
            
            # Scraper'ı oluştur - her zaman görünür mod
            self.scraper = GoogleMapsScraper(headless=False)
            
            # Arama yap - progress callback ile
            success = self.scraper.search_businesses(
                query=query,
                location=location,
                max_results=max_results,
                detailed_info=True,
                progress_callback=self.update_progress
            )
            
            if success and self.scraper.business_data:
                self.log_message(f"✅ {len(self.scraper.business_data)} işletme bulundu!", 'success')
                self.update_status("Arama tamamlandı!")
                self.update_count(len(self.scraper.business_data))
                self.progress_var.set(100)
                
                # İlk 5 işletmeyi göster
                self.log_message("\n🔍 BULUNAN İŞLETMELER:", 'info')
                for i, business in enumerate(self.scraper.business_data[:5], 1):
                    self.log_message(f"{i}. {business.get('Ad', 'Bilinmiyor')}", 'success')
                    if business.get('Adres'):
                        self.log_message(f"   📍 {business['Adres']}", 'info')
                    if business.get('Telefon'):
                        self.log_message(f"   📞 {business['Telefon']}", 'info')
                    if business.get('Puan/Yorum'):
                        self.log_message(f"   ⭐ {business['Puan/Yorum']}", 'info')
                    self.log_message("", 'info')
                
                if len(self.scraper.business_data) > 5:
                    self.log_message(f"... ve {len(self.scraper.business_data) - 5} işletme daha", 'info')
                    
            else:
                self.log_message("❌ Hiç işletme bulunamadı!", 'error')
                self.update_status("Arama başarısız!")
                
        except Exception as e:
            self.log_message(f"❌ Hata: {str(e)}", 'error')
            self.update_status("Hata oluştu!")
            
        finally:
            # UI'yi güncelle
            self.is_running = False
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
            if self.scraper and self.scraper.business_data:
                self.save_button.config(state='normal')
                
    def stop_search(self):
        """Aramayı durdur"""
        self.is_running = False
        if self.scraper:
            self.scraper.close()
        self.update_status("Durduruldu")
        self.log_message("Arama durduruldu", 'warning')
        
    def save_to_excel(self):
        """Excel'e kaydet"""
        if not self.scraper or not self.scraper.business_data:
            messagebox.showwarning("Uyarı", "Kaydedilecek veri bulunamadı!")
            return
        
        # Otomatik dosya ismi oluştur
        auto_filename = self.scraper.generate_filename()
        
        # Kullanıcıya dosya konumu seçtir
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Excel dosyasını kaydet",
            initialfile=auto_filename
        )
        
        if filename:
            try:
                if self.scraper.save_to_excel(filename):
                    self.log_message(f"✅ Veriler '{os.path.basename(filename)}' dosyasına kaydedildi!", 'success')
                    messagebox.showinfo("Başarılı", f"Veriler başarıyla kaydedildi!\n\nDosya: {filename}")
                else:
                    self.log_message("❌ Excel dosyası kaydedilemedi!", 'error')
                    messagebox.showerror("Hata", "Excel dosyası kaydedilemedi!")
            except Exception as e:
                self.log_message(f"❌ Kaydetme hatası: {str(e)}", 'error')
                messagebox.showerror("Hata", f"Kaydetme hatası: {str(e)}")
                
    def open_bulk_message_window(self):
        """Toplu mesaj penceresini aç"""
        try:
            from tkinter import filedialog
            
            # Excel dosyası seç
            excel_file = filedialog.askopenfilename(
                title="Excel Dosyası Seçin",
                filetypes=[("Excel dosyaları", "*.xlsx"), ("Tüm dosyalar", "*.*")],
                initialdir=os.getcwd()
            )
            
            if not excel_file:
                return  # Kullanıcı iptal etti
            
            # Toplu mesaj penceresini aç
            BulkMessageWindow(self.root, excel_file)
            
        except Exception as e:
            messagebox.showerror("Hata", f"Toplu mesaj penceresi açılamadı: {str(e)}")
            
    def update_status(self, status):
        """Durum etiketini güncelle"""
        self.status_label.config(text=status)
        self.root.update_idletasks()
        
    def update_count(self, count):
        """İşletme sayısını güncelle"""
        self.count_label.config(text=f"Bulunan işletme: {count}")
        self.root.update_idletasks()
        
    def update_progress(self, progress_percent, count, business_name):
        """İlerleme çubuğunu güncelle"""
        try:
            # Thread-safe güncelleme
            self.root.after(0, self._update_progress_ui, progress_percent, count, business_name)
        except Exception as e:
            pass  # İlerleme güncelleme hatası sessizce geç
    
    def _update_progress_ui(self, progress_percent, count, business_name):
        """UI'yi güncelle (main thread'de çalışır)"""
        try:
            # İlerleme çubuğunu güncelle
            self.progress_var.set(progress_percent)
            
            # İşletme sayısını güncelle
            self.update_count(count)
            
            # Durum mesajını güncelle
            self.update_status(f"İşletme toplanıyor: {business_name}")
            
            # Log mesajı ekle
            self.log_message(f"📊 {count}. işletme: {business_name}", 'info')
            
        except Exception as e:
            pass  # UI güncelleme hatası sessizce geç
        

class BulkMessageWindow:
    """Toplu mesaj gönderme penceresi"""
    
    def center_window(self, window):
        """Pencereyi ekranın ortasında konumlandır - EXE uyumlu"""
        window.update_idletasks()
        
        # Sabit pencere boyutları (EXE'de güvenilir)
        window_width = 900
        window_height = 800
        
        # Ekran boyutlarını al
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Ortalama koordinatlarını hesapla
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Negatif koordinatları önle
        x = max(0, x)
        y = max(0, y)
        
        # Pencereyi ortala - sabit boyutlarla
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        window.update()
    
    def __init__(self, parent, excel_file):
        self.parent = parent
        self.excel_file = excel_file
        self.whatsapp_driver = None
        
        # Pencere oluştur
        self.window = tk.Toplevel(parent)
        self.window.title("📱 Toplu WhatsApp Mesajı")
        self.window.geometry("900x800")
        self.window.configure(bg='#F5F5F5')
        self.window.resizable(True, True)
        self.window.minsize(600, 500)
        
        # Pencereyi ortala
        self.center_window(self.window)
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_widgets()
        self.load_excel_data()
        
    def create_widgets(self):
        """Widget'ları oluştur"""
        # Başlık
        title_label = tk.Label(
            self.window,
            text="📱 WhatsApp Toplu Mesaj Gönder",
            font=('Segoe UI', 16, 'bold'),
            bg='#F5F5F5',
            fg='#2E86AB'
        )
        title_label.pack(pady=20)
        
        # Excel dosyası bilgisi
        import os
        file_name = os.path.basename(self.excel_file)
        file_label = tk.Label(
            self.window,
            text=f"📄 Excel Dosyası: {file_name}",
            font=('Segoe UI', 10),
            bg='#F5F5F5',
            fg='#666666'
        )
        file_label.pack(pady=5)
        
        
        
        
        # Mesaj alanı
        message_frame = tk.Frame(self.window, bg='#F5F5F5')
        message_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        tk.Label(
            message_frame,
            text="💬 Mesaj İçeriği:",
            font=('Segoe UI', 12, 'bold'),
            bg='#F5F5F5',
            fg='#2E86AB'
        ).pack(anchor='w')
        
        self.message_text = tk.Text(
            message_frame,
            height=10,
            font=('Segoe UI', 11),
            wrap='word',
            relief='flat',
            bd=1,
            bg='white'
        )
        self.message_text.pack(fill='both', expand=True, pady=5)
        
        # Örnek mesaj
        example_message = """Merhaba {isim},

{isletme_adi} işletmenizi Google Maps'te gördük ve başarılı çalışmalarınızı takdir ettik! 

Biz HDynamicX olarak, işletmenizin dijital dönüşümünde yanınızdayız. 

Sunduğumuz hizmetler:

• Web Sitesi Geliştirme
• Yapay Zeka Otomasyon Çözümleri
• Mobil Uygulama Geliştirme
• IT Altyapı Danışmanlığı
• Dijital Pazarlama Desteği
• Veri Güvenliği Çözümleri

E-Mail: info@hdynamicx.com
Adres: Diyarbakır, Türkiye

Yazılım ve IT alanında herhangi bir ihtiyacınız varsa, danışmanlık için bizimle iletişime geçebilirsiniz.

Başarılarınızın devamını dileriz!"""
        
        self.message_text.insert('1.0', example_message)
        
        # Otomatik gönderim ayarları
        # Gecikme ayarları kaldırıldı - hemen gönder
        
        # Butonlar
        button_frame = tk.Frame(self.window, bg='#F5F5F5')
        button_frame.pack(pady=20, padx=20, fill='x')
        
        # Manuel gönder butonu
        self.send_button = tk.Button(
            button_frame,
            text="📤 Manuel Mesaj Linkleri",
            font=('Segoe UI', 12, 'bold'),
            bg='#E8F8F5',    # Soft yeşil (WhatsApp teması)
            fg='#1B5E20',    # Koyu yeşil yazı
            relief='flat',
            bd=1,
            padx=25,         # Eşit boyut için
            pady=12,         # Eşit boyut için
            command=self.send_bulk_messages,
            cursor='hand2',
            state='disabled',
            activebackground='#D4F4E6',  # Hover efekti
            activeforeground='#0D3D0D'
        )
        self.send_button.pack(side='left', padx=10, fill='x', expand=True)
        
        # Otomatik gönder butonu
        self.auto_send_button = tk.Button(
            button_frame,
            text="🚀 Otomatik Gönder",
            font=('Segoe UI', 12, 'bold'),
            bg='#FFF3E0',    # Soft turuncu (otomatik işlem)
            fg='#E65100',    # Koyu turuncu yazı
            relief='flat',
            bd=1,
            padx=25,         # Eşit boyut için
            pady=12,         # Eşit boyut için
            command=self.auto_send_messages,
            cursor='hand2',
            state='disabled',
            activebackground='#FFE0B2',  # Hover efekti
            activeforeground='#BF360C'
        )
        self.auto_send_button.pack(side='left', padx=5, fill='x', expand=True)
        
        # Kapat butonu
        close_button = tk.Button(
            button_frame,
            text="❌ Kapat",
            font=('Segoe UI', 12, 'bold'),  # Eşit font boyutu
            bg='#FFEBEE',    # Soft kırmızı (kapatma)
            fg='#C62828',    # Koyu kırmızı yazı
            relief='flat',
            bd=1,
            padx=25,         # Eşit boyut için
            pady=12,         # Eşit boyut için
            command=self.window.destroy,
            cursor='hand2',
            activebackground='#FFCDD2',  # Hover efekti
            activeforeground='#B71C1C'
        )
        close_button.pack(side='right', padx=20, fill='x', expand=True)
        
        # Butonlara hover efektleri ekle
        self.add_bulk_message_hover_effects()
        
    def add_bulk_message_hover_effects(self):
        """Toplu mesaj butonlarına hover efektleri ekle"""
        try:
            # Manuel gönder butonu hover efekti
            self.send_button.bind("<Enter>", lambda e: self.send_button.config(bg='#D4F4E6'))
            self.send_button.bind("<Leave>", lambda e: self.send_button.config(bg='#E8F8F5'))
            
            # Otomatik gönder butonu hover efekti
            self.auto_send_button.bind("<Enter>", lambda e: self.auto_send_button.config(bg='#FFE0B2'))
            self.auto_send_button.bind("<Leave>", lambda e: self.auto_send_button.config(bg='#FFF3E0'))
            
        except Exception as e:
            # Efekt ekleme başarısız olursa devam et
            pass
        
    def load_excel_data(self):
        """Excel verilerini yükle"""
        try:
            import pandas as pd
            
            # Excel dosyasını header=1 ile oku (ikinci satırı başlık olarak al)
            self.df = pd.read_excel(self.excel_file, header=1)
            
            # Boş satırları temizle
            self.df = self.df.dropna(how='all')  # Tüm sütunları boş olan satırları sil
            
            # İşletme adı olmayan satırları temizle
            if 'Ad' in self.df.columns:
                self.df = self.df.dropna(subset=['Ad'])  # Ad sütunu boş olan satırları sil
                self.df = self.df[self.df['Ad'].astype(str).str.strip() != '']  # Boş string'leri sil
            
            # Butonları aktif hale getir
            self.send_button.config(state='normal')
            self.auto_send_button.config(state='normal')
            
        except Exception as e:
            messagebox.showerror("Hata", f"Excel dosyası okunamadı: {str(e)}")
            self.window.destroy()
    
    
    
    def send_bulk_messages(self):
        """Toplu mesaj gönder - yeni yöntem"""
        try:
            message_content = self.message_text.get('1.0', 'end-1c')
            if not message_content.strip():
                messagebox.showerror("Hata", "Mesaj içeriği boş olamaz!")
                return
            
            # Mesajları hazırla
            messages = []
            for index, row in self.df.iterrows():
                try:
                    # Excel sütun isimlerini kontrol et
                    
                    # Sütun isimlerini farklı varyasyonlarla dene
                    # Önce Unnamed sütunlarını kontrol et
                    if 'Unnamed: 1' in row and row['Unnamed: 1'] != 'Ad':
                        name = str(row.get('Unnamed: 1', 'Değerli Müşteri'))
                    else:
                        name = (row.get('Ad') or row.get('İsim') or row.get('Name') or 
                               row.get('İşletme Adı') or row.get('Business Name') or 'Değerli Müşteri')
                    
                    # Telefon numarası - Unnamed: 3 sütununda
                    if 'Unnamed: 3' in row and row['Unnamed: 3'] != 'Telefon':
                        phone = str(row.get('Unnamed: 3', ''))
                    else:
                        phone = (row.get('Telefon') or row.get('Phone') or 
                                row.get('Tel') or row.get('Telefon Numarası') or '')
                    
                    # Telefon numarasını temizle ve kontrol et
                    if phone:
                        clean_phone = ''.join(filter(str.isdigit, str(phone)))
                        if len(clean_phone) >= 10:  # En az 10 haneli olmalı
                            phone = clean_phone
                        else:
                            phone = ''  # Geçersiz telefon numarası
                    
                    # Adres - Unnamed: 2 sütununda
                    if 'Unnamed: 2' in row and row['Unnamed: 2'] != 'Adres':
                        address = str(row.get('Unnamed: 2', 'Adres bilgisi yok'))
                    else:
                        address = (row.get('Adres') or row.get('Address') or 
                                  row.get('Konum') or row.get('Location') or 'Adres bilgisi yok')
                    
                    # Puan - Unnamed: 4 sütununda
                    if 'Unnamed: 4' in row and row['Unnamed: 4'] != 'Puan/Yorum':
                        rating = str(row.get('Unnamed: 4', 'Puan bilgisi yok'))
                    else:
                        rating = (row.get('Puan/Yorum') or row.get('Rating') or 
                                 row.get('Puan') or row.get('Score') or 'Puan bilgisi yok')
                    
                    # Mesajı kişiselleştir
                    try:
                        personalized_message = message_content.format(
                            isim=name,
                            isletme_adi=name,
                            adres=address,
                            telefon=phone,
                            puan=rating
                        )
                        
                        if phone:
                            messages.append({
                                'phone': phone,
                                'name': name,
                                'message': personalized_message
                            })
                    
                    except Exception as e:
                        continue  # Mesaj hazırlanamadı, devam et
                        
                except Exception as e:
                    continue  # Satır işlenirken hata, devam et
            
            # WhatsApp linklerini oluştur ve göster
            self.show_whatsapp_links(messages)
            
        except Exception as e:
            messagebox.showerror("Hata", f"Toplu mesaj hazırlanamadı: {str(e)}")
    
    def auto_send_messages(self):
        """Mesajları gerçekten gönder"""
        try:
            message_content = self.message_text.get('1.0', 'end-1c')
            if not message_content.strip():
                messagebox.showerror("Hata", "Mesaj içeriği boş olamaz!")
                return
            
            # İlk bilgilendirme mesajı
            info_result = messagebox.showinfo(
                "📱 WhatsApp Web Açılacak", 
                f"🚀 Otomatik mesaj gönderimi başlatılacak!\n\n"
                f"📊 Toplam {len(self.df)} işletmeye mesaj gönderilecek\n"
                f"🌐 WhatsApp Web açılacak\n"
                f"📱 QR kod okutmanız için 15 saniye süreniz var\n"
                f"⏰ Sonra otomatik mesajlar gönderilecek\n\n"
                f"Devam etmek için 'Tamam' butonuna basın"
            )
            
            # Onay al
            result = messagebox.askyesno(
                "Onay", 
                f"Toplam {len(self.df)} işletmeye gerçek mesaj gönderilecek!\n"
                f"📱 Mesajlar WhatsApp Web'de gönderilecek\n"
                f"⚠️ Bu işlem geri alınamaz!\n\n"
                f"Devam etmek istiyor musunuz?"
            )
            
            if not result:
                return
            
            # Butonları devre dışı bırak
            self.auto_send_button.config(state='disabled', text="⏳ Gönderiliyor...")
            self.send_button.config(state='disabled')
            
            # Arka planda çalıştır
            threading.Thread(target=self._auto_send_worker, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Mesaj gönderimi başlatılamadı: {str(e)}")
            self.auto_send_button.config(state='normal', text="🚀 Otomatik Gönder")
            self.send_button.config(state='normal')
    
    def _send_whatsapp_message_normal(self, phone_no, message):
        """WhatsApp mesajını aynı sekmede gönder - SELENIUM YÖNTEMİ"""
        try:
            # WhatsApp Web URL'sini oluştur
            clean_phone = phone_no.replace('+', '').replace(' ', '')
            whatsapp_url = f"https://web.whatsapp.com/send?phone={clean_phone}&text={message.replace(' ', '%20').replace('\n', '%0A')}"
            
            # Mevcut driver'ı kullan (aynı sekmede)
            if hasattr(self, 'whatsapp_driver') and self.whatsapp_driver is not None:
                # Aynı sekmede URL'yi aç
                self.whatsapp_driver.get(whatsapp_url)
                time.sleep(5)  # WhatsApp'ın tam yüklenmesi için bekleme süresi
                
                # Mesaj alanını doldurduktan hemen sonra Enter tuşuna bas
                pyautogui.press('enter')
                return True
            else:
                return False
            
        except Exception as e:
            return False
    
    def _auto_send_worker(self):
        """Otomatik gönderim işçi fonksiyonu - SELENIUM İLE AYNI SEKME"""
        try:
            message_content = self.message_text.get('1.0', 'end-1c')
            success_count = 0
            error_count = 0
            
            # Selenium driver'ı başlat (WhatsApp için)
            try:
                from selenium import webdriver
                from selenium.webdriver.chrome.service import Service
                from selenium.webdriver.chrome.options import Options
                from webdriver_manager.chrome import ChromeDriverManager
                
                # Chrome seçenekleri
                chrome_options = Options()
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                
                # WhatsApp driver'ı oluştur
                service = Service(ChromeDriverManager().install())
                self.whatsapp_driver = webdriver.Chrome(service=service, options=chrome_options)
                
                # WhatsApp Web'i aç
                self.whatsapp_driver.get("https://web.whatsapp.com")
                time.sleep(15)  # WhatsApp Web'in tam yüklenmesi ve QR kod okutma için 15 saniye bekleme
            except Exception as e:
                return
            
            for index, row in self.df.iterrows():
                try:
                    # Boş satırları atla
                    if row.isnull().all() or row.empty:
                        continue
                    
                    # İşletme adı kontrolü - eğer ad yoksa atla
                    business_name = row.get('Ad') or row.get('İsim') or row.get('Name') or row.get('İşletme Adı') or row.get('Business Name')
                    
                    if not business_name or str(business_name).strip() == '' or str(business_name).lower() == 'nan':
                        continue
                    
                    # Telefon numarasını al
                    phone = self._extract_phone(row)
                    if not phone:
                        error_count += 1
                        continue
                    
                    # Telefon numarasını temizle (ülke kodu ekle)
                    clean_phone = self._clean_phone_number(phone)
                    if not clean_phone:
                        error_count += 1
                        continue
                    
                    # Mesajı kişiselleştir
                    personalized_message = self._personalize_message(message_content, row)
                    
                    # Normal Chrome penceresinde mesaj gönder
                    if self._send_whatsapp_message_normal(clean_phone, personalized_message):
                        # Sayfa yenile (sonraki mesaj için) - Selenium ile
                        time.sleep(2)  # Enter tuşunun işlenmesi için bekleme süresi
                        if hasattr(self, 'whatsapp_driver') and self.whatsapp_driver is not None:
                            self.whatsapp_driver.refresh()  # Selenium ile sayfa yenile
                        time.sleep(3)  # Sayfa yenilenmesi için bekleme süresi
                        
                        success_count += 1
                        
                        # Hemen sonraki mesaja geç
                        if index < len(self.df) - 1:  # Son mesaj değilse
                            pass  # Sonraki mesaja geç
                    else:
                        error_count += 1
                        
                except Exception as e:
                    error_count += 1
                    continue
            
            # Sonuçları göster
            self.window.after(0, lambda: self._show_auto_send_results(success_count, error_count))
            
        except Exception as e:
            self.window.after(0, lambda: messagebox.showerror("Hata", f"Otomatik gönderim hatası: {str(e)}"))
        finally:
            # WhatsApp driver'ı kapat
            if hasattr(self, 'whatsapp_driver') and self.whatsapp_driver is not None:
                try:
                    self.whatsapp_driver.quit()
                    pass  # WhatsApp driver kapatıldı
                except:
                    pass
            
            # Butonları tekrar aktif et
            self.window.after(0, lambda: self.auto_send_button.config(state='normal', text="🚀 Otomatik Gönder"))
            self.window.after(0, lambda: self.send_button.config(state='normal'))
    
    def _extract_phone(self, row):
        """Telefon numarasını çıkar"""
        # Tüm sütunları kontrol et
        for col_name, value in row.items():
            if pd.isna(value) or value is None:
                continue
                
            value_str = str(value).strip()
            
            # Boş değerleri atla
            if not value_str or value_str in ['nan', 'None', '']:
                continue
            
            # Telefon numarası olabilecek değerleri kontrol et
            # Sadece rakam, +, -, (, ), boşluk içeren değerler
            if self._looks_like_phone(value_str):
                return value_str
        
        return None
    
    def _looks_like_phone(self, text):
        """Metnin telefon numarası gibi görünüp görünmediğini kontrol et"""
        if not text:
            return False
        
        # Sadece rakam, +, -, (, ), boşluk içermeli
        allowed_chars = set('0123456789+-() ')
        if not all(c in allowed_chars for c in text):
            return False
        
        # En az 7 rakam içermeli
        digits = ''.join(filter(str.isdigit, text))
        if len(digits) < 7:
            return False
        
        # Çok uzun olmamalı (maksimum 15 karakter)
        if len(text) > 15:
            return False
        
        # Adres gibi görünen metinleri filtrele
        address_indicators = ['cd', 'sok', 'mah', 'no:', 'kat', 'daire', 'apartman', 'bulvar', 'cadde']
        text_lower = text.lower()
        if any(indicator in text_lower for indicator in address_indicators):
            return False
        
        return True
    
    def _personalize_message(self, message_content, row):
        """Mesajı kişiselleştir"""
        # İsim
        if 'Unnamed: 1' in row and row['Unnamed: 1'] != 'Ad':
            name = str(row.get('Unnamed: 1', 'Değerli Müşteri'))
        else:
            name = (row.get('Ad') or row.get('Name') or 
                   row.get('İsim') or row.get('İşletme') or 'Değerli Müşteri')
        
        # Adres
        if 'Unnamed: 3' in row and row['Unnamed: 3'] != 'Adres':
            address = str(row.get('Unnamed: 3', 'Adres bilgisi yok'))
        else:
            address = (row.get('Adres') or row.get('Address') or 
                      row.get('Konum') or row.get('Location') or 'Adres bilgisi yok')
        
        # Puan
        if 'Unnamed: 4' in row and row['Unnamed: 4'] != 'Puan/Yorum':
            rating = str(row.get('Unnamed: 4', 'Puan bilgisi yok'))
        else:
            rating = (row.get('Puan/Yorum') or row.get('Rating') or 
                     row.get('Puan') or row.get('Score') or 'Puan bilgisi yok')
        
        # Telefon
        phone = self._extract_phone(row) or 'Telefon bilgisi yok'
        
        return message_content.format(
            isim=name,
            isletme_adi=name,
            adres=address,
            telefon=phone,
            puan=rating
        )
    
    def _clean_phone_number(self, phone):
        """Telefon numarasını temizle ve ülke kodu ekle"""
        if not phone:
            return None
            
        # Sadece rakamları al
        clean_phone = ''.join(filter(str.isdigit, str(phone)))
        
        # Boş ise None döndür
        if not clean_phone:
            return None
        
        # Türkiye için +90 ekle (eğer yoksa)
        if clean_phone.startswith('90') and len(clean_phone) == 12:
            return '+' + clean_phone
        elif clean_phone.startswith('0') and len(clean_phone) == 11:
            return '+90' + clean_phone[1:]
        elif len(clean_phone) == 10:
            return '+90' + clean_phone
        elif len(clean_phone) == 11 and not clean_phone.startswith('0'):
            return '+90' + clean_phone
        
        # Geçersiz format
        return None
    
    def _show_auto_send_results(self, success_count, error_count):
        """Otomatik gönderim sonuçlarını göster"""
        messagebox.showinfo(
            "Gönderim Tamamlandı",
            f"✅ Gönderildi: {success_count} mesaj\n"
            f"❌ Hatalı: {error_count} mesaj\n\n"
            f"Toplam: {success_count + error_count} işletme\n\n"
            f"📱 Mesajlar gerçekten gönderildi\n"
            f"⏰ WhatsApp Web'de kontrol edebilirsiniz"
        )
    
    def show_whatsapp_links(self, messages):
        """WhatsApp linklerini göster"""
        try:
            # Yeni pencere oluştur
            link_window = tk.Toplevel(self.window)
            link_window.title("📱 WhatsApp Mesaj Linkleri")
            link_window.geometry("900x700")
            link_window.configure(bg='#F5F5F5')
            
            # Pencereyi ortala
            self.center_window(link_window)
            
            # Başlık
            title_label = tk.Label(
                link_window,
                text=f"📱 {len(messages)} WhatsApp Mesaj Linki Hazırlandı",
                font=('Segoe UI', 16, 'bold'),
                bg='#F5F5F5',
                fg='#2E86AB'
            )
            title_label.pack(pady=20)
            
            # Açıklama
            info_label = tk.Label(
                link_window,
                text="Linklere tıklayarak WhatsApp'ta mesaj gönderebilirsiniz:",
                font=('Segoe UI', 12),
                bg='#F5F5F5',
                fg='#666666'
            )
            info_label.pack(pady=10)
            
            # Ana frame
            main_frame = tk.Frame(link_window, bg='#F5F5F5')
            main_frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            # Scrollbar
            scrollbar = tk.Scrollbar(main_frame)
            scrollbar.pack(side='right', fill='y')
            
            # Canvas
            canvas = tk.Canvas(main_frame, bg='#F5F5F5', yscrollcommand=scrollbar.set)
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.config(command=canvas.yview)
            
            # Frame for content
            content_frame = tk.Frame(canvas, bg='#F5F5F5')
            canvas.create_window((0, 0), window=content_frame, anchor='nw')
            
            # Her mesaj için link oluştur
            for i, msg in enumerate(messages, 1):
                # Mesaj frame'i
                msg_frame = tk.Frame(content_frame, bg='white', relief='solid', bd=1)
                msg_frame.pack(fill='x', padx=5, pady=5)
                
                # İsim ve telefon
                name_label = tk.Label(
                    msg_frame,
                    text=f"{i}. {msg['name']} - {msg['phone']}",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white',
                    fg='#2E86AB'
                )
                name_label.pack(anchor='w', padx=10, pady=5)
                
                # Mesaj önizleme
                preview_text = msg['message'][:100] + "..." if len(msg['message']) > 100 else msg['message']
                preview_label = tk.Label(
                    msg_frame,
                    text=f"Mesaj: {preview_text}",
                    font=('Segoe UI', 10),
                    bg='white',
                    fg='#666666',
                    wraplength=800,
                    justify='left'
                )
                preview_label.pack(anchor='w', padx=10, pady=2)
                
                # WhatsApp link butonu - telefon numarasını düzelt
                clean_phone = ''.join(filter(str.isdigit, msg['phone']))
                # Türkiye telefon numarası formatı (90 ile başlamalı)
                if clean_phone.startswith('0'):
                    clean_phone = '90' + clean_phone[1:]  # 0'ı kaldır, 90 ekle
                elif not clean_phone.startswith('90'):
                    clean_phone = '90' + clean_phone  # 90 ekle
                
                whatsapp_link = f"https://wa.me/{clean_phone}?text={msg['message'].replace(' ', '%20').replace('\n', '%0A')}"
                
                link_button = tk.Button(
                    msg_frame,
                    text="📱 WhatsApp'ta Aç",
                    font=('Segoe UI', 11, 'bold'),
                    bg='#25D366',
                    fg='white',
                    relief='flat',
                    bd=0,
                    padx=20,
                    pady=8,
                    command=lambda link=whatsapp_link: self.open_whatsapp_link(link),
                    cursor='hand2'
                )
                link_button.pack(anchor='w', padx=10, pady=5)
            
            # Canvas scroll ayarı
            content_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
            
            # Butonlar
            button_frame = tk.Frame(link_window, bg='#F5F5F5')
            button_frame.pack(pady=20)
            
            # Tümünü aç butonu
            open_all_button = tk.Button(
                button_frame,
                text="🚀 Tümünü Aç",
                font=('Segoe UI', 12, 'bold'),
                bg='#E8F8F5',    # Soft yeşil (WhatsApp teması)
                fg='#1B5E20',    # Koyu yeşil yazı
                relief='flat',
                bd=1,
                padx=25,         # Eşit boyut için
                pady=12,         # Eşit boyut için
                command=lambda: self.open_all_whatsapp_links(messages),
                cursor='hand2',
                activebackground='#D4F4E6',  # Hover efekti
                activeforeground='#0D3D0D'
            )
            open_all_button.pack(side='left', padx=10)
            
            # Kapat butonu
            close_button = tk.Button(
                button_frame,
                text="❌ Kapat",
                font=('Segoe UI', 12, 'bold'),
                bg='#FFEBEE',    # Soft kırmızı (kapatma)
                fg='#C62828',    # Koyu kırmızı yazı
                relief='flat',
                bd=1,
                padx=25,         # Eşit boyut için
                pady=12,         # Eşit boyut için
                command=link_window.destroy,
                cursor='hand2',
                activebackground='#FFCDD2',  # Hover efekti
                activeforeground='#B71C1C'
            )
            close_button.pack(side='left', padx=10)
            
            # Butonlara hover efektleri ekle
            open_all_button.bind("<Enter>", lambda e: open_all_button.config(bg='#D4F4E6'))
            open_all_button.bind("<Leave>", lambda e: open_all_button.config(bg='#E8F8F5'))
            
            close_button.bind("<Enter>", lambda e: close_button.config(bg='#FFCDD2'))
            close_button.bind("<Leave>", lambda e: close_button.config(bg='#FFEBEE'))
            
        except Exception as e:
            messagebox.showerror("Hata", f"Link penceresi gösterilemedi: {str(e)}")
    
    def open_whatsapp_link(self, link):
        """WhatsApp linkini aç"""
        try:
            import webbrowser
            webbrowser.open(link)
        except Exception as e:
            messagebox.showerror("Hata", f"Link açılamadı: {str(e)}")
    
    def open_all_whatsapp_links(self, messages):
        """Tüm WhatsApp linklerini aç"""
        try:
            import webbrowser
            import time
            
            for i, msg in enumerate(messages):
                # Telefon numarasını düzelt
                clean_phone = ''.join(filter(str.isdigit, msg['phone']))
                # Türkiye telefon numarası formatı (90 ile başlamalı)
                if clean_phone.startswith('0'):
                    clean_phone = '90' + clean_phone[1:]  # 0'ı kaldır, 90 ekle
                elif not clean_phone.startswith('90'):
                    clean_phone = '90' + clean_phone  # 90 ekle
                
                whatsapp_link = f"https://wa.me/{clean_phone}?text={msg['message'].replace(' ', '%20').replace('\n', '%0A')}"
                webbrowser.open(whatsapp_link)
                
                # Linkler arası bekleme
                if i < len(messages) - 1:
                    time.sleep(2)
            
            messagebox.showinfo("Başarılı", f"{len(messages)} WhatsApp linki açıldı!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Linkler açılamadı: {str(e)}")
    


def main():
    """Ana fonksiyon"""
    root = tk.Tk()
    
    # Modern tema ayarları
    style = ttk.Style()
    style.theme_use('clam')
    
    # Uygulamayı başlat
    app = ModernScraperGUI(root)
    
    # Pencereyi ortala
    app.center_window(root)
    
    # Uygulamayı çalıştır
    root.mainloop()

if __name__ == "__main__":
    main()
