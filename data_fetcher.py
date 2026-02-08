import yfinance as yf
import json
import requests
from datetime import datetime, timedelta

# BIST 100 EKRANI - Sadece En Büyük 30 Hisse (Ekrana Sığsın)
BIST100_HARITASI = {
    "BANKA": ["AKBNK.IS", "GARAN.IS", "YKBNK.IS"],
    "SAVUNMA": ["ASELS.IS"],
    "HAVACILIK": ["THYAO.IS", "PGSUS.IS"],
    "ENERJİ": ["AKSEN.IS", "AKENR.IS"],
    "HOLDİNG": ["KCHOL.IS", "SAHOL.IS"],
    "TEKNOLOJİ": ["LOGO.IS"],
    "PERAKENDE": ["BIMAS.IS", "MGROS.IS"],
    "OTOMOTİV": ["FROTO.IS", "TOASO.IS"],
    "GIDA": ["ULKER.IS", "CCOLA.IS"],
    "ÇİMENTO": ["KONYA.IS"],
    "DEMİR-ÇELİK": ["EREGL.IS"],
    "KİMYA": ["SASA.IS", "GUBRF.IS"],
    "SPOR": ["GSRAY.IS", "BJKAS.IS"]
}

# TÜM HİSSELER - Modal'da seçim için
TUM_HISSELER = {
    "BANKA": [
        "AKBNK.IS", "ISCTR.IS", "GARAN.IS", "YKBNK.IS", "HALKB.IS", "VAKBN.IS", 
        "ICBCT.IS", "SKBNK.IS", "ALBRK.IS", "TSKB.IS", "QNBFK.IS"
    ],
    "SAVUNMA & HAVACILIK": [
        "ASELS.IS", "SDTTR.IS", "KORDS.IS", "OTKAR.IS", "REEDR.IS", "KATMR.IS",
        "THYAO.IS", "PGSUS.IS", "TAVHL.IS", "DOCO.IS", "CLEBI.IS", "RYSAS.IS"
    ],
    "ENERJİ": [
        "ASTOR.IS", "EUPWR.IS", "SMRTG.IS", "KONTR.IS", "ALARK.IS", "CWENE.IS", 
        "ODAS.IS", "AKENR.IS", "AKSEN.IS", "ZOREN.IS", "AYEN.IS", "HUNER.IS", 
        "ENJSA.IS", "AYDEM.IS", "AYES.IS", "AYGAZ.IS", "ZERGY.IS", "BIOEN.IS"
    ],
    "HOLDİNG": [
        "KCHOL.IS", "SAHOL.IS", "AGHOL.IS", "DOHOL.IS", "ECZYT.IS", "BIMAS.IS", 
        "SISE.IS", "AVHOL.IS", "TURSG.IS", "NTHOL.IS", "TRHOL.IS"
    ],
    "TEKNOLOJİ": [
        "LOGO.IS", "LINK.IS", "INDES.IS", "ARENA.IS", "KAREL.IS", "NETAS.IS", 
        "ESCOM.IS", "ALCTL.IS", "FONET.IS", "INFO.IS", "INVEO.IS"
    ],
    "PERAKENDE": [
        "BIMAS.IS", "MGROS.IS", "SOKM.IS", "MAVI.IS", "CRFSA.IS", "MPARK.IS", 
        "ADESE.IS", "BIZIM.IS", "KOTON.IS"
    ],
    "OTOMOTİV": [
        "FROTO.IS", "TOASO.IS", "TTRAK.IS", "KLMSN.IS", "TMSN.IS", "GEREL.IS", 
        "PARSN.IS", "ASUZU.IS", "BFREN.IS", "OTKAR.IS"
    ],
    "GIDA": [
        "ULKER.IS", "TATGD.IS", "PETUN.IS", "CCOLA.IS", "BANVT.IS", "PENGD.IS", 
        "KNFRT.IS", "AEFES.IS", "EKIZ.IS", "ERSU.IS", "PINSU.IS", "KENT.IS"
    ],
    "ÇİMENTO": [
        "KONYA.IS", "CIMSA.IS", "GOLTS.IS", "BTCIM.IS", "BUCIM.IS", "NUHCM.IS"
    ],
    "DEMİR-ÇELİK": [
        "EREGL.IS", "KRDMD.IS", "KRDMA.IS", "IZMDC.IS", "ERBOS.IS", "BURCE.IS"
    ],
    "KİMYA": [
        "SASA.IS", "GUBRF.IS", "AKSA.IS", "PETKM.IS", "TUPRS.IS", "ALKIM.IS", "BAGFS.IS"
    ],
    "TEKSTİL": [
        "HEKTS.IS", "YUNSA.IS", "BRSAN.IS", "SKTAS.IS", "BLCYT.IS", "MAVI.IS"
    ],
    "SPOR": [
        "GSRAY.IS", "BJKAS.IS", "FENER.IS", "TSPOR.IS"
    ],
    "TELEKOMÜNİKASYON": [
        "TCELL.IS", "TTKOM.IS"
    ],
    "SİGORTA": [
        "AKGRT.IS", "AGESA.IS", "ANSGR.IS"
    ],
    "TURİZM": [
        "MAALT.IS", "AYCES.IS", "MARTI.IS", "PKENT.IS"
    ],
    "GYO": [
        "ADGYO.IS", "AVGYO.IS", "EKGYO.IS", "ISGYO.IS", "KGYO.IS", "TRGYO.IS"
    ]
}

