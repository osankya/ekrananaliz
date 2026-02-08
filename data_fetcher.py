import yfinance as yf
import json

# BIST 100 EKRANI (Ana Ekran)
BIST100_HARITASI = {
    "BANKA": ["AKBNK.IS", "GARAN.IS", "ISCTR.IS", "YKBNK.IS"],
    "SAVUNMA": ["ASELS.IS", "KORDS.IS"],
    "HAVACILIK": ["THYAO.IS", "PGSUS.IS"],
    "ENERJİ": ["AKSEN.IS", "AKENR.IS", "EUPWR.IS"],
    "HOLDİNG": ["KCHOL.IS", "SAHOL.IS", "DOHOL.IS"],
    "TEKNOLOJİ": ["LOGO.IS", "KAREL.IS"],
    "PERAKENDE": ["BIMAS.IS", "MGROS.IS", "SOKM.IS"],
    "OTOMOTİV": ["FROTO.IS", "TOASO.IS", "TTRAK.IS"],
    "GIDA": ["ULKER.IS", "CCOLA.IS", "AEFES.IS"],
    "DEMİR-ÇELİK": ["EREGL.IS", "KRDMD.IS"],
    "KİMYA": ["SASA.IS", "GUBRF.IS", "TUPRS.IS"]
}

# TÜM HİSSELER (Seçim Modalı için - Özet Liste)
TUM_HISSELER = {
    "BANKA": ["AKBNK.IS", "ISCTR.IS", "GARAN.IS", "YKBNK.IS", "VAKBN.IS", "HALKB.IS"],
    "ENERJİ": ["ASTOR.IS", "EUPWR.IS", "SMRTG.IS", "KONTR.IS", "ALARK.IS", "ENJSA.IS"],
    "HOLDİNG": ["KCHOL.IS", "SAHOL.IS", "SISE.IS", "DOHOL.IS", "AGHOL.IS"],
    "DİĞER": ["THYAO.IS", "PGSUS.IS", "ASELS.IS", "EREGL.IS", "TUPRS.IS", "BIMAS.IS", "MGROS.IS", "SASA.IS"]
}

def get_stock_data(symbol):
    try:
        t = yf.Ticker(symbol)
        h = t.history(period="2d")
        if len(h) < 2: return None
            
        degisim = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
        info = t.info
        market_cap = info.get('marketCap') or (info.get('sharesOutstanding', 0) * h['Close'].iloc[-1])
        
        return {
            "x": symbol.replace(".IS", ""), 
            "y": round(degisim, 2),
            "z": int(market_cap) if market_cap > 0 else 1000000
        }
    except:
        return None

def main():
    bist_res = []
    for s, syms in BIST100_HARITASI.items():
        data = [get_stock_data(sm) for sm in syms if get_stock_data(sm)]
        if data: bist_res.append({"name": s, "data": data})

    all_res = []
    for s, syms in TUM_HISSELER.items():
        data = [get_stock_data(sm) for sm in syms if get_stock_data(sm)]
        if data: all_res.append({"name": s, "data": data})

    with open('data.json', 'w', encoding='utf-8') as f: json.dump(bist_res, f, ensure_ascii=False)
    with open('all_stocks.json', 'w', encoding='utf-8') as f: json.dump(all_res, f, ensure_ascii=False)
    print("Veriler başarıyla güncellendi.")

if __name__ == "__main__":
    main()