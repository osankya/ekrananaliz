import yfinance as yf
import json

# Hisseleri sektörlere göre gruplayalım
SEKTOR_HARITASI = {
    "SAVUNMA": ["ASELS.IS", "SDTTR.IS", "KORDS.IS"],
    "ULAŞTIRMA": ["THYAO.IS", "PGSUS.IS", "TAVHL.IS"],
    "BANKA": ["AKBNK.IS", "ISCTR.IS", "GARAN.IS", "YKBNK.IS"],
    "ENERJİ": ["ASTOR.IS", "EUPWR.IS", "SMRTG.IS", "KONTR.IS", "ALARK.IS"],
    "SANAYİ/KİMYA": ["SASA.IS", "HEKTS.IS", "EREGL.IS", "KRDMD.IS", "SISE.IS"]
}

def get_data():
    output = []
    
    for sektor, semboller in SEKTOR_HARITASI.items():
        sektor_verisi = {"name": sektor, "data": []}
        
        for sym in semboller:
            try:
                ticker = yf.Ticker(sym)
                hist = ticker.history(period="2d")
                if len(hist) < 2: continue
                
                degisim = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100
                sektor_verisi["data"].append({
                    "x": sym.replace(".IS", ""),
                    "y": round(degisim, 2)
                })
            except: continue
        
        if sektor_verisi["data"]:
            output.append(sektor_verisi)
            
    with open('data.json', 'w') as f:
        json.dump(output, f)

if __name__ == "__main__":
    get_data()