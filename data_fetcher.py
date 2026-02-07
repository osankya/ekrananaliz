import yfinance as yf
import json

# Örnek sektör eşleşmeleri (Daha fazlası eklenebilir)
SEKTORLER = {
    "THYAO": "Ulaştırma", "PGSUS": "Ulaştırma",
    "ASELS": "Savunma", "SDTTR": "Savunma", "KORDS": "Savunma",
    "EREGL": "Demir Çelik", "KRDMD": "Demir Çelik",
    "AKBNK": "Banka", "ISCTR": "Banka", "GARAN": "Banka",
    "SASA": "Kimya", "HEKTS": "Kimya",
    "EUPWR": "Enerji", "ASTOR": "Enerji", "SMRTG": "Enerji", "KONTR": "Enerji"
}

def get_data():
    # Buraya BIST'teki tüm sembolleri ekleyebilirsin
    symbols = ["THYAO.IS", "ASELS.IS", "EREGL.IS", "AKBNK.IS", "SASA.IS", "ASTOR.IS", "ISCTR.IS", "GARAN.IS", "PGSUS.IS", "EUPWR.IS"]
    data_list = []

    for sym in symbols:
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(period="2d")
            if len(hist) < 2: continue
            
            prev_close = hist['Close'].iloc[-2]
            current_price = hist['Close'].iloc[-1]
            change = ((current_price - prev_close) / prev_close) * 100
            
            clean_sym = sym.replace(".IS", "")
            data_list.append({
                "x": clean_sym,
                "y": round(change, 2),
                "s": SEKTORLER.get(clean_sym, "Diğer") # Sektör bilgisi
            })
        except:
            continue
            
    with open('data.json', 'w') as f:
        json.dump(data_list, f)

get_data()