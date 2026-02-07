import yfinance as yf
import json

# BIST'teki TÜM önemli hisseler (200+ hisse)
SEKTOR_HARITASI = {
    "BANKA": ["AKBNK.IS", "ISCTR.IS", "GARAN.IS", "YKBNK.IS", "HALKB.IS", "VAKBN.IS", "ICBCT.IS", "SKBNK.IS", "ALBRK.IS", "TSKB.IS", "QNBFB.IS"],
    
    "SAVUNMA": ["ASELS.IS", "SDTTR.IS", "KORDS.IS", "OTKAR.IS", "REEDR.IS", "KATMR.IS"],
    
    "HAVACILIK/ULAŞIM": ["THYAO.IS", "PGSUS.IS", "TAVHL.IS", "DOCO.IS", "CLEBI.IS", "RYSAS.IS"],
    
    "ENERJİ": ["ASTOR.IS", "EUPWR.IS", "SMRTG.IS", "KONTR.IS", "ALARK.IS", "CWENE.IS", "ODAS.IS", "AKENR.IS", "AKSEN.IS", "ZOREN.IS", "AYEN.IS", "HUNER.IS", "ENJSA.IS"],
    
    "DEMİR-ÇELİK": ["EREGL.IS", "KRDMD.IS", "IZMDC.IS", "ERBOS.IS", "BURCE.IS", "CELHA.IS", "DOKTA.IS"],
    
    "KİMYA/PETROKIMYA": ["SASA.IS", "GUBRF.IS", "AKSA.IS", "PETKM.IS", "TUPRS.IS", "GOODY.IS", "SODA.IS", "ALKIM.IS", "BAGFS.IS"],
    
    "TEKSTİL": ["HEKTS.IS", "YUNSA.IS", "BRSAN.IS", "SKTAS.IS", "KORDS.IS", "BLCYT.IS", "DAGI.IS", "ROYAL.IS"],
    
    "OTOMOTİV": ["FROTO.IS", "TOASO.IS", "TTRAK.IS", "KLMSN.IS", "TMSN.IS", "GEREL.IS", "PARSN.IS"],
    
    "İNŞAAT/ÇİMENTO": ["KONYA.IS", "ENJSA.IS", "EGEEN.IS", "CIMSA.IS", "GOLTS.IS", "BTCIM.IS", "ADANA.IS", "BUCIM.IS", "BRSAN.IS", "NUHCM.IS"],
    
    "TEKNOLOJİ": ["LOGO.IS", "LINK.IS", "INDES.IS", "ARENA.IS", "ASELS.IS", "KAREL.IS", "NETAS.IS", "ESCOM.IS"],
    
    "GIDA": ["ULKER.IS", "TATGD.IS", "PETUN.IS", "CCOLA.IS", "BANVT.IS", "PENGD.IS", "KNFRT.IS", "AEFES.IS", "EKIZ.IS", "ERSU.IS", "KERVT.IS", "PINSU.IS"],
    
    "HOLDİNG": ["KCHOL.IS", "SAHOL.IS", "AGHOL.IS", "DOHOL.IS", "ECZYT.IS", "BIMAS.IS", "SISE.IS", "ARBUL.IS", "AVHOL.IS", "IHEVA.IS", "TURSG.IS"],
    
    "PERAKENDE": ["BIMAS.IS", "MGROS.IS", "SOKM.IS", "MAVI.IS", "CRFSA.IS", "MPARK.IS", "ADESE.IS"],
    
    "SPOR": ["GSRAY.IS", "BJKAS.IS", "FENER.IS", "TSPOR.IS"],
    
    "TELEKOMÜNİKASYON": ["TCELL.IS", "TTKOM.IS", "AKNET.IS"],
    
    "SİGORTA": ["AKGRT.IS", "AGESA.IS", "ANSGR.IS", "ANHYT.IS"],
    
    "MADENCİLİK": ["IPEKE.IS", "KOZAL.IS", "KOZAA.IS", "PAMEL.IS", "CMENT.IS"],
    
    "TURİZM": ["MAALT.IS", "AYCES.IS", "UTOPYA.IS", "MARTI.IS", "PKENT.IS"],
    
    "KAĞIT": ["KARTN.IS", "OLMIP.IS", "SILVR.IS"],
    
    "DİĞER": ["VESBE.IS", "ENKAI.IS", "IEYHO.IS", "RALYH.IS", "PRKME.IS", "OYAKC.IS", "GESAN.IS", "MRSHL.IS", "DZGYO.IS", "VKGYO.IS"]
}

def get_data():
    output = []
    
    for sektor, semboller in SEKTOR_HARITASI.items():
        sektor_verisi = {"name": sektor, "data": []}
        
        for sym in semboller:
            try:
                t = yf.Ticker(sym)
                
                # Fiyat değişimi
                h = t.history(period="2d")
                if len(h) < 2: 
                    continue
                    
                degisim = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
                
                # Piyasa değeri (market cap)
                info = t.info
                market_cap = info.get('marketCap', 0)
                
                # Eğer market cap yoksa shares * price ile hesapla
                if market_cap == 0:
                    shares = info.get('sharesOutstanding', 0)
                    price = h['Close'].iloc[-1]
                    market_cap = shares * price
                
                sektor_verisi["data"].append({
                    "x": sym.replace(".IS", ""), 
                    "y": round(degisim, 2),
                    "z": int(market_cap) if market_cap > 0 else 1000000  # z = piyasa değeri
                })
                
            except Exception as e:
                print(f"Hata: {sym} - {e}")
                continue
        
        # Piyasa değerine göre sırala (büyükten küçüğe)
        sektor_verisi["data"].sort(key=lambda x: x.get('z', 0), reverse=True)
        
        if sektor_verisi["data"]:
            output.append(sektor_verisi)
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    toplam = sum(len(s['data']) for s in output)
    print(f"✓ {toplam} hisse güncellendi!")
    print(f"✓ {len(output)} sektör işlendi!")

if __name__ == "__main__":
    get_data()