def get_stock_data(symbol):
    """Tek bir hisse için veri çeker"""
    try:
        t = yf.Ticker(symbol)
        h = t.history(period="5d")
        
        if len(h) < 2:
            return None
            
        degisim = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
        
        info = t.info
        market_cap = info.get('marketCap', 0)
        
        if market_cap == 0 or market_cap is None:
            shares = info.get('sharesOutstanding', 0)
            price = h['Close'].iloc[-1]
            if shares and shares > 0:
                market_cap = shares * price
            else:
                market_cap = 1000000
        
        return {
            "x": symbol.replace(".IS", ""), 
            "y": round(degisim, 2),
            "z": int(market_cap) if market_cap > 0 else 1000000
        }
    except:
        return None

def calculate_fear_greed_index():
    """BIST Korku & Açgözlülük Endeksi Hesaplar"""
    try:
        # XU100 için veri çek
        xu100 = yf.Ticker("XU100.IS")
        hist = xu100.history(period="6mo")
        
        if len(hist) < 125:
            return {"score": 50, "status": "Nötr", "data": []}
        
        # 1. Momentum (25 puan) - 125 günlük momentum
        current_price = hist['Close'].iloc[-1]
        ma_125 = hist['Close'].rolling(window=125).mean().iloc[-1]
        momentum_score = min(100, max(0, ((current_price / ma_125 - 1) * 500) + 50))
        
        # 2. Volatilite (25 puan) - 50 günlük standart sapma
        volatility = hist['Close'].pct_change().rolling(window=50).std().iloc[-1]
        volatility_score = max(0, min(100, 100 - (volatility * 1000)))
        
        # 3. Hacim (25 puan) - Hacim değişimi
        avg_volume = hist['Volume'].rolling(window=50).mean().iloc[-1]
        current_volume = hist['Volume'].iloc[-1]
        volume_score = min(100, max(0, (current_volume / avg_volume - 1) * 100 + 50))
        
        # 4. Piyasa Genişliği (25 puan) - Yükselen hisse sayısı
        breadth_score = 50  # Basitleştirilmiş
        
        # Toplam skor
        total_score = (
            momentum_score * 0.25 +
            volatility_score * 0.25 +
            volume_score * 0.25 +
            breadth_score * 0.25
        )
        
        # Durum belirleme
        if total_score >= 75:
            status = "Aşırı Açgözlülük"
        elif total_score >= 55:
            status = "Açgözlülük"
        elif total_score >= 45:
            status = "Nötr"
        elif total_score >= 25:
            status = "Korku"
        else:
            status = "Aşırı Korku"
        
        # Son 30 günlük veri
        recent_data = []
        for i in range(min(30, len(hist))):
            idx = -(30-i)
            date = hist.index[idx].strftime('%Y-%m-%d')
            # Basitleştirilmiş günlük skor
            daily_score = 50 + (hist['Close'].iloc[idx] / ma_125 - 1) * 100
            daily_score = max(0, min(100, daily_score))
            recent_data.append({"date": date, "score": round(daily_score, 1)})
        
        return {
            "score": round(total_score, 1),
            "status": status,
            "data": recent_data,
            "components": {
                "momentum": round(momentum_score, 1),
                "volatility": round(volatility_score, 1),
                "volume": round(volume_score, 1),
                "breadth": round(breadth_score, 1)
            }
        }
    except Exception as e:
        print(f"Korku endeksi hatası: {e}")
        return {"score": 50, "status": "Nötr", "data": []}

def get_data():
    # BIST 100 için veri
    bist100_data = []
    for sektor, semboller in BIST100_HARITASI.items():
        sektor_verisi = {"name": sektor, "data": []}
        for sym in semboller:
            data = get_stock_data(sym)
            if data:
                sektor_verisi["data"].append(data)
                print(f"✓ {data['x']} - %{data['y']}")
        
        sektor_verisi["data"].sort(key=lambda x: x.get('z', 0), reverse=True)
        if sektor_verisi["data"]:
            bist100_data.append(sektor_verisi)
    
    # TÜM HİSSELER için veri
    tum_hisseler_data = []
    for sektor, semboller in TUM_HISSELER.items():
        sektor_verisi = {"name": sektor, "data": []}
        for sym in semboller:
            data = get_stock_data(sym)
            if data:
                sektor_verisi["data"].append(data)
        
        sektor_verisi["data"].sort(key=lambda x: x.get('z', 0), reverse=True)
        if sektor_verisi["data"]:
            tum_hisseler_data.append(sektor_verisi)
    
    # Korku endeksi hesapla
    fear_index = calculate_fear_greed_index()
    
    # Dosyaları kaydet
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(bist100_data, f, ensure_ascii=False, indent=2)
    
    with open('all_stocks.json', 'w', encoding='utf-8') as f:
        json.dump(tum_hisseler_data, f, ensure_ascii=False, indent=2)
    
    with open('fear_index.json', 'w', encoding='utf-8') as f:
        json.dump(fear_index, f, ensure_ascii=False, indent=2)
    
    bist100_count = sum(len(s['data']) for s in bist100_data)
    total_count = sum(len(s['data']) for s in tum_hisseler_data)
    
    print(f"\n{'='*50}")
    print(f"✓ BIST 100: {bist100_count} hisse")
    print(f"✓ TÜM HİSSELER: {total_count} hisse")
    print(f"✓ KORKU ENDEKSİ: {fear_index['score']} - {fear_index['status']}")
    print(f"{'='*50}")

if __name__ == "__main__":
    get_data()