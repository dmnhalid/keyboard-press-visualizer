# Klavye Göstergesi (Türkçe Q)

Sistem genelinde bastığın tuşu ekrandaki sanal klavyede yakıp söndüren araç.
Hangi programda olursan ol (oyun, tarayıcı, Word...) çalışır.

## Kurulum

1. [Python 3](https://www.python.org/downloads/) kurulu olmalı.
   (Kurarken "Add Python to PATH" kutusunu işaretle.)
2. Bağımlılığı kur:
   ```
   pip install keyboard
   ```

## Çalıştırma

```
python klavye_gosterge.py
```

> **Önemli:** `keyboard` kütüphanesi tüm sistemi dinlediği için, bazı
> durumlarda (özellikle yönetici haklı başka programlar açıkken) betiğin
> **yönetici olarak** çalıştırılması gerekebilir.
>
> Yönetici olarak çalıştırmak için: Başlat menüsünde **PowerShell**'e sağ
> tıkla → "Yönetici olarak çalıştır", sonra:
> ```
> cd "C:\Users\Halid\Desktop\keyboard tuşlamaları"
> python klavye_gosterge.py
> ```

## Kullanım

- Pencere açıldıktan sonra istediğin programda yaz; bastığın tuşlar
  ekrandaki klavyede mavi renkte yanar, bırakınca söner.
- Shift / Ctrl / Alt gibi tuşlar da yandığı için kombinasyonları görürsün.
- Kapatmak için pencereyi kapat.

## Notlar

- Düzen: Türkçe Q.
- Sol/sağ Ctrl ve Alt aynı fiziksel koda sahip olduğundan birlikte yanabilir
  (küçük bir görsel sınırlama).
