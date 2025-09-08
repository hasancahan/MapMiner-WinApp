@echo off
echo ========================================
echo Google Maps Scraper Kurulum Scripti
echo ========================================
echo.

echo Python kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo HATA: Python yuklu degil!
    echo Lutfen Python 3.7+ yukleyin: https://python.org
    pause
    exit /b 1
)

echo Python bulundu!
echo.

echo Gerekli paketler yukleniyor...
pip install -r requirements.txt

if errorlevel 1 (
    echo HATA: Paketler yuklenemedi!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Kurulum tamamlandi!
echo ========================================
echo.
echo Kullanmak icin: python main.py
echo.
pause
