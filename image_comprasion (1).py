import cv2
import os
import time
import numpy as np
from skimage.metrics import structural_similarity as ssim

# Belirtilen klasörden resimleri yükleriz


def klasorden_resim_yukle(klasor):
    resimler = []
    for dosya_adi in os.listdir(klasor):
        resim = cv2.imread(os.path.join(klasor, dosya_adi))
        if resim is not None:
            resimler.append(resim)
    return resimler

# İki resim arasındaki benzerlik skorunu hesaplarız


def benzerlik_hesapla(resimA, resimB):
    resimA = cv2.cvtColor(resimA, cv2.COLOR_BGR2GRAY)
    resimB = cv2.cvtColor(resimB, cv2.COLOR_BGR2GRAY)

    # Görüntüler küçük olanın boyutlarına yeniden boyutlandırılır
    if resimA.shape != resimB.shape:
        yukseklik = min(resimA.shape[0], resimB.shape[0])
        genislik = min(resimA.shape[1], resimB.shape[1])
        resimA = cv2.resize(resimA, (genislik, yukseklik))
        resimB = cv2.resize(resimB, (genislik, yukseklik))

    return ssim(resimA, resimB)

# Görüntüler arasındaki benzerlik skorlarını buluruz


def benzer_resimleri_bul(resimler):
    benzerlik_listesi = []
    for i in range(len(resimler)):
        for j in range(i + 1, len(resimler)):
            benzerlik = benzerlik_hesapla(resimler[i], resimler[j])
            benzerlik_listesi.append((i, j, benzerlik))

    # Benzerlik skorlarına göre listeyi büyükten küçüğe sıralar
    benzerlik_listesi.sort(key=lambda x: x[2], reverse=True)

    return benzerlik_listesi

# Belirtilen klasördeki görüntüler arasında benzer olanları buluruz


def klasordeki_benzer_resimleri_bul(klasor_yolu):
    resimler = klasorden_resim_yukle(klasor_yolu)
    benzerlik_listesi = benzer_resimleri_bul(resimler)
    return benzerlik_listesi


klasor_yolu = r"C:\Users\user\Desktop\python\opencv_project\resim"

baslama_zamani = time.time()
benzerlik_listesi = klasordeki_benzer_resimleri_bul(klasor_yolu)
bitis_zamani = time.time()

# Benzerlik skoru tam 1 olan görüntü çiftlerini ekranda yazdırırız
for i, j, skor in benzerlik_listesi:
    if skor == 1.0:
        print(f"Görüntüler {i} ve {j} benzerlik skoru {skor} ile benzer.")

# Toplamda kaç karşılaştırma yapıldığını ekranda gösterir
print(f"Toplamda {len(benzerlik_listesi)} karşılaştırma yapıldı.")
print(f"Kodun çalışma süresi: {bitis_zamani - baslama_zamani} saniye.")
