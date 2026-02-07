import yfinance as yf
import json

# BIST 100 EKRANI - Sadece Önemli Hisseler (İlk ekranda gösterilecek)
BIST100_HARITASI = {
    "BANKA": ["AKBNK.IS", "GARAN.IS", "ISCTR.IS", "YKBNK.IS", "HALKB.IS"],
    "SAVUNMA": ["ASELS.IS", "KORDS.IS", "SDTTR.IS"],
    "HAVACILIK": ["THYAO.IS", "PGSUS.IS", "TAVHL.IS"],
    "ENERJİ": ["AKSEN.IS", "AKENR.IS", "EUPWR.IS", "ODAS.IS"],
    "HOLDİNG": ["KCHOL.IS", "SAHOL.IS", "DOHOL.IS", "AGHOL.IS"],
    "TEKNOLOJİ": ["ASELS.IS", "LOGO.IS", "KAREL.IS", "LINK.IS"],
    "PERAKENDE": ["BIMAS.IS", "MGROS.IS", "SOKM.IS", "MAVI.IS"],
    "OTOMOTİV": ["FROTO.IS", "TOASO.IS", "TTRAK.IS", "TMSN.IS"],
    "GIDA": ["ULKER.IS", "TATGD.IS", "CCOLA.IS", "AEFES.IS"],
    "ÇİMENTO": ["KONYA.IS", "CIMSA.IS", "GOLTS.IS"],
    "DEMİR-ÇELİK": ["EREGL.IS", "KRDMD.IS", "IZMDC.IS"],
    "KİMYA": ["SASA.IS", "GUBRF.IS", "AKSA.IS", "TUPRS.IS"],
    "SPOR": ["GSRAY.IS", "BJKAS.IS", "FENER.IS"],
    "SİGORTA": ["AKGRT.IS", "AGESA.IS"],
    "TELEKOMÜNİKASYON": ["TCELL.IS", "TTKOM.IS"],
    "TURİZM": ["MAALT.IS", "AYCES.IS", "PKENT.IS"]
}

