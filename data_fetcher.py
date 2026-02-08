import yfinance as yf
import json

# SADECE 12 HİSSE - EKRANA RAHATLICA SIĞ
BIST100_HARITASI = {
    "BANKA": ["AKBNK.IS", "GARAN.IS"],
    "HAVACILIK": ["THYAO.IS"],
    "SAVUNMA": ["ASELS.IS"],
    "ENERJİ": ["AKSEN.IS"],
    "HOLDİNG": ["KCHOL.IS"],
    "PERAKENDE": ["BIMAS.IS"],
    "OTOMOTİV": ["FROTO.IS"],
    "GIDA": ["ULKER.IS"],
    "ÇİMENTO": ["KONYA.IS"],
    "KİMYA": ["SASA.IS"],
    "SPOR": ["GSRAY.IS"]
}

TUM_HISSELER = {
    "BANKA": ["AKBNK.IS", "ISCTR.IS", "GARAN.IS", "YKBNK.IS", "HALKB.IS", "VAKBN.IS", "ICBCT.IS", "SKBNK.IS"],
    "SAVUNMA & HAVACILIK": ["ASELS.IS", "SDTTR.IS", "KORDS.IS", "THYAO.IS", "PGSUS.IS", "TAVHL.IS"],
    "ENERJİ": ["AKSEN.IS", "AKENR.IS", "EUPWR.IS", "ODAS.IS", "ZOREN.IS", "AYGAZ.IS"],
    "HOLDİNG": ["KCHOL.IS", "SAHOL.IS", "DOHOL.IS", "BIMAS.IS", "SISE.IS"],
    "PERAKENDE": ["BIMAS.IS", "MGROS.IS", "SOKM.IS", "MAVI.IS"],
    "OTOMOTİV": ["FROTO.IS", "TOASO.IS", "TTRAK.IS", "TMSN.IS"],
    "GIDA": ["ULKER.IS", "CCOLA.IS", "AEFES.IS", "TATGD.IS"],
    "ÇİMENTO": ["KONYA.IS", "CIMSA.IS", "GOLTS.IS"],
    "KİMYA": ["SASA.IS", "GUBRF.IS", "TUPRS.IS"],
    "SPOR": ["GSRAY.IS", "BJKAS.IS", "FENER.IS"],
    "TEKNOLOJİ": ["LOGO.IS", "KAREL.IS", "LINK.IS"]
}

def get_stock_data(symbol):
    try:
        t = yf.Ticker(symbol)
        h = t.history(period="5d")
        if len(h) < 2: return None
        degisim = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
        info = t.info
        market_cap = info.get('marketCap', 1000000) or 1000000
        return {"x": symbol.replace(".IS", ""), "y": round(degisim, 2), "z": int(market_cap)}
    except:
        return None

def calculate_fear_greed_index():
    try:
        xu100 = yf.Ticker("XU100.IS")
        hist = xu100.history(period="6mo")
        if len(hist) < 125:
            return {"score": 50, "status": "Nötr", "data": [], "components": {"momentum": 50, "volatility": 50, "volume": 50, "breadth": 50}}
        
        current_price = hist['Close'].iloc[-1]
        ma_125 = hist['Close'].rolling(window=125).mean().iloc[-1]
        momentum_score = min(100, max(0, ((current_price / ma_125 - 1) * 500) + 50))
        volatility = hist['Close'].pct_change().rolling(window=50).std().iloc[-1]
        volatility_score = max(0, min(100, 100 - (volatility * 1000)))
        avg_volume = hist['Volume'].rolling(window=50).mean().iloc[-1]
        current_volume = hist['Volume'].iloc[-1]
        volume_score = min(100, max(0, (current_volume / avg_volume - 1) * 100 + 50))
        total_score = (momentum_score * 0.25 + volatility_score * 0.25 + volume_score * 0.25 + 50 * 0.25)
        
        if total_score >= 75: status = "Aşırı Açgözlülük"
        elif total_score >= 55: status = "Açgözlülük"
        elif total_score >= 45: status = "Nötr"
        elif total_score >= 25: status = "Korku"
        else: status = "Aşırı Korku"
        
        recent_data = []
        for i in range(min(30, len(hist))):
            idx = -(30-i)
            date = hist.index[idx].strftime('%Y-%m-%d')
            daily_score = max(0, min(100, 50 + (hist['Close'].iloc[idx] / ma_125 - 1) * 100))
            recent_data.append({"date": date, "score": round(daily_score, 1)})
        
        return {"score": round(total_score, 1), "status": status, "data": recent_data, 
                "components": {"momentum": round(momentum_score, 1), "volatility": round(volatility_score, 1), 
                              "volume": round(volume_score, 1), "breadth": 50}}
    except:
        return {"score": 50, "status": "Nötr", "data": [], "components": {"momentum": 50, "volatility": 50, "volume": 50, "breadth": 50}}

def get_data():
    bist100_data = []
    for sektor, semboller in BIST100_HARITASI.items():
        sektor_verisi = {"name": sektor, "data": []}
        for sym in semboller:
            data = get_stock_data(sym)
            if data:
                sektor_verisi["data"].append(data)
                print(f"✓ {data['x']} - %{data['y']}")
        if sektor_verisi["data"]:
            bist100_data.append(sektor_verisi)
    
    tum_hisseler_data = []
    for sektor, semboller in TUM_HISSELER.items():
        sektor_verisi = {"name": sektor, "data": []}
        for sym in semboller:
            data = get_stock_data(sym)
            if data: sektor_verisi["data"].append(data)
        if sektor_verisi["data"]:
            tum_hisseler_data.append(sektor_verisi)
    
    fear_index = calculate_fear_greed_index()
    
    with open('data.json', 'w', encoding='utf-8') as f: json.dump(bist100_data, f, ensure_ascii=False)
    with open('all_stocks.json', 'w', encoding='utf-8') as f: json.dump(tum_hisseler_data, f, ensure_ascii=False)
    with open('fear_index.json', 'w', encoding='utf-8') as f: json.dump(fear_index, f, ensure_ascii=False)
    
    print(f"\n{'='*50}\n✓ BIST 100: {sum(len(s['data']) for s in bist100_data)} hisse\n✓ KORKU: {fear_index['score']}\n{'='*50}")

if __name__ == "__main__":
    get_data()