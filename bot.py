import os
import requests
import json

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def ai_bulten_olustur():
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/KursunAhmet/NOSBTekstil",
        "X-Title": "NOSB Tekstil Bulten Bot"
    }
    
    prompt = """
Sen global ve yerel tekstil piyasalarını, emtia borsalarını anlık takip eden kıdemli bir Sektör Analistisin.
Bana Telegram üzerinden yayınlanmaya hazır, yüksek kaliteli, derli toplu ve kaynaklı bir sabah bülteni hazırla.

⚠️ ÇOK KESİN FORMAT & İÇERİK KURALLARI:
1. GİRİŞ/AÇILIŞ CÜMLESİ YAZMA! ("Tabii ki", "İşte bülten" vb. YASAK).
2. Yıldızları (**) rasgele kullanma! Başlıkları net ve temiz yap.
3. VERDİĞİN HER HABER VEYA VERİNİN YANINA PARANTEZ İÇİNDE KISA KAYNAK EKLE! (Örn: [Kaynak: USDA], [Kaynak: Bloomberg], [Kaynak: TGSD], [Kaynak: Niğde OSB Basın]).

BÜLTEN YAPISI:

🌍 **GLOBAL TEKSTİL & EMTİA PİYASALARI**
• Cotlook A, Brent Petrol ve Polyester Elyaf fiyatları + [Kaynak]
• ABD, Çin, Hindistan ve Pakistan pamuk/stok durumları + [Kaynak]
• AB Yeşil Mutabakatı, Dijital Ürün Pasaportu (DPP) gelişmeleri + [Kaynak]
• Asya üreticileri (Bangladeş, Vietnam) gelişmeleri + [Kaynak]

🇹🇷 **TÜRKİYE İHRACAT & HAM MADDE PİYASASI**
• İplik (Open-End, Ring) ve kumaş piyasası fiyat/talep hareketi + [Kaynak]
• İhracat pazarları (Almanya, İtalya, ABD) sipariş durumları + [Kaynak]

🏭 **NİĞDE OSB & BÖLGESEL SANAYİ BAKIŞI**
• Niğde OSB tekstil/elyaf devleri (Migiteks, Biska vb.) yatırımları ve OSB haberleri + [Kaynak]

💡 **GÜNÜN MÜHENDİSLİK & YÖNETİM TAVSİYESİ**
• Stajyer/Yönetici adayı için sahaya veya üretime dair 1 cümlelik profesyonel öğüt.

Biçimlendirme:
- Anlamlı emojiler kullan (🧵, 📊, 🌍, 🌾, 🏭, 💡).
- Telegram'da temiz görünecek şekilde başlıkları belirgin yap.
- En sona "🤖 _DeepSeek V4 Flash AI Otomasyonu ile Üretilmiştir_" ekle.
"""

    payload = {
        "model": "deepseek/deepseek-v4-flash",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=45)
        response_json = response.json()
        
        if "error" in response_json:
            return f"⚠️ OpenRouter API Hatası: {response_json['error']['message']}"
            
        return response_json['choices'][0]['message']['content']
        
    except Exception as e:
        return f"⚠️ Python Kod Hatası: {str(e)}"

def telegrama_gonder(mesaj):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mesaj,
        "parse_mode": "Markdown"  # YILDIZLARI VE FORMATI DÜZGÜN AŞAĞIYA YANSITAN KRİTİK AYAR!
    }
    res = requests.post(url, json=payload)
    
    # Eğer Markdown formatında bir hata çıkarsa düz metin olarak yedek gönder
    if res.status_code != 200:
        payload_plain = {
            "chat_id": CHAT_ID,
            "text": mesaj
        }
        requests.post(url, json=payload_plain)

if __name__ == "__main__":
    bulten = ai_bulten_olustur()
    telegrama_gonder(bulten)
