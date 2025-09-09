#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loading Screen for Google Maps Scraper
"""

import tkinter as tk
from tkinter import ttk
import threading
import time

class LoadingScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Yükleniyor...")
        self.root.geometry("900x800")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)
        
        # Pencereyi her zaman üstte tut
        self.root.attributes('-topmost', True)
        
        # Loading ekranını oluştur
        self.create_loading_screen()
        
        # İçerikler eklendikten sonra pencereyi ortala - çoklu güvenlik
        self.root.after(100, self.center_window)
        self.root.after(500, self.center_window)  # Ek güvenlik
        self.root.after(1000, self.center_window)  # Son güvenlik
        
        # 5 saniye sonra ana uygulamayı başlat
        self.start_main_app_after_delay()
        
    def center_window(self, window=None):
        """Pencereyi ekranın ortasında konumlandır - EXE uyumlu"""
        if window is None:
            window = self.root
        
        # Pencere boyutlarını güncelle
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
        
        # Pencereyi güncelle
        window.update()
        
    def create_loading_screen(self):
        """Loading ekranını oluştur - Modern ve Profesyonel"""
        # Ana frame - sabit boyut
        main_frame = tk.Frame(self.root, bg='#1a1a2e', width=900, height=800)
        main_frame.pack_propagate(False)
        main_frame.pack(expand=True, fill='both')
        
        # Ana içerik - tek renk
        content_frame = tk.Frame(main_frame, bg='#1a1a2e', height=800)
        content_frame.pack(fill='both', expand=True)
        content_frame.pack_propagate(False)
        
        # Logo container - sabit boyut ve ortalanmış
        logo_container = tk.Frame(content_frame, bg='#ffffff', relief='flat', bd=0, width=800, height=400)
        logo_container.pack_propagate(False)
        logo_container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Gölge efekti için border
        logo_container.configure(highlightbackground='#e0e0e0', highlightthickness=1)
        
        # İçerik frame - sabit boyut
        inner_frame = tk.Frame(logo_container, bg='#ffffff', width=760, height=360)
        inner_frame.pack_propagate(False)
        inner_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Modern ikon - sabit konum
        icon_label = tk.Label(
            inner_frame,
            text="🗺️",
            font=('Segoe UI', 64),
            bg='#ffffff',
            fg='#2E86AB'
        )
        icon_label.place(relx=0.58, y=40, anchor='center')
        
        # Ana başlık - sabit konum
        title_label = tk.Label(
            inner_frame,
            text="Google Maps Scraper",
            font=('Segoe UI', 24, 'bold'),
            bg='#ffffff',
            fg='#1a1a2e',
            justify='center'
        )
        title_label.place(relx=0.5, y=120, anchor='center')
        
        # Alt başlık - sabit konum
        subtitle_label = tk.Label(
            inner_frame,
            text="İşletme Veri Toplama Aracı",
            font=('Segoe UI', 14),
            bg='#ffffff',
            fg='#666666',
            justify='center'
        )
        subtitle_label.place(relx=0.5, y=160, anchor='center')
        
        # Loading metni - sabit konum
        loading_label = tk.Label(
            inner_frame,
            text="Uygulama başlatılıyor...",
            font=('Segoe UI', 12),
            bg='#ffffff',
            fg='#2E86AB',
            justify='center'
        )
        loading_label.place(relx=0.5, y=200, anchor='center')
        
        # Progress bar - sabit konum
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            inner_frame,
            variable=self.progress_var,
            maximum=100,
            length=350,
            mode='determinate'
        )
        self.progress_bar.place(relx=0.5, y=250, anchor='center')
        
        # Modern progress bar stili
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Modern.Horizontal.TProgressbar", 
                       background='#2E86AB',
                       troughcolor='#f0f0f0',
                       borderwidth=0,
                       lightcolor='#2E86AB',
                       darkcolor='#2E86AB',
                       relief='flat')
        self.progress_bar.configure(style="Modern.Horizontal.TProgressbar")
        
        # Durum etiketi - sabit konum
        self.status_label = tk.Label(
            inner_frame,
            text="Başlatılıyor...",
            font=('Segoe UI', 10),
            bg='#ffffff',
            fg='#888888',
            justify='center'
        )
        self.status_label.place(relx=0.5, y=290, anchor='center')
        
        # Alt bilgi - sabit konum
        info_label = tk.Label(
            inner_frame,
            text="Lütfen bekleyiniz...",
            font=('Segoe UI', 9),
            bg='#ffffff',
            fg='#aaaaaa',
            justify='center'
        )
        info_label.place(relx=0.5, y=320, anchor='center')
        
        # HdynamicX yapımı etiketi - en altta
        hdynamic_label = tk.Label(
            inner_frame,
            text="Made by HDynamicX",
            font=('Segoe UI', 10, 'bold'),
            bg='#ffffff',
            fg='#2E86AB',
            justify='center'
        )
        hdynamic_label.place(relx=0.5, y=350, anchor='center')
        
        # Progress animasyonu başlat
        self.animate_progress()
        
    def animate_progress(self):
        """Progress bar animasyonu"""
        def update_progress():
            for i in range(101):
                # Thread-safe UI güncelleme
                self.root.after(0, self._update_progress_ui, i)
                time.sleep(0.05)  # 5 saniye / 100 = 0.05 saniye
                
        # Animasyonu thread'de çalıştır
        progress_thread = threading.Thread(target=update_progress, daemon=True)
        progress_thread.start()
        
    def _update_progress_ui(self, progress):
        """UI'yi güncelle (main thread'de çalışır)"""
        try:
            self.progress_var.set(progress)
            self.update_status_text(progress)
        except:
            pass  # Pencere kapatılmışsa hata verme
        
    def update_status_text(self, progress):
        """Durum metnini güncelle"""
        if progress < 20:
            self.status_label.config(text="Modüller yükleniyor...")
        elif progress < 40:
            self.status_label.config(text="Arayüz hazırlanıyor...")
        elif progress < 60:
            self.status_label.config(text="Veritabanı bağlantısı kuruluyor...")
        elif progress < 80:
            self.status_label.config(text="Sistem kontrolü yapılıyor...")
        elif progress < 100:
            self.status_label.config(text="Son hazırlıklar...")
        else:
            self.status_label.config(text="Hazır!")
            
    def start_main_app_after_delay(self):
        """5 saniye sonra ana uygulamayı başlat"""
        def start_main():
            time.sleep(5)  # 5 saniye bekle
            self.root.after(0, self.launch_main_app)
            
        # Thread'de bekle
        delay_thread = threading.Thread(target=start_main, daemon=True)
        delay_thread.start()
        
    def launch_main_app(self):
        """Ana uygulamayı başlat"""
        try:
            # Loading ekranını kapat
            self.root.destroy()
            
            # Ana uygulamayı import et ve başlat
            from modern_gui import main as gui_main
            gui_main()
            
        except Exception as e:
            # Hata durumunda loading ekranını kapat ve hata göster
            self.root.destroy()
            import tkinter.messagebox as mb
            mb.showerror("Hata", f"Uygulama başlatılamadı: {str(e)}")
            
    def run(self):
        """Loading ekranını çalıştır"""
        self.root.mainloop()

def main():
    """Loading ekranını başlat"""
    loading = LoadingScreen()
    loading.run()

if __name__ == "__main__":
    main()