# TÜM HİSSELER - Modal'da seçim için (Delist olanlar çıkarıldı)
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
        "ENJSA.IS", "AYDEM.IS", "AYES.IS", "AYGAZ.IS", "ZERGY.IS", "BIOEN.IS", 
        "EUREN.IS"
    ],
    
    "HOLDİNG": [
        "KCHOL.IS", "SAHOL.IS", "AGHOL.IS", "DOHOL.IS", "ECZYT.IS", "BIMAS.IS", 
        "SISE.IS", "AVHOL.IS", "IHEVA.IS", "TURSG.IS", "NTHOL.IS",
        "EUHOL.IS", "GRTHO.IS", "IEYHO.IS", "MZHLD.IS", "TRHOL.IS"
    ],
    
    "TEKNOLOJİ": [
        "LOGO.IS", "LINK.IS", "INDES.IS", "ARENA.IS", "KAREL.IS", "NETAS.IS", 
        "ESCOM.IS", "ALCTL.IS", "ANELE.IS", "DGATE.IS", "EDATA.IS", "FONET.IS",
        "INFO.IS", "INVEO.IS", "INTEM.IS", "NETCD.IS", "SMART.IS"
    ],
    
    "PERAKENDE": [
        "BIMAS.IS", "MGROS.IS", "SOKM.IS", "MAVI.IS", "CRFSA.IS", "MPARK.IS", 
        "ADESE.IS", "BIZIM.IS", "KOTON.IS"
    ],
    
    "OTOMOTİV": [
        "FROTO.IS", "TOASO.IS", "TTRAK.IS", "KLMSN.IS", "TMSN.IS", "GEREL.IS", 
        "PARSN.IS", "ASUZU.IS", "BFREN.IS", "DITAS.IS", "OTKAR.IS"
    ],
    
    "GIDA": [
        "ULKER.IS", "TATGD.IS", "PETUN.IS", "CCOLA.IS", "BANVT.IS", "PENGD.IS", 
        "KNFRT.IS", "AEFES.IS", "EKIZ.IS", "ERSU.IS", "PINSU.IS", "KENT.IS", 
        "BALSU.IS", "PNSUT.IS"
    ],
    
    "ÇİMENTO & İNŞAAT": [
        "KONYA.IS", "ENJSA.IS", "EGEEN.IS", "CIMSA.IS", "GOLTS.IS", "BTCIM.IS", 
        "BUCIM.IS", "NUHCM.IS", "AKCNS.IS", "CMENT.IS"
    ],
    
    "DEMİR-ÇELİK": [
        "EREGL.IS", "KRDMD.IS", "KRDMA.IS", "KRDMB.IS", "IZMDC.IS", "ERBOS.IS", 
        "BURCE.IS", "CELHA.IS", "DOKTA.IS", "ISDMR.IS", "CEMTS.IS"
    ],
    
    "KİMYA": [
        "SASA.IS", "GUBRF.IS", "AKSA.IS", "PETKM.IS", "TUPRS.IS", "GOODY.IS", 
        "ALKIM.IS", "BAGFS.IS", "BRISA.IS"
    ],
    
    "TEKSTİL": [
        "HEKTS.IS", "YUNSA.IS", "BRSAN.IS", "SKTAS.IS", "BLCYT.IS", "DAGI.IS", 
        "MAVI.IS", "ARSAN.IS", "ATEKS.IS", "DESA.IS", "DERIM.IS", "KRSTL.IS"
    ],
    
    "SPOR": [
        "GSRAY.IS", "BJKAS.IS", "FENER.IS", "TSPOR.IS"
    ],
    
    "TELEKOMÜNİKASYON": [
        "TCELL.IS", "TTKOM.IS"
    ],
    
    "SİGORTA": [
        "AKGRT.IS", "AGESA.IS", "ANSGR.IS", "ANHYT.IS"
    ],
    
    "MADENCİLİK": [
        "PAMEL.IS", "CMENT.IS", "IZMDC.IS", "GZNMI.IS"
    ],
    
    "TURİZM": [
        "MAALT.IS", "AYCES.IS", "MARTI.IS", "PKENT.IS", "MERIT.IS", "AVTUR.IS"
    ],
    
    "KAĞIT": [
        "KARTN.IS", "SILVR.IS"
    ],
    
    "MEDYA": [
        "IHLAS.IS", "IHLGM.IS", "IHYAY.IS", "IHGZT.IS"
    ],
    
    "İLAÇ": [
        "DEVA.IS", "SELEC.IS", "MTRKS.IS"
    ],
    
    "DAYANIKLI TÜKETİM": [
        "ARCLK.IS", "VESBE.IS", "ARZUM.IS", "EMKEL.IS"
    ],
    
    "KUYUMCULUK": [
        "GLDTR.IS", "ZGOLD.IS", "ALTNY.IS"
    ],
    
    "GYO": [
        "ADGYO.IS", "AGYO.IS", "AKFGY.IS", "ALGYO.IS", "AVGYO.IS", "BEGYO.IS",
        "DGGYO.IS", "DZGYO.IS", "EKGYO.IS", "EYGYO.IS", "GRNYO.IS", "HLGYO.IS",
        "IDGYO.IS", "ISGYO.IS", "KGYO.IS", "KLGYO.IS", "KRGYO.IS", "KZGYO.IS",
        "MRGYO.IS", "MSGYO.IS", "NUGYO.IS", "OZGYO.IS", "OZKGY.IS", "PAGYO.IS",
        "RYGYO.IS", "SNGYO.IS", "TDGYO.IS", "TRGYO.IS", "VKGYO.IS", "ZGYO.IS"
    ],
    
    "DİĞER": [
        "ALCAR.IS", "ASUZU.IS", "ATLAS.IS", "BASCM.IS", "BASGZ.IS",
        "BERA.IS", "BESLR.IS", "BEYAZ.IS", "BINHO.IS", "BLUME.IS", "BMSCH.IS",
        "BNTAS.IS", "BORLS.IS", "BOSSA.IS", "BRKO.IS", "BRMEN.IS", "BRYAT.IS",
        "BSOKE.IS", "BULGS.IS", "BURVA.IS", "BVSAN.IS", "CANTE.IS", "CASA.IS",
        "CEMAS.IS", "CEMZY.IS", "CONSE.IS", "COSMO.IS", "CUSAN.IS", "CVKMD.IS",
        "DERHL.IS", "DESPC.IS", "DIRIT.IS", "DMSAS.IS", "DNISI.IS", "DOAS.IS",
        "DOGUB.IS", "DURDO.IS", "DURKN.IS", "DYOBY.IS", "ECILC.IS", "ECOGR.IS",
        "EDIP.IS", "EFOR.IS", "EGPRO.IS", "EKOS.IS", "ELITE.IS", "EMNIS.IS",
        "ENDAE.IS", "ENERY.IS", "ENSRI.IS", "ENTRA.IS", "EPLAS.IS", "ERCB.IS",
        "ESCAR.IS", "ESEN.IS", "ETILR.IS", "ETYAT.IS", "FADE.IS", "FLAP.IS",
        "FORMT.IS", "FORTE.IS", "FRIGO.IS", "GARFA.IS", "GEDIK.IS", "GENIL.IS",
        "GENTS.IS", "GIPTA.IS", "GLBMD.IS", "GLCVY.IS", "GLDTR.IS", "GLRMK.IS",
        "GMSTR.IS", "GMTAS.IS", "GOKNR.IS", "GOZDE.IS", "GRSEL.IS", "GUNDG.IS",
        "GWIND.IS", "HATEK.IS", "HATSN.IS", "HEDEF.IS", "HOROZ.IS", "HRKET.IS",
        "HUBVC.IS", "HURGZ.IS", "IHAAS.IS", "INGRM.IS", "INTEK.IS", "INVES.IS",
        "ISBIR.IS", "ISGSY.IS", "ISKPL.IS", "ISMEN.IS", "ISSEN.IS", "ISYAT.IS",
        "IZENR.IS", "IZFAS.IS", "IZINV.IS", "JANTS.IS", "KAPLM.IS", "KBORU.IS",
        "KCAER.IS", "KIMMR.IS", "KLKIM.IS", "KLNMA.IS", "KLRHO.IS", "KLSER.IS",
        "KLSYN.IS", "KMPUR.IS", "KOCMT.IS", "KONKA.IS", "KOPOL.IS", "KRONT.IS",
        "KRPLS.IS", "KRTEK.IS", "KRVGD.IS", "KSTUR.IS", "KTLEV.IS", "KTSKR.IS",
        "KUTPO.IS", "KUVVA.IS", "KUYAS.IS", "KZBGY.IS", "LIDER.IS", "LILAK.IS",
        "LKMNH.IS", "LMKDC.IS", "LYDHO.IS", "MACKO.IS", "MAGEN.IS", "MAKIM.IS",
        "MAKTK.IS", "MANAS.IS", "MARBL.IS", "MARKA.IS", "MARMR.IS", "MEDTR.IS",
        "MEGMT.IS", "MEKAG.IS", "MERCN.IS", "METRO.IS", "MEYSU.IS", "MIATK.IS",
        "MMCAS.IS", "MNDRS.IS", "MOBTL.IS", "MOGAN.IS", "MOPAS.IS", "NATEN.IS",
        "OBASE.IS", "ODINE.IS", "ONCSM.IS", "ONRYT.IS", "ORGE.IS", "ORMA.IS",
        "OSMEN.IS", "OYAKC.IS", "OYYAT.IS", "OZRDN.IS", "OZSUB.IS", "OZYSR.IS",
        "PAPIL.IS", "PATEK.IS", "PASEU.IS", "PEKGY.IS", "PENTA.IS", "PLTUR.IS",
        "PNLSN.IS", "POLHO.IS", "PRKAB.IS", "PRKME.IS", "PRZMA.IS", "QUAGR.IS",
        "RALYH.IS", "RAYSG.IS", "RGYAS.IS", "RNPOL.IS", "RUBNS.IS", "RUZYE.IS",
        "SAFKR.IS", "SANKO.IS", "SARKY.IS", "SAYAS.IS", "SEGYO.IS", "SEKUR.IS",
        "SELVA.IS", "SERNT.IS", "SEYKM.IS", "SMRVA.IS", "SODSN.IS", "SOKE.IS",
        "SONME.IS", "SRVGY.IS", "SUMAS.IS", "SUNTK.IS", "SURGY.IS", "SUWEN.IS",
        "TABGD.IS", "TARKM.IS", "TATEN.IS", "TBORG.IS", "TCKRC.IS", "TEHOL.IS",
        "TEKTU.IS", "TERA.IS", "TEZOL.IS", "TGSAS.IS", "TKFEN.IS", "TKNSA.IS",
        "TLMAN.IS", "TMPOL.IS", "TNZTP.IS", "TRALT.IS", "TRCAS.IS", "TRENJ.IS",
        "TRILC.IS", "TRMET.IS", "TUCLK.IS", "TUKAS.IS", "TUREX.IS", "TURGG.IS",
        "UCAYM.IS", "UFUK.IS", "ULAS.IS", "ULUSE.IS", "ULUUN.IS", "UNLU.IS",
        "USAK.IS", "VAKKO.IS", "VANGD.IS", "VBTYZ.IS", "VERTU.IS", "VERUS.IS",
        "VESTL.IS", "VKING.IS", "VSNMD.IS", "YAPRK.IS", "YAYLA.IS", "YBTAS.IS",
        "YEOTK.IS", "YESIL.IS", "YIGIT.IS", "YKSLN.IS", "YONGA.IS", "YYAPI.IS",
        "YYLGD.IS", "ZEDUR.IS", "ZELOT.IS"
    ]
}

def get_stock_data(symbol):
    """Tek bir hisse için veri çeker"""
    try:
        t = yf.Ticker(symbol)
        h = t.history(period="2d")
        
        if len(h) < 2:
            return None
            
        degisim = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
        
        # Piyasa değeri
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

def get_data():
    # BIST 100 için veri (İlk ekranda gösterilecek)
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
    
    # TÜM HİSSELER için veri (Modal'da seçim için)
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
    
    # İki ayrı dosya kaydet
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(bist100_data, f, ensure_ascii=False, indent=2)
    
    with open('all_stocks.json', 'w', encoding='utf-8') as f:
        json.dump(tum_hisseler_data, f, ensure_ascii=False, indent=2)
    
    bist100_count = sum(len(s['data']) for s in bist100_data)
    total_count = sum(len(s['data']) for s in tum_hisseler_data)
    
    print(f"\n{'='*50}")
    print(f"✓ BIST 100: {bist100_count} hisse")
    print(f"✓ TÜM HİSSELER: {total_count} hisse")
    print(f"✓ {len(bist100_data)} sektör")
    print(f"{'='*50}")

if __name__ == "__main__":
    get_data()