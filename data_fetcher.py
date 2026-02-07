import yfinance as yf
import json

def verileri_cek():
    # Takip etmek istediğin hisseler
    hisseler = ["THYAO.IS", "TUPRS.IS", "ASELS.IS", "EREGL.IS", "AKBNK.IS", "BIMAS.IS", "SASAD.IS"]
    sonuc_listesi = []

    print("Borsa verileri çekiliyor...")

    for sembol in hisseler:
        try:
            hisse = yf.Ticker(sembol)
            # 5 günlük veri çek (Hafta sonu boşluğunu kapatmak için en güvenli yol)
            data = hisse.history(period="5d")
            
            if len(data) < 2:
                continue

            fiyat = data['Close'].iloc[-1]
            onceki_fiyat = data['Close'].iloc[-2]
            degisim = round(((fiyat - onceki_fiyat) / onceki_fiyat) * 100, 2)
            
            # Renk: Artış varsa yeşil, düşüş varsa kırmızı
            renk = "#22c55e" if degisim >= 0 else "#ef4444"

            sonuc_listesi.append({
                "x": sembol.replace(".IS", ""), # Ekranda 'THYAO.IS' yerine 'THYAO' yazar
                "y": abs(degisim) + 1,          # Kutunun büyüklüğü
                "d": degisim,                   # Gerçek değişim oranı
                "f": round(fiyat, 2),           # Güncel fiyat
                "fillColor": renk
            })
            print(f"Başarılı: {sembol}")
        except Exception as e:
            print(f"Hata oluştu ({sembol}): {e}")

    # Verileri data.json dosyasına kaydet
    with open("data.json", "w") as f:
        json.dump(sonuc_listesi, f)
    
    print("\n--- İŞLEM TAMAM ---")
    print("data.json dosyası başarıyla oluşturuldu.")

# Kodu çalıştıran ana kısım
if __name__ == "__main__":
    verileri_cek()