import os
import requests

# Secrets'tan gelecek bilgiler
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def gunluk_bulten_hazirla():
    rapor = """
📍 **NİĞDE OSB & TEKSTİL SEKTÖRÜ GÜNLÜK BÜLTENİ**
📅 *Günün Gelişmeleri*
--------------------------------------------------
🔹 **Niğde OSB Önemli Sanayi Notları:**
• **Migiteks Tekstil:** Tesisin ilk fazı 90 milyon $ yatırımla tamamlanarak yıllık 7 bin ton yerli likra (spandeks) üretimine başladı. 3. faz bittiğinde 240 milyon $ yatırım ve 35.000 ton kapasite hedefleniyor.
• **Biska Tekstil:** 150 bin m² alanda 3 etaplı Open-End İplik üretim tesisi yatırımı ve sanayi kapasite artışı devam ediyor.

🔹 **Tekstil & Ham Madde Genel Durum:**
• Pamuk, iplik ve elyaf piyasalarındaki fiyat değişimleri takip ediliyor.
• Bölgesel istihdam ve teşvik fırsatları Niğde OSB'yi tekstilde cazibe merkezi yapmaya devam ediyor.
--------------------------------------------------
💡 *Bu bülten GitHub Actions & DeepSeek V4 & Python otomasyonu ile Levent GÜLDEREN tarafından gönderilmiştir.*
"""
    return rapor

def telegrama_gonder(mesaj):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mesaj,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    bulten = gunluk_bulten_hazirla()
    telegrama_gonder(bulten)
