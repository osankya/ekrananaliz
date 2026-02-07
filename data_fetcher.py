import yfinance as yf
import json

# Senin listenden derlediğim genişletilmiş sektör haritası
SEKTOR_HARITASI = {
    "BANKA": ["AKBNK.IS", "ISCTR.IS", "GARAN.IS", "YKBNK.IS", "HALKB.IS", "VAKBN.IS", "SKBNK.IS", "ALBRK.IS"],
    "SAVUNMA/TEKNOLOJİ": ["ASELS.IS", "SDTTR.IS", "MIATK.IS", "ARDYZ.IS", "REEDR.IS", "OTKAR.IS", "KFEIN.IS", "LOGOS.IS"],
    "ENERJİ": ["ASTOR.IS", "EUPWR.IS", "SMRTG.IS", "KONTR.IS", "ALARK.IS", "CWENE.IS", "ODAS.IS", "ZOREN.IS", "AYDEM.IS", "ENJSA.IS", "HUNER.IS"],
    "SANAYİ/METAL": ["SASA.IS", "HEKTS.IS", "EREGL.IS", "KRDMD.IS", "SISE.IS", "TOASO.IS", "FROTO.IS", "BRISA.IS", "KCAER.IS", "ARCLK.IS"],
    "ULAŞTIRMA": ["THYAO.IS", "PGSUS.IS", "TAVHL.IS", "DOCO.IS", "TMSN.IS"],
    "PERAKENDE/GIDA": ["BIMAS.IS", "MGROS.IS", "SOKM.IS", "AEFES.IS", "CCOLA.IS", "ULKER.IS", "TATGD.IS"],
    "HOLDİNG/GAYRİMENKUL": ["KCHOL.IS", "SAHOL.IS", "AGHOL.IS", "DOHOL.IS", "EKGYO.IS", "OZKGY.IS", "TRGYO.IS"],
}

def get_data():
    output = []
    print("Piyasa değerleri ve veriler çekiliyor... Lütfen bekleyin.")
    
    for sektor, semboller in SEKTOR_HARITASI.items():
        sektor_verisi = {"name": sektor, "data": []}
        for sym in semboller:
            try:
                t = yf.Ticker(sym)
                info = t.info
                hist = t.history(period="2d")
                
                if len(hist) < 2: continue
                
                # mcap: Piyasa Değeri (Kutu boyutu için)
                # change: Yüzdelik değişim (Renk için)
                mcap = info.get('marketCap', 1000000) # Değer yoksa min. değer
                change = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100
                
                sektor_verisi["data"].append({
                    "x": sym.replace(".IS", ""),
                    "y": mcap, 
                    "c": round(change, 2)
                })
                print(f"Bitti: {sym}")
            except: continue
        
        if sektor_verisi["data"]:
            output.append(sektor_verisi)
            
    with open('data.json', 'w') as f:
        json.dump(output, f)
    print("Veri tabanı güncellendi!")

if __name__ == "__main__":
    get_data()