import yfinance as yf
import json

# TÜM BIST HİSSELERİ - Sektörel Sınıflandırma
SEKTOR_HARITASI = {
    "BANKA": [
        "AKBNK.IS", "ISCTR.IS", "GARAN.IS", "YKBNK.IS", "HALKB.IS", "VAKBN.IS", 
        "ICBCT.IS", "SKBNK.IS", "ALBRK.IS", "TSKB.IS", "QNBFB.IS", "QNBFK.IS"
    ],
    
    "SAVUNMA & HAVACILIK": [
        "ASELS.IS", "SDTTR.IS", "KORDS.IS", "OTKAR.IS", "REEDR.IS", "KATMR.IS",
        "THYAO.IS", "PGSUS.IS", "TAVHL.IS", "DOCO.IS", "CLEBI.IS", "RYSAS.IS"
    ],
    
    "ENERJİ": [
        "ASTOR.IS", "EUPWR.IS", "SMRTG.IS", "KONTR.IS", "ALARK.IS", "CWENE.IS", 
        "ODAS.IS", "AKENR.IS", "AKSEN.IS", "ZOREN.IS", "AYEN.IS", "HUNER.IS", 
        "ENJSA.IS", "AYDEM.IS", "AYES.IS", "AYGAZ.IS", "ZERGY.IS", "AKGRT.IS",
        "BIOEN.IS", "EUREN.IS", "ZRGYO.IS"
    ],
    
    "BANKA & FİNANS": [
        "AKFIN.IS", "AKFYE.IS", "ISFIN.IS", "VAKFA.IS", "VAKFN.IS"
    ],
    
    "DEMİR-ÇELİK & METAL": [
        "EREGL.IS", "KRDMD.IS", "KRDMA.IS", "KRDMB.IS", "IZMDC.IS", "ERBOS.IS", 
        "BURCE.IS", "CELHA.IS", "DOKTA.IS", "ISDMR.IS", "CEMTS.IS", "OZATD.IS"
    ],
    
    "KİMYA & PETROKIMYA": [
        "SASA.IS", "GUBRF.IS", "AKSA.IS", "PETKM.IS", "TUPRS.IS", "GOODY.IS", 
        "SODA.IS", "ALKIM.IS", "BAGFS.IS", "BRISA.IS", "MEPET.IS", "SNICE.IS"
    ],
    
    "TEKSTİL & HAZIR GİYİM": [
        "HEKTS.IS", "YUNSA.IS", "BRSAN.IS", "SKTAS.IS", "BLCYT.IS", "DAGI.IS", 
        "ROYAL.IS", "MAVI.IS", "ARSAN.IS", "ATEKS.IS", "DESA.IS", "DERIM.IS",
        "KRSTL.IS", "LUKSK.IS", "MARKA.IS", "YATAS.IS"
    ],
    
    "OTOMOTİV": [
        "FROTO.IS", "TOASO.IS", "TTRAK.IS", "KLMSN.IS", "TMSN.IS", "GEREL.IS", 
        "PARSN.IS", "ASUZU.IS", "BFREN.IS", "DITAS.IS", "EGEEN.IS", "FMIZP.IS",
        "KARSN.IS", "OTKAR.IS", "TTRAK.IS"
    ],
    
    "İNŞAAT & ÇİMENTO": [
        "KONYA.IS", "ENJSA.IS", "EGEEN.IS", "CIMSA.IS", "GOLTS.IS", "BTCIM.IS", 
        "ADANA.IS", "BUCIM.IS", "NUHCM.IS", "AKCNS.IS", "BOLUC.IS", "CMENT.IS"
    ],
    
    "TEKNOLOJİ & YAZILIM": [
        "LOGO.IS", "LINK.IS", "INDES.IS", "ARENA.IS", "KAREL.IS", "NETAS.IS", 
        "ESCOM.IS", "ALCTL.IS", "ANELE.IS", "DGATE.IS", "EDATA.IS", "FONET.IS",
        "INFO.IS", "INVEO.IS", "INTEM.IS", "KFEIN.IS", "NETCD.IS", "SMART.IS"
    ],
    
    "GIDA & İÇECEK": [
        "ULKER.IS", "TATGD.IS", "PETUN.IS", "CCOLA.IS", "BANVT.IS", "PENGD.IS", 
        "KNFRT.IS", "AEFES.IS", "EKIZ.IS", "ERSU.IS", "KERVT.IS", "PINSU.IS",
        "KENT.IS", "BALSU.IS", "BIZIM.IS", "MERKO.IS", "KERVN.IS", "PNSUT.IS"
    ],
    
    "HOLDİNG": [
        "KCHOL.IS", "SAHOL.IS", "AGHOL.IS", "DOHOL.IS", "ECZYT.IS", "BIMAS.IS", 
        "SISE.IS", "ARBUL.IS", "AVHOL.IS", "IHEVA.IS", "TURSG.IS", "NTHOL.IS",
        "EUHOL.IS", "GRTHO.IS", "IEYHO.IS", "MZHLD.IS", "TRHOL.IS"
    ],
    
    "PERAKENDE": [
        "BIMAS.IS", "MGROS.IS", "SOKM.IS", "MAVI.IS", "CRFSA.IS", "MPARK.IS", 
        "ADESE.IS", "BIZIM.IS", "KOTON.IS", "MPARK.IS"
    ],
    
    "SPOR": [
        "GSRAY.IS", "BJKAS.IS", "FENER.IS", "TSPOR.IS"
    ],
    
    "TELEKOMÜNİKASYON": [
        "TCELL.IS", "TTKOM.IS", "AKNET.IS"
    ],
    
    "SİGORTA": [
        "AKGRT.IS", "AGESA.IS", "ANSGR.IS", "ANHYT.IS"
    ],
    
    "MADENCİLİK": [
        "IPEKE.IS", "KOZAL.IS", "KOZAA.IS", "PAMEL.IS", "CMENT.IS", "IZMDC.IS",
        "GZNMI.IS"
    ],
    
    "TURİZM & OTEL": [
        "MAALT.IS", "AYCES.IS", "UTOPYA.IS", "MARTI.IS", "PKENT.IS", "Merit.IS",
        "AVTUR.IS"
    ],
    
    "KAĞIT": [
        "KARTN.IS", "OLMIP.IS", "SILVR.IS"
    ],
    
    "MEDYA & YAYINCILIK": [
        "IHLAS.IS", "IHLGM.IS", "IHYAY.IS", "IHGZT.IS"
    ],
    
    "İLAÇ & SAĞLIK": [
        "DEVA.IS", "SELEC.IS", "MTRKS.IS"
    ],
    
    "DAYANIKLI TÜKETİM": [
        "ARCLK.IS", "VESBE.IS", "ARZUM.IS", "EMKEL.IS", "KRONE.IS"
    ],
    
    "KUYUMCULUK": [
        "KOZAL.IS", "KOZAA.IS", "IPEKE.IS", "GLDTR.IS", "ZGOLD.IS", "ALTNY.IS"
    ],
    
    "ENERJI SANTRALİ": [
        "AKSEN.IS", "AKENR.IS", "ZOREN.IS", "EUPWR.IS", "SMRTG.IS", "CWENE.IS"
    ],
    
    "İNŞAAT MALZEMESİ": [
        "CIMSA.IS", "GOLTS.IS", "KONYA.IS", "NUHCM.IS", "ADANA.IS", "BOLUC.IS"
    ],
    
    "DENIZCILIK": [
        "CLEBI.IS", "DOCO.IS", "RYSAS.IS", "VAPO.IS"
    ],
    
    "REIT (GYO)": [
        "ADGYO.IS", "AGYO.IS", "AKFGY.IS", "ALGYO.IS", "ATAGY.IS", "AVGYO.IS",
        "BEGYO.IS", "DGGYO.IS", "DZGYO.IS", "EKGYO.IS", "EYGYO.IS", "GRNYO.IS",
        "HLGYO.IS", "IDGYO.IS", "ISGYO.IS", "KGYO.IS", "KLGYO.IS", "KRGYO.IS",
        "KZGYO.IS", "MRGYO.IS", "MSGYO.IS", "MTRYO.IS", "NUGYO.IS", "OZGYO.IS",
        "OZKGY.IS", "PAGYO.IS", "PSGYO.IS", "RYGYO.IS", "SNGYO.IS", "TDGYO.IS",
        "TRGYO.IS", "TSGYO.IS", "VKFYO.IS", "VKGYO.IS", "VRGYO.IS", "YGGYO.IS",
        "ZGYO.IS", "ZRGYO.IS"
    ],
    
    "DİĞER SANAYİ": [
        "ALCAR.IS", "ANACM.IS", "ASUZU.IS", "ATLAS.IS", "BASCM.IS", "BASGZ.IS",
        "BAYRK.IS", "BERA.IS", "BESLR.IS", "BEYAZ.IS", "BINHO.IS", "BLUME.IS",
        "BMSCH.IS", "BMSTL.IS", "BNTAS.IS", "BOBET.IS", "BORLS.IS", "BORSK.IS",
        "BOSSA.IS", "BRKO.IS", "BRKSN.IS", "BRKVY.IS", "BRLSM.IS", "BRMEN.IS",
        "BRYAT.IS", "BSOKE.IS", "BULGS.IS", "BURVA.IS", "BVSAN.IS", "BYDNR.IS",
        "CANTE.IS", "CASA.IS", "CATES.IS", "CEMAS.IS", "CEMZY.IS", "CEOEM.IS",
        "CGCAM.IS", "CONSE.IS", "COSMO.IS", "CRDFA.IS", "CUSAN.IS", "CVKMD.IS",
        "DAPGM.IS", "DARDL.IS", "DCTTR.IS", "DENGE.IS", "DERHL.IS", "DESPC.IS",
        "DGNMO.IS", "DIRIT.IS", "DMRGD.IS", "DMSAS.IS", "DNISI.IS", "DOAS.IS",
        "DOFER.IS", "DOFRB.IS", "DOGUB.IS", "DSTKF.IS", "DUNYH.IS", "DURDO.IS",
        "DURKN.IS", "DYOBY.IS", "EBEBK.IS", "ECILC.IS", "ECOGR.IS", "EDIP.IS",
        "EFOR.IS", "EGEGY.IS", "EGEPO.IS", "EGGUB.IS", "EGPRO.IS", "EGSER.IS",
        "EKOS.IS", "EKSUN.IS", "ELITE.IS", "EMNIS.IS", "ENDAE.IS", "ENERY.IS",
        "ENSRI.IS", "ENTRA.IS", "EPLAS.IS", "ERCB.IS", "ESCAR.IS", "ESEN.IS",
        "ETILR.IS", "ETYAT.IS", "EUKYO.IS", "EUYO.IS", "FADE.IS", "FLAP.IS",
        "FORMT.IS", "FORTE.IS", "FRIGO.IS", "FRMPL.IS", "FZLGY.IS", "GARFA.IS",
        "GATEG.IS", "GEDIK.IS", "GEDZA.IS", "GENIL.IS", "GENTS.IS", "GIPTA.IS",
        "GLBMD.IS", "GLCVY.IS", "GLRMK.IS", "GLRYH.IS", "GLYHO.IS", "GMSTR.IS",
        "GMTAS.IS", "GOKNR.IS", "GOZDE.IS", "GRSEL.IS", "GSDDE.IS", "GSDHO.IS",
        "GUNDG.IS", "GWIND.IS", "HALKS.IS", "HATEK.IS", "HATSN.IS", "HDFGS.IS",
        "HEDEF.IS", "HKTM.IS", "HOROZ.IS", "HRKET.IS", "HTTBT.IS", "HUBVC.IS",
        "HURGZ.IS", "ICUGS.IS", "IHAAS.IS", "IMASM.IS", "INGRM.IS", "INTEK.IS",
        "INVES.IS", "ISBIR.IS", "ISGLK.IS", "ISGSY.IS", "ISKPL.IS", "ISMEN.IS",
        "ISSEN.IS", "ISYAT.IS", "IZENR.IS", "IZFAS.IS", "IZINV.IS", "JANTS.IS",
        "KAPLM.IS", "KAYSE.IS", "KBORU.IS", "KCAER.IS", "KERVN.IS", "KIMMR.IS",
        "KLKIM.IS", "KLNMA.IS", "KLRHO.IS", "KLSER.IS", "KLSYN.IS", "KLYPV.IS",
        "KMPUR.IS", "KOCMT.IS", "KONKA.IS", "KOPOL.IS", "KRONT.IS", "KRPLS.IS",
        "KRTEK.IS", "KRVGD.IS", "KSTUR.IS", "KTLEV.IS", "KTSKR.IS", "KUTPO.IS",
        "KUVVA.IS", "KUYAS.IS", "KZBGY.IS", "LIDER.IS", "LIDFA.IS", "LILAK.IS",
        "LKMNH.IS", "LMKDC.IS", "LRSHO.IS", "LYDHO.IS", "MACKO.IS", "MAGEN.IS",
        "MAKIM.IS", "MAKTK.IS", "MANAS.IS", "MARBL.IS", "MARMR.IS", "MEDTR.IS",
        "MEGAP.IS", "MEGMT.IS", "MEKAG.IS", "MERCN.IS", "METRO.IS", "MEYSU.IS",
        "MHRGY.IS", "MIATK.IS", "MMCAS.IS", "MNDRS.IS", "MNDTR.IS", "MOBTL.IS",
        "MOGAN.IS", "MOPAS.IS", "NATEN.IS", "NIBAS.IS", "NPTLR.IS", "NTGAZ.IS",
        "OBAMS.IS", "OBASE.IS", "ODINE.IS", "OFSYM.IS", "ONCSM.IS", "ONRYT.IS",
        "ORCAY.IS", "ORGE.IS", "ORMA.IS", "OSMEN.IS", "OSTIM.IS", "OTTO.IS",
        "OYAKC.IS", "OYAYO.IS", "OYLUM.IS", "OYYAT.IS", "OZRDN.IS", "OZSUB.IS",
        "OZYSR.IS", "PAHOL.IS", "PAPIL.IS", "PATEK.IS", "PASEU.IS", "PCILT.IS",
        "PEKGY.IS", "PENTA.IS", "PKART.IS", "PLTUR.IS", "PNLSN.IS", "POLHO.IS",
        "POLTK.IS", "PRDGS.IS", "PRKAB.IS", "PRKME.IS", "PRZMA.IS", "PSDTC.IS",
        "QUAGR.IS", "RALYH.IS", "RAYSG.IS", "RGYAS.IS", "RNPOL.IS", "RODRG.IS",
        "RTALB.IS", "RUBNS.IS", "RUZYE.IS", "SAFKR.IS", "SAMAT.IS", "SANEL.IS",
        "SANFM.IS", "SANKO.IS", "SARKY.IS", "SAYAS.IS", "SEGMN.IS", "SEGYO.IS",
        "SEKFK.IS", "SEKUR.IS", "SELVA.IS", "SERNT.IS", "SEYKM.IS", "SKYLP.IS",
        "SKYMD.IS", "SMRVA.IS", "SNPAM.IS", "SODSN.IS", "SOKE.IS", "SONME.IS",
        "SRVGY.IS", "SUMAS.IS", "SUNTK.IS", "SURGY.IS", "SUWEN.IS", "TABGD.IS",
        "TARKM.IS", "TATEN.IS", "TBORG.IS", "TCKRC.IS", "TEHOL.IS", "TEKTU.IS",
        "TERA.IS", "TEZOL.IS", "TGSAS.IS", "TKFEN.IS", "TKNSA.IS", "TLMAN.IS",
        "TMPOL.IS", "TNZTP.IS", "TRALT.IS", "TRCAS.IS", "TRENJ.IS", "TRILC.IS",
        "TRMET.IS", "TUCLK.IS", "TUKAS.IS", "TUREX.IS", "TURGG.IS", "UCAYM.IS",
        "UFUK.IS", "ULAS.IS", "ULUFA.IS", "ULUSE.IS", "ULUUN.IS", "UNLU.IS",
        "USAK.IS", "VAKKO.IS", "VANGD.IS", "VBTYZ.IS", "VERTU.IS", "VERUS.IS",
        "VESTL.IS", "VKING.IS", "VSNMD.IS", "YAPRK.IS", "YAYLA.IS", "YBTAS.IS",
        "YEOTK.IS", "YESIL.IS", "YIGIT.IS", "YKSLN.IS", "YONGA.IS", "YYAPI.IS",
        "YYLGD.IS", "ZEDUR.IS", "ZELOT.IS"
    ]
}

