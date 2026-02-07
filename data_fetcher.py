import yfinance as yf
import json

# Listeyi genişlettik, daha fazla hisse ekledik
SEKTOR_HARITASI = {
    "BANKA": ["AKBNK.IS", "ISCTR.IS", "GARAN.IS", "YKBNK.IS", "HALKB.IS", "VAKBN.IS"],
    "SAVUNMA": ["ASELS.IS", "SDTTR.IS", "KORDS.IS", "OTKAR.IS", "REEDR.IS"],
    "ULAŞTIRMA": ["THYAO.IS", "PGSUS.IS", "TAVHL.IS", "DOCO.IS"],
    "ENERJİ": ["ASTOR.IS", "EUPWR.IS", "SMRTG.IS", "KONTR.IS", "ALARK.IS", "CWENE.IS", "ODAS.IS"],
    "SANAYİ/KİMYA": ["SASA.IS", "HEKTS.IS", "EREGL.IS", "KRDMD.IS", "SISE.IS", "TOASO.IS", "FROTO.IS"],
    "HOLDİNG": ["KCHOL.IS", "SAHOL.IS", "AGHOL.IS", "DOHOL.IS"]
}

def get_data():
    output = []
    for sektor, semboller in SEKTOR_HARITASI.items():
        sektor_verisi = {"name": sektor, "data": []}
        for sym in semboller:
            try:
                t = yf.Ticker(sym)
                h = t.history(period="2d")
                if len(h) < 2: continue
                degisim = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
                sektor_verisi["data"].append({"x": sym.replace(".IS", ""), "y": round(degisim, 2)})
            except: continue
        if sektor_verisi["data"]: output.append(sektor_verisi)
    with open('data.json', 'w') as f:
        json.dump(output, f)

if __name__ == "__main__":
    get_data()