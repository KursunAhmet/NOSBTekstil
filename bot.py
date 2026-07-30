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
Sen global ve yerel tekstil piyasalarını, emtia borsalarını takip eden kıdemli bir Sektör Analistisin.
Web araması yaparak GÜNCEL verileri topla ve Telegram üzerinden yayınlanmaya hazır, derli toplu, kaynaklı bir sabah bülteni hazırla.

⚠️ DOĞRULUK KURALLARI (EN ÖNEMLİ KURALLAR):
- SADECE web arama sonuçlarında gerçekten bulduğun verileri yaz.
- Arama sonucunda bulamadığın fiyat, haber veya şirket gelişmesini ASLA uydurma.
- Veri bulamadığın madde için "Bugün için doğrulanmış veri bulunamadı" yaz.
- Kaynak olarak sadece arama sonucundaki GERÇEK site/kurum adını yaz, kaynak uydurma.
- Özellikle Niğde OSB ve yerel şirketler (Migiteks, Biska vb.) hakkında web'de haber bulamazsan hikaye YAZMA, "bölgesel yeni haber yok" de.

⚠️ FORMAT KURALLARI:
1. GİRİŞ/AÇILIŞ CÜMLESİ YAZMA! ("Tabii ki", "İşte bülten" vb. YASAK).
2. Yıldızları (**) rasgele kullanma! Başlıkları net ve temiz yap.
3. Verdiğin her veri/haberin yanına parantez içinde kısa kaynak ekle (Örn: [Kaynak: USDA]).

BÜLTEN YAPISI:

🌍 **GLOBAL TEKSTİL & EMTİA PİYASALARI**
- Cotlook A, Brent Petrol ve Polyester Elyaf fiyatları + [Kaynak]
- ABD, Çin, Hindistan ve Pakistan pamuk/stok durumları + [Kaynak]
- AB Yeşil Mutabakatı, Dijital Ürün Pasaportu (DPP) gelişmeleri + [Kaynak]
- Asya üreticileri (Bangladeş, Vietnam) gelişmeleri + [Kaynak]

🇹🇷 **TÜRKİYE İHRACAT & HAM MADDE PİYASASI**
- İplik (Open-End, Ring) ve kumaş piyasası fiyat/talep hareketi + [Kaynak]
- İhracat pazarları (Almanya, İtalya, ABD) sipariş durumları + [Kaynak]

🏭 **NİĞDE OSB & BÖLGESEL SANAYİ BAKIŞI**
- Niğde OSB ve bölge tekstil/elyaf firmaları hakkında web'de bulunan GERÇEK haberler + [Kaynak]
- Haber yoksa dürüstçe "Bölgesel yeni haber bulunamadı" yaz.

💡 **GÜNÜN MÜHENDİSLİK & YÖNETİM TAVSİYESİ**
- Stajyer/Yönetici adayı için sahaya veya üretime dair 1 cümlelik profesyonel öğüt.

Biçimlendirme:
- Anlamlı emojiler kullan (🧵, 📊, 🌍, 🌾, 🏭, 💡).
- Telegram'da temiz görünecek şekilde başlıkları belirgin yap.
- En sona "🤖 _DeepSeek V4 Flash AI Otomasyonu ile Üretilmiştir_" ekle.
"""

    payload = {
        "model": "deepseek/deepseek-v4-flash:online",  # :online = web araması aktif
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        # Web aramalı istekler yavaş döner, timeout yüksek tutuldu
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=120)
        response_json = response.json()

        if "error" in response_json:
            return f"⚠️ OpenRouter API Hatası: {response_json['error']['message']}"

        return response_json['choices'][0]['message']['content']

    except Exception as e:
        return f"⚠️ Python Kod Hatası: {str(e)}"


def mesaji_parcala(mesaj, limit=4000):
    """Telegram'ın 4096 karakter limitini aşan mesajları satır sonlarından böler."""
    if len(mesaj) <= limit:
        return [mesaj]

    parcalar = []
    kalan = mesaj
    while len(kalan) > limit:
        # Limit içindeki son satır sonundan böl ki cümle ortadan kesilmesin
        kesme_noktasi = kalan.rfind("\n", 0, limit)
        if kesme_noktasi == -1:
            kesme_noktasi = limit
        parcalar.append(kalan[:kesme_noktasi])
        kalan = kalan[kesme_noktasi:].lstrip("\n")
    if kalan:
        parcalar.append(kalan)
    return parcalar


def telegrama_gonder(mesaj):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    for parca in mesaji_parcala(mesaj):
        payload = {
            "chat_id": CHAT_ID,
            "text": parca,
            "parse_mode": "Markdown"
        }
        res = requests.post(url, json=payload)

        # Markdown hatası çıkarsa düz metin olarak yedek gönder
        if res.status_code != 200:
            payload_plain = {
                "chat_id": CHAT_ID,
                "text": parca
            }
            requests.post(url, json=payload_plain)


if __name__ == "__main__":
    bulten = ai_bulten_olustur()
    telegrama_gonder(bulten)
