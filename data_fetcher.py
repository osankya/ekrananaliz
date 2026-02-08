import yfinance as yf
import json
import pandas as pd
import numpy as np

# --- AYARLAR ---
BIST100_SEKTORLER = {
    "BANKA": ["AKBNK.IS", "GARAN.IS", "ISCTR.IS", "YKBNK.IS", "VAKBN.IS"],
    "HOLDİNG": ["KCHOL.IS", "SAHOL.IS", "SISE.IS", "DOHOL.IS"],
    "HAVACILIK": ["THYAO.IS", "PGSUS.IS", "TAVHL.IS"],
    "SANAYİ": ["TUPRS.IS", "EREGL.IS", "ASELS.IS", "FROTO.IS", "SASA.IS"],
    "PERAKENDE": ["BIMAS.IS", "MGROS.IS", "SOKM.IS"],
    "ENERJİ": ["ASTOR.IS", "EUPWR.IS", "SMRTG.IS", "ODAS.IS"]
}

TUM_HISSELER = [item for sublist in BIST100_SEKTORLER.values() for item in sublist]

def calculate_fear_greed():
    """BIST 100 için Korku ve Açgözlülük Endeksi Hesaplar (0-100)"""
    try:
        # BIST 100 Endeksini Çek (XU100.IS)
        xu100 = yf.Ticker("XU100.IS").history(period="3mo")
        if len(xu100) < 50: return 50 # Veri yoksa nötr dön

        # 1. RSI Hesapla (14 Günlük) - Ağırlık %60
        delta = xu100['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]

        # 2. Trend (Fiyat vs 50 Günlük Ortalama) - Ağırlık %40
        sma50 = xu100['Close'].rolling(window=50).mean().iloc[-1]
        price = xu100['Close'].iloc[-1]
        trend_score = 50 + ((price - sma50) / sma50) * 100
        trend_score = max(0, min(100, trend_score)) # 0-100 arasına sıkıştır

        # Nihai Skor
        final_score = (rsi * 0.6) + (trend_score * 0.4)
        return int(final_score)
    except Exception as e:
        print(f"Korku endeksi hatası: {e}")
        return 50

def get_stock_data(symbol):
    try:
        t = yf.Ticker(symbol)
        hist = t.history(period="5d")
        if len(hist) < 2: return None
        
        # Son fiyat ve değişim
        last_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2]
        change_pct = ((last_price - prev_price) / prev_price) * 100
        
        # Market Cap (Hata önleyici)
        info = t.info
        mcap = info.get('marketCap')
        if mcap is None:
            mcap = last_price * info.get('sharesOutstanding', 1000000)

        return {
            "x": symbol.replace(".IS", ""),
            "y": round(change_pct, 2),
            "z": int(mcap) # Treemap büyüklüğü için
        }
    except:
        return None

def main():
    print("Veriler çekiliyor, lütfen bekleyin...")
    
    # 1. Heatmap Verileri
    heatmap_data = []
    for sektor, hisseler in BIST100_SEKTORLER.items():
        data_points = []
        for hisse in hisseler:
            d = get_stock_data(hisse)
            if d: data_points.append(d)
        
        if data_points:
            heatmap_data.append({"name": sektor, "data": data_points})
    
    # 2. Korku Endeksi
    fear_score = calculate_fear_greed()
    
    # Dosyaları Kaydet
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(heatmap_data, f, ensure_ascii=False)
        
    with open('fear_index.json', 'w', encoding='utf-8') as f:
        json.dump({"score": fear_score}, f)
        
    print(f"İşlem Tamam! Korku Endeksi: {fear_score}")

if __name__ == "__main__":
    main()