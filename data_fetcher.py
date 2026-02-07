import yfinance as yf
import json

SEKTORLER = {
    "BANKA": ["AKBNK.IS", "ISCTR.IS", "GARAN.IS", "YKBNK.IS", "VAKBN.IS", "HALKB.IS"],
    "ULAŞTIRMA": ["THYAO.IS", "PGSUS.IS", "TAVHL.IS"],
    "SAVUNMA": ["ASELS.IS", "SDTTR.IS", "OTKAR.IS"],
    "ENERJİ": ["ASTOR.IS", "SMRTG.IS", "KONTR.IS", "ODAS.IS", "ZOREN.IS"],
    "SANAYİ": ["SASA.IS", "EREGL.IS", "KRDMD.IS", "SISE.IS", "FROTO.IS", "TOASO.IS"],
    "GIDA": ["BIMAS.IS", "MGROS.IS", "CCOLA.IS"]
}

def fetch():
    final_data = []
    for sektor, listem in SEKTORLER.items():
        node = {"name": sektor, "data": []}
        for s in listem:
            try:
                t = yf.Ticker(s)
                h = t.history(period="2d")
                if len(h) < 2: continue
                
                # y = Market Cap (Kutu Boyutu), c = Değişim (Renk)
                mcap = t.info.get('marketCap', 1000)
                change = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
                
                node["data"].append({
                    "x": s.replace(".IS", ""),
                    "y": mcap,
                    "c": round(change, 2)
                })
                print(f"Çekildi: {s}")
            except: continue
        if node["data"]: final_data.append(node)
    
    with open('data.json', 'w') as f:
        json.dump(final_data, f)

if __name__ == "__main__":
    fetch()