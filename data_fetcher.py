import yfinance as yf
import json

# BIST 100 hisseleri sektörlere göre sınıflandırılmış
SEKTOR_HARITASI = {
    "BANKA": ["AKBNK.IS", "ISCTR.IS", "GARAN.IS", "YKBNK.IS", "HALKB.IS", "VAKBN.IS", "ICBCT.IS", "SKBNK.IS", "ALBRK.IS", "TSKB.IS"],
    "SAVUNMA": ["ASELS.IS", "SDTTR.IS", "KORDS.IS", "OTKAR.IS", "REEDR.IS"],
    "HAVACILIK/ULAŞIM": ["THYAO.IS", "PGSUS.IS", "TAVHL.IS", "DOCO.IS", "CLEBI.IS"],
    "ENERJİ": ["ASTOR.IS", "EUPWR.IS", "SMRTG.IS", "KONTR.IS", "ALARK.IS", "CWENE.IS", "ODAS.IS", "AKENR.IS", "AKSEN.IS", "ZOREN.IS"],
    "DEMİR-ÇELİK": ["EREGL.IS", "KRDMD.IS", "IZMDC.IS"],
    "KİMYA/PETROKIMYA": ["SASA.IS", "GUBRF.IS", "AKSA.IS", "PETKM.IS", "TUPRS.IS"],
    "TEKSTİL": ["HEKTS.IS", "YUNSA.IS", "BRSAN.IS", "SKTAS.IS"],
    "OTOMOTİV": ["FROTO.IS", "TOASO.IS", "TTRAK.IS", "KLMSN.IS", "TMSN.IS"],
    "İNŞAAT/ÇIMENTO": ["KONYA.IS", "ENJSA.IS", "EGEEN.IS", "CIMSA.IS", "GOLTS.IS", "BTCIM.IS"],
    "TEKNOLOJİ": ["LOGO.IS", "LINK.IS", "INDES.IS", "ARENA.IS"],
    "GIDA": ["ULKER.IS", "TATGD.IS", "PETUN.IS", "CCOLA.IS", "BANVT.IS", "PENGD.IS"],
    "HOLDİNG": ["KCHOL.IS", "SAHOL.IS", "AGHOL.IS", "DOHOL.IS", "ECZYT.IS", "BIMAS.IS", "THYAO.IS", "SISE.IS"],
    "PERAKENDE": ["BIMAS.IS", "MGROS.IS", "SOKM.IS", "MAVI.IS"],
    "SPOR/EĞLENCE": ["GSRAY.IS", "BJKAS.IS", "FENER.IS", "TSPOR.IS"],
    "TELEKOMÜNİKASYON": ["TCELL.IS", "TTKOM.IS"],
    "SİGORTA": ["AKGRT.IS", "AGESA.IS"],
    "MADENCİLİK": ["IPEKE.IS", "KOZAL.IS", "KOZAA.IS"],
    "TURİZM": ["MAALT.IS", "AYCES.IS", "UTOPYA.IS"],
    "DİĞER": ["VESBE.IS", "ENKAI.IS", "IEYHO.IS", "RALYH.IS", "PRKME.IS", "OYAKC.IS", "GESAN.IS"]
}

def get_data():
    output = []
    for sektor, semboller in SEKTOR_HARITASI.items():
        sektor_verisi = {"name": sektor, "data": []}
        for sym in semboller:
            try:
                t = yf.Ticker(sym)
                h = t.history(period="2d")
                if len(h) < 2: 
                    continue
                degisim = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
                sektor_verisi["data"].append({
                    "x": sym.replace(".IS", ""), 
                    "y": round(degisim, 2)
                })
            except Exception as e:
                print(f"Hata: {sym} - {e}")
                continue
        
        if sektor_verisi["data"]:
            output.append(sektor_verisi)
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✓ {sum(len(s['data']) for s in output)} hisse güncellendi!")

if __name__ == "__main__":
    get_data()