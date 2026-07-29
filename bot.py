import os
import requests
import json

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def telegrama_gonder(mesaj):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    # Formatlama hatası yüzünden Telegram'ın mesajı reddetmesini önlemek için 
    # parse_mode kullanmıyoruz (düz metin olarak atacak)
    payload = {
        "chat_id": CHAT_ID,
        "text": mesaj
    }
    requests.post(url, json=payload)

def ai_bulten_olustur():
    # Değişken kontrolü
    if not OPENROUTER_API_KEY:
        return "⚠️ HATA: OPENROUTER_API_KEY GitHub Secrets tarafında bulunamadı!"
    
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
4. Stajyer bir mühendis/yönetici adayı için günün kısa tavsiyesi.

Format:
- Mobil ekranda rahat okunsun.
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
        
        if "error" in response_json:
            return f"⚠️ OpenRouter Dönüş Hatası:\n{json.dumps(response_json['error'], indent=2)}"
            
        if "choices" in response_json and len(response_json["choices"]) > 0:
            return response_json['choices'][0]['message']['content']
        else:
            return f"⚠️ Yanıt Yapısı Geçersiz:\n{json.dumps(response_json, indent=2)}"
            
    except Exception as e:
        return f"⚠️ Python Kod İstek Hatası: {str(e)}"

if __name__ == "__main__":
    bulten = ai_bulten_olustur()
    telegrama_gonder(bulten)
