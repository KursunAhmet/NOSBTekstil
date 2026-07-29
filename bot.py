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
    
    # GELİŞTİRİLMİŞ VE KATI KURALLI PROMPT
    prompt = """
Sen global ve yerel tekstil piyasalarını, emtia borsalarını ve sanayi devlerini anlık takip eden kıdemli bir Sektör Analistisin. 
Bana Telegram üzerinden yayınlanmaya hazır, zengin emojili, yüksek kaliteli ve profesyonel bir sabah bülteni hazırla.

⚠️ ÇOK KESİN KURAL:
"Tabii ki", "İşte bülteniniz", "Merhaba" gibi HİÇBİR giriş/açılış cümlesi YAZMA. Doğrudan başlıktan başla!

BÜLTEN İÇERİK MİMARİSİ:

📌 **GLOBAL TEKSTİL & EMTİA PİYASALARI**
• Cotton #2 (Cotlook A), Brent Petrol ve Polyester Elyaf fiyat trendleri.
• ABD (USDA raporları), Çin, Hindistan ve Pakistan pamuk rekolte/stok durumları.
• AB Yeşil Mutabakatı, Dijital Ürün Pasaportu (DPP) ve Karbon Vergisi güncellemeleri.
• Asya üreticileri (Bangladeş, Vietnam) ve küresel tedarik zinciri değişimleri.

🇹🇷 **TÜRKİYE İHRACAT & HAM MADDE PİYASASI**
• Türkiye iplik (Open-End, Ring) ve kumaş piyasasındaki fiyat/talep hareketleri.
• İhracat pazarları (Almanya, İtalya, ABD) ve hazır giyim sipariş durumları.

🏭 **NİĞDE OSB & BÖLGESEL SANAYİ BAKIŞI**
• Niğde OSB tekstil/elyaf/iplik devlerinin (Migiteks, Biska vb.) genel sanayi durumu, lojistik ve teşvik fırsatları.

💡 **GÜNÜN MÜHENDİSLİK & YÖNETİM TAVSİYESİ**
• Stajyer/Yönetici adayı için sahaya, verimliliğe veya kalite kontrole dair 1 cümlelik profesyonel öğüt.

Biçimlendirme Kriterleri:
- Bol ve anlamlı emojiler kullan (🧵, 📊, 🌍, 🌾, 🏭, 💡).
- Şık ve okuması kolay bir düzen sun.
- En sona "🤖 *DeepSeek V4 Flash AI Otomasyonu ile Üretilmiştir*" imzası ekle.
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
        "text": mesaj
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    bulten = ai_bulten_olustur()
    telegrama_gonder(bulten)
