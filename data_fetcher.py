import yfinance as yf
import json
import re

# Senin gönderdiğin ham liste (Hepsini buraya ekledim, script içinden ayıklayacak)
RAW_DATA = """
A1CAP 16.103.8718:09:38 A1YEN 30.80-0.2618:05:13 ACSEL 111.704.3918:09:00 ADEL 35.082.3918:09:20 
ADESE 1.181.7218:09:13 ADGYO 62.15-4.4618:09:48 AEFES 20.181.0018:09:50 AFYON 14.44-0.7618:05:13 
ASELS 288.001.0518:09:50 SASA 2.42-2.8118:09:49 THYAO 322.501.7418:09:49
""" # Buraya senin yukarıdaki listenin tamamını yapıştırabilirsin.

def fetch_bist_data():
    # Hisse kodlarını ayıkla (Büyük harf 4-5 karakterli kelimeler)
    ticker_list = re.findall(r'[A-Z0-9]{3,5}', RAW_DATA)
    ticker_list = list(set([t + ".IS" for t in ticker_list if not t.isdigit()]))
    
    print(f"{len(ticker_list)} hisse işleniyor...")
    
    final_data = [{"name": "BIST TÜM", "data": []}]
    
    for symbol in ticker_list:
        try:
            t = yf.Ticker(symbol)
            hist = t.history(period="2d")
            if len(hist) < 2: continue
            
            # Değişim ve Piyasa Değeri
            change = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100
            mcap = t.info.get('marketCap', 1000000) # Değer yoksa küçük kutu yap
            
            final_data[0]["data"].append({
                "x": symbol.replace(".IS", ""),
                "y": mcap,
                "c": round(change, 2)
            })
            print(f"Başarılı: {symbol}")
        except:
            continue
            
    with open('data.json', 'w') as f:
        json.dump(final_data, f)
    print("Veri başarıyla data.json dosyasına yazıldı!")

if __name__ == "__main__":
    fetch_bist_data()