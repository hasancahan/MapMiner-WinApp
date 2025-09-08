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
import pywhatkit as pwk
import time
from datetime import datetime, timedelta
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
        """Pencereyi ekranın ortasında konumlandır"""
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (window.winfo_width() // 2)
        y = (window.winfo_screenheight() // 2) - (window.winfo_height() // 2)
        window.geometry(f"+{x}+{y}")
        
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
            bg='#2E8B57',    # Deniz yeşili
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            command=self.start_search,
            cursor='hand2',
            activebackground='#228B22',
            activeforeground='white'
        )
        self.start_button.pack(side='left', padx=(0, 8))
        
        # Durdur butonu - modern ve şık
        self.stop_button = tk.Button(
            button_frame,
            text="DURDUR",
            font=('Segoe UI', 11, 'bold'),
            bg='#DC143C',    # Koyu kırmızı
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            command=self.stop_search,
            state='disabled',
            cursor='hand2',
            activebackground='#B22222',
            activeforeground='white'
        )
        self.stop_button.pack(side='left', padx=(0, 8))
        
        # Excel'e kaydet butonu - modern ve şık
        self.save_button = tk.Button(
            button_frame,
            text="KAYDET",
            font=('Segoe UI', 11, 'bold'),
            bg='#4169E1',    # Kraliyet mavisi
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            command=self.save_to_excel,
            state='disabled',
            cursor='hand2',
            activebackground='#1E90FF',
            activeforeground='white'
        )
        self.save_button.pack(side='left', padx=(0, 8))
        
        # Toplu mesaj gönder butonu - modern ve şık
        self.bulk_message_button = tk.Button(
            button_frame,
            text="TOPLU MESAJ",
            font=('Segoe UI', 11, 'bold'),
            bg='#8A2BE2',    # Mavi menekşe
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            command=self.open_bulk_message_window,
            cursor='hand2',
            activebackground='#9370DB',
            activeforeground='white'
        )
        self.bulk_message_button.pack(side='right')
        
        # Butonlara modern efektler ekle
        self.add_button_effects()
        
    def add_button_effects(self):
        """Butonlara modern efektler ekle"""
        try:
            # Butonlara hover efekti ekle
            self.start_button.bind("<Enter>", lambda e: self.start_button.config(bg='#228B22'))
            self.start_button.bind("<Leave>", lambda e: self.start_button.config(bg='#2E8B57'))
            
            self.stop_button.bind("<Enter>", lambda e: self.stop_button.config(bg='#B22222'))
            self.stop_button.bind("<Leave>", lambda e: self.stop_button.config(bg='#DC143C'))
            
            self.save_button.bind("<Enter>", lambda e: self.save_button.config(bg='#1E90FF'))
            self.save_button.bind("<Leave>", lambda e: self.save_button.config(bg='#4169E1'))
            
            self.bulk_message_button.bind("<Enter>", lambda e: self.bulk_message_button.config(bg='#9370DB'))
            self.bulk_message_button.bind("<Leave>", lambda e: self.bulk_message_button.config(bg='#8A2BE2'))
            
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
            
            # Scraper'ı oluştur - her zaman görünür mod
            self.scraper = GoogleMapsScraper(headless=False)
            
            # Arama yap
            success = self.scraper.search_businesses(
                query=query,
                location=location,
                max_results=max_results,
                detailed_info=True
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
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Excel dosyasını kaydet"
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
        

class BulkMessageWindow:
    """Toplu mesaj gönderme penceresi"""
    
    def center_window(self, window):
        """Pencereyi ekranın ortasında konumlandır"""
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (window.winfo_width() // 2)
        y = (window.winfo_screenheight() // 2) - (window.winfo_height() // 2)
        window.geometry(f"+{x}+{y}")
    
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
            bg='#25D366',
            fg='white',
            relief='flat',
            bd=2,
            padx=20,
            pady=10,
            command=self.send_bulk_messages,
            cursor='hand2',
            state='disabled'
        )
        self.send_button.pack(side='left', padx=10, fill='x', expand=True)
        
        # Otomatik gönder butonu
        self.auto_send_button = tk.Button(
            button_frame,
            text="🚀 Otomatik Gönder",
            font=('Segoe UI', 12, 'bold'),
            bg='#FF6B35',
            fg='white',
            relief='flat',
            bd=2,
            padx=20,
            pady=10,
            command=self.auto_send_messages,
            cursor='hand2',
            state='disabled'
        )
        self.auto_send_button.pack(side='left', padx=5, fill='x', expand=True)
        
        # Kapat butonu
        close_button = tk.Button(
            button_frame,
            text="❌ Kapat",
            font=('Segoe UI', 14, 'bold'),
            bg='#DC3545',
            fg='white',
            relief='flat',
            bd=2,
            padx=40,
            pady=15,
            command=self.window.destroy,
            cursor='hand2'
        )
        close_button.pack(side='right', padx=20, fill='x', expand=True)
        
    def load_excel_data(self):
        """Excel verilerini yükle"""
        try:
            import pandas as pd
            self.df = pd.read_excel(self.excel_file)
            print(f"✅ {len(self.df)} işletme verisi yüklendi")
            print(f"📊 Excel sütunları: {list(self.df.columns)}")
            
            # İlk satırı göster
            if len(self.df) > 0:
                print(f"📋 İlk satır örneği: {dict(self.df.iloc[0])}")
            
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
                    print(f"Excel sütunları: {list(self.df.columns)}")
                    print(f"Satır verisi: {dict(row)}")
                    
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
                    print(f"Mesaj hazırlanamadı: {e}")
                    continue
            
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
            
            # Onay al
            result = messagebox.askyesno(
                "Onay", 
                f"Toplam {len(self.df)} işletmeye gerçek mesaj gönderilecek!\n"
                f"📱 Mesajlar pywhatkit ile gönderilecek\n"
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
                print(f"📤 Enter tuşuna basıldı - mesaj gönderildi: {phone_no}")
                
                return True
            else:
                print("❌ WhatsApp driver bulunamadı")
                return False
            
        except Exception as e:
            print(f"❌ Mesaj gönderilemedi: {e}")
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
                print("✅ WhatsApp Web açıldı, mesajlar gönderilmeye başlanıyor...")
                time.sleep(10)  # WhatsApp Web'in tam yüklenmesi için 10 saniye bekleme
            except Exception as e:
                print(f"WhatsApp Web açılamadı: {e}")
                return
            
            for index, row in self.df.iterrows():
                try:
                    # Telefon numarasını al
                    phone = self._extract_phone(row)
                    if not phone:
                        print(f"⚠️ Telefon numarası bulunamadı: {dict(row)}")
                        error_count += 1
                        continue
                    
                    # Telefon numarasını temizle (ülke kodu ekle)
                    clean_phone = self._clean_phone_number(phone)
                    if not clean_phone:
                        print(f"⚠️ Geçersiz telefon numarası: {phone}")
                        error_count += 1
                        continue
                    
                    # Mesajı kişiselleştir
                    personalized_message = self._personalize_message(message_content, row)
                    
                    print(f"📱 Mesaj gönderiliyor: {clean_phone}")
                    
                    # Normal Chrome penceresinde mesaj gönder
                    if self._send_whatsapp_message_normal(clean_phone, personalized_message):
                        # Sayfa yenile (sonraki mesaj için) - Selenium ile
                        time.sleep(2)  # Enter tuşunun işlenmesi için bekleme süresi
                        if hasattr(self, 'whatsapp_driver') and self.whatsapp_driver is not None:
                            self.whatsapp_driver.refresh()  # Selenium ile sayfa yenile
                        time.sleep(3)  # Sayfa yenilenmesi için bekleme süresi
                        print(f"🔄 Sayfa yenilendi - sonraki mesaj için hazır")
                        
                        success_count += 1
                        print(f"✅ Mesaj başarıyla gönderildi: {clean_phone}")
                        
                        # Hemen sonraki mesaja geç
                        if index < len(self.df) - 1:  # Son mesaj değilse
                            print(f"⚡ Sonraki mesaja geçiliyor...")
                    else:
                        error_count += 1
                        
                except Exception as e:
                    print(f"❌ Mesaj gönderilemedi ({phone}): {str(e)}")
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
                    print("✅ WhatsApp driver kapatıldı")
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
                print(f"📱 Telefon numarası bulundu: {col_name} = {value_str}")
                return value_str
        
        print(f"⚠️ Telefon numarası bulunamadı. Mevcut sütunlar: {list(row.index)}")
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
        print(f"⚠️ Geçersiz telefon formatı: {phone} -> {clean_phone}")
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
                bg='#25D366',
                fg='white',
                relief='flat',
                bd=0,
                padx=30,
                pady=12,
                command=lambda: self.open_all_whatsapp_links(messages),
                cursor='hand2'
            )
            open_all_button.pack(side='left', padx=10)
            
            # Kapat butonu
            close_button = tk.Button(
                button_frame,
                text="❌ Kapat",
                font=('Segoe UI', 12, 'bold'),
                bg='#DC3545',
                fg='white',
                relief='flat',
                bd=0,
                padx=30,
                pady=12,
                command=link_window.destroy,
                cursor='hand2'
            )
            close_button.pack(side='left', padx=10)
            
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
