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
Sen Niğde OSB ve Tekstil sektörü için uzman bir sanayi analistisin. 
Bana bugün için Telegram'dan gönderilmeye uygun, kısa, vurucu ve profesyonel bir sabah bülteni hazırla.

Bültende şu konulara odaklan:
1. Niğde OSB (Organize Sanayi Bölgesi) yatırımları, tekstil/elyaf/iplik fabrikaları (Migiteks, Biska vb.) ve sanayi haberleri.
2. Türkiye genel tekstil sektörü, pamuk/iplik piyasaları ve ihracat durumları.
3. Global piyasada tekstil sektörü ile ilgili haberler ve olaylar.
4. Stajyer bir mühendis/yönetici adayı için günün kısa tavsiyesi veya dikkat edilmesi gereken 1 teknik not.

Format:
- Emoji ve Markdown başlıkları kullan (Kalın yazılar, liste işaretleri vb.).
- Çok uzun olmasın, mobil ekranda 1-2 kaydırmada okunabilsin.
- Sonunda "🤖 DeepSeek V4 Flash AI Otomasyonu ile Üretilmiştir" imzası olsun.
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
        
        # OpenRouter bir hata döndürdüyse hatayı Telegram'a bas
        if "error" in response_json:
            return f"⚠️ OpenRouter API Hatası: {response_json['error']['message']}"
            
        bulten = response_json['choices'][0]['message']['content']
        return bulten
        
    except Exception as e:
        return f"⚠️ Python Kod Hatası: {str(e)}"

def telegrama_gonder(mesaj):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mesaj,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    canli_bulten = ai_bulten_olustur()
    telegrama_gonder(canli_bulten)