def get_data():
    output = []
    toplam_hisse = 0
    
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
                if market_cap == 0 or market_cap is None:
                    shares = info.get('sharesOutstanding', 0)
                    price = h['Close'].iloc[-1]
                    if shares and shares > 0:
                        market_cap = shares * price
                    else:
                        market_cap = 1000000  # Varsayılan değer
                
                sektor_verisi["data"].append({
                    "x": sym.replace(".IS", ""), 
                    "y": round(degisim, 2),
                    "z": int(market_cap) if market_cap > 0 else 1000000
                })
                
                toplam_hisse += 1
                print(f"✓ {sym.replace('.IS', '')} - %{round(degisim, 2)}")
                
            except Exception as e:
                print(f"✗ Hata: {sym} - {e}")
                continue
        
        # Piyasa değerine göre sırala (büyükten küçüğe)
        sektor_verisi["data"].sort(key=lambda x: x.get('z', 0), reverse=True)
        
        if sektor_verisi["data"]:
            output.append(sektor_verisi)
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*50}")
    print(f"✓ TOPLAM {toplam_hisse} HİSSE GÜNCELLENDİ!")
    print(f"✓ {len(output)} SEKTÖR İŞLENDİ!")
    print(f"{'='*50}")

if __name__ == "__main__":
    get_data()