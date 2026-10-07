# picfit 🖼️⚡

**EN | Batch resize & convert photos in seconds — 100% offline, EXIF/GPS stripped by default.**
**TR | FotoSığdır — Fotoğrafları saniyeler içinde toplu boyutlandır ve dönüştür — %100 çevrimdışı, EXIF/GPS varsayılan olarak silinir.**

Sending 20 photos by e-mail? Uploading to a portal that rejects >2 MB? Posting
photos online without leaking your **GPS location**? One command:

20 fotoğrafı e-postayla mı göndereceksiniz? 2 MB üstünü reddeden bir portala mı
yüklüyorsunuz? **GPS konumunuzu** sızdırmadan fotoğraf mı paylaşacaksınız? Tek komut:

```bash
python picfit.py ./Photos --max 1920 --apply      # EN: longest side 1920px | TR: uzun kenar 1920px
python picfit.py ./DCIM --format webp --apply     # EN: convert folder to WebP | TR: klasörü WebP'ye çevir
python picfit.py IMG_*.jpg --percent 40 --apply   # EN: shrink to 40 % | TR: %40'a küçült
python picfit.py selfie.jpg                       # EN: strip GPS/EXIF only | TR: sadece GPS/EXIF sil
```

```
✔ big.png: 4000x2000 -> 1920x960  106.1 KB -> 30.5 KB, exif stripped
✔ mid.jpg: 1600x900 -> 800x450 -> WEBP  44.9 KB -> 7.1 KB, exif stripped
```

---

## 🇬🇧 English

### Why?

- Online resizers = **uploading your private photos to strangers' servers**.
- Photo editors = overkill for "make these smaller".
- And almost nobody knows their photos **carry GPS coordinates and camera serials**
  when posted online. `picfit` removes that by default.

### Privacy

| | Default | `--keep-exif` |
|---|---|---|
| GPS location | ❌ removed | ✅ kept |
| Camera make/serial | ❌ removed | ✅ kept |
| Date taken | ❌ removed | ✅ kept |

Verified by test: metadata written into a JPEG comes out **empty** after `picfit`.

### Install

```bash
pip install pillow
curl -LO https://raw.githubusercontent.com/Volvox6767/picfit/main/picfit.py
```

One dependency (Pillow), one file.

### Usage

```
python picfit.py INPUT... [--max PX | --percent N | --width PX | --height PX]
                   [--format jpg|png|webp] [--quality N] [--out DIR]
                   [--apply] [--keep-exif] [--recursive]

INPUT...      image files and/or folders
--max PX      longest side becomes PX (keeps aspect, never upscales)
--percent N   scale to N %
--width/--height PX   set one side, keep aspect
--format      convert: jpg / png / webp
--quality     JPEG/WebP quality (default 85)
--out DIR     write results to DIR instead of *_fit.* files
--apply       really write (default: dry-run preview)
--keep-exif   keep metadata (default: strip)
```

Input formats: jpg, png, webp, bmp, gif, tiff. Output: jpg / png / webp.

With **no resize option**, picfit runs in *privacy mode*: re-saves every photo
same-size with metadata stripped.

### Notes

- Animated GIFs are skipped (safety).
- Dry-run preview by default — nothing is written until `--apply`.
- Originals are never touched: results go to `*_fit.*` or `--out DIR`.

### FAQ

**Will it ruin quality?** LANCZOS resampling + optimized JPEG/WebP. 85 quality is visually transparent for sharing.

**Upscaling?** Never — smaller images are left as-is.

---

## 🇹🇷 Türkçe

### Neden?

- Online boyutlandırıcılar = **özel fotoğraflarınızı tanımadığınız sunuculara yüklemek**.
- Fotoğraf editörleri = "bunları küçült" işi için fazlasıyla gereksiz.
- Üstelik çoğu kişi bilmez: internete yüklediğiniz fotoğraflar **GPS koordinatı ve
  kamera seri numarası** taşır. `picfit` bunları varsayılan olarak siler.

### Gizlilik

| | Varsayılan | `--keep-exif` |
|---|---|---|
| GPS konumu | ❌ silinir | ✅ korunur |
| Kamera marka/seri no | ❌ silinir | ✅ korunur |
| Çekim tarihi | ❌ silinir | ✅ korunur |

Testle doğrulandı: JPEG'e yazılan metadata, `picfit` sonrası **boş** çıkıyor.

### Kurulum

```bash
pip install pillow
curl -LO https://raw.githubusercontent.com/Volvox6767/picfit/main/picfit.py
```

Tek bağımlılık (Pillow), tek dosya.

### Kullanım

```
python picfit.py GİRDİ... [--max PX | --percent N | --width PX | --height PX]
                   [--format jpg|png|webp] [--quality N] [--out KLASÖR]
                   [--apply] [--keep-exif] [--recursive]

GİRDİ...         görsel dosyaları ve/veya klasörleri
--max PX         uzun kenar PX olur (oran korunur, asla büyütmez)
--percent N      %N boyutuna ölçekle
--width/--height PX   bir kenarı ayarla, oranı koru
--format         dönüştür: jpg / png / webp
--quality        JPEG/WebP kalitesi (varsayılan 85)
--out KLASÖR     sonuçları *_fit.* yerine KLASÖR'e yaz
--apply          gerçekten yaz (varsayılan: dry-run önizleme)
--keep-exif      metadata'yı koru (varsayılan: sil)
```

Girdi biçimleri: jpg, png, webp, bmp, gif, tiff. Çıktı: jpg / png / webp.

**Boyut seçeneği verilmeyince** picfit *gizlilik modunda* çalışır: her fotoğrafı
aynı boyutta, metadata'sız yeniden kaydeder.

### Notlar

- Animasyonlu GIF'ler atlanır (güvenlik).
- Varsayılan dry-run önizleme — `--apply` gelene kadar hiçbir şey yazılmaz.
- Orijinallere asla dokunulmaz: sonuçlar `*_fit.*` veya `--out KLASÖR`'e gider.

### SSS

**Kaliteyi bozar mı?** LANCZOS yeniden örnekleme + optimize JPEG/WebP. 85 kalitesi paylaşım için gözle ayırt edilmez.

**Büyütme yapar mı?** Asla — küçük görsellere dokunulmaz.

---

Made with ❤ by **Ahmet Gedik** — [instagram.com/ahmetgedik67](https://www.instagram.com/ahmetgedik67)
Follow on Instagram for more free everyday tools.
Daha fazla ücretsiz günlük araç için Instagram'da takip edin.

License / Lisans: [MIT](LICENSE)
