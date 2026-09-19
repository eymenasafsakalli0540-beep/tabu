# Tabu — Siret-i Nebi (Flask sürümü)

## Render.com'a deploy (önerilen — okula sadece bir link götürürsünüz)

1. Bu klasörü bir **GitHub reposuna** yükleyin (repo public ya da private olabilir).
2. [render.com](https://render.com) üzerinde ücretsiz hesap açın, **"New +" → "Web Service"** deyin, GitHub reponuzu bağlayın.
3. Ayarlar:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - Environment: Python 3
4. **Deploy** deyin. Birkaç dakika sonra size şuna benzer gerçek bir adres verir:
   `https://tabu-siret.onrender.com`
5. Okulda akıllı tahtada bu adresi açın → **tahta modu** (QR + skor + süre).
6. Telefonla QR'ı okutun → **kontrol modu** açılır. Artık aynı WiFi'da olma zorunluluğu yok, ikisi de sadece internete bağlı olsun yeterli.

> Not: Render'ın ücretsiz planında sunucu birkaç dakika kullanılmazsa uykuya geçer, ilk açılışta 20-30 saniye gecikme olabilir. Dersten biraz önce bir kere açıp "uyandırmanız" yeterli.

## Yerel test (opsiyonel)
```
pip install -r requirements.txt
python app.py
```
Tarayıcıda `http://localhost:5000` açılır (sadece kendi bilgisayarınızda test için).

## Notlar
- Kelime listesi `app.py` içindeki `WORDS` listesinden değiştirilebilir.
- Oyunu sıfırlamak için: `POST https://<adresiniz>/api/reset`
- `Procfile` içindeki `web: gunicorn app:app` satırı Render'ın uygulamayı nasıl başlatacağını söyler, dokunmanıza gerek yok.
