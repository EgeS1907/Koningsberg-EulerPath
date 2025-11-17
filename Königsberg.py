import pygame
import sys
from collections import defaultdict
import time

# --- Pygame Başlangıç Ayarları ---
pygame.init()
WIDTH, HEIGHT = 800, 600
ekran = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Königsberg Köprü Problemi - Euler Yolu & Devresi")

# --- Renk Tanımları ---
BEYAZ = (255, 255, 255)
SIYAH = (0, 0, 0)
MAVI = (0, 100, 200)   # Nehir/Arkaplan
GRI = (150, 150, 150)   # Kullanılmamış köprüler
YESIL = (0, 200, 100)  # Kullanılmış köprüler
KIRMIZI = (200, 50, 50)  # Düğümler
SARI = (255, 255, 0) # Aktif Düğüm

# --- Graf Veri Yapısı ---
dugumler = {
    'A': (200, 300), 'B': (400, 150),
    'C': (400, 450), 'D': (600, 300)
}

# --- YENİ: Toplam 8 Köprü Tanımlıyoruz ---
# Orijinal 7 köprü + 1 ekstra köprü (Devre için)
kenarlar = [
    ('A', 'B'), ('A', 'B'),  # 0, 1
    ('A', 'C'), ('A', 'C'),  # 2, 3
    ('A', 'D'),              # 4
    ('B', 'D'),              # 5
    ('C', 'D'),              # 6 (İmkansız problemdeki 7. köprü)
    ('A', 'B')               # 7 (Devre sahnesi için 8. köprü)
]

# Sahnelere göre hangi köprülerin aktif olduğunu tanımlayacağız
SAHNE_IMKANSIZ_KENARLARI = {0, 1, 2, 3, 4, 5, 6}
SAHNE_PATH_KENARLARI = {0, 1, 2, 3, 4, 5}
SAHNE_DEVRE_KENARLARI = {0, 1, 2, 3, 4, 5, 7} # 6 yerine 7'yi kullan

# --- Euler Algoritması Mantığı ---

def hesapla_dereceler(aktif_kenar_listesi):
    """Verilen kenar listesine göre dereceleri hesaplar."""
    dereceler = defaultdict(int)
    for u, v in aktif_kenar_listesi:
        dereceler[u] += 1
        dereceler[v] += 1
    return dereceler

def euler_yolu_kontrol(dereceler):
    """
    Hesaplanan derecelere göre Euler yolu/devresi olup olmadığını kontrol eder.
    'dereceler' sözlüğü SADECE kenarı olan düğümleri içerir.
    """
    tek_dereceli_dugumler = []
    tum_dugumler = set(dugumler.keys()) # A, B, C, D
    
    print("--- Derece Analizi ---")
    for dugum in tum_dugumler:
        # dereceler.get(dugum, 0) ile 0 dereceli düğümleri de (çift) say
        derece = dereceler.get(dugum, 0) 
        print(f"Düğüm {dugum}: {derece} derece (Tek: {derece % 2 != 0})")
        if derece % 2 != 0:
            tek_dereceli_dugumler.append(dugum)
    print("------------------------")
            
    if len(tek_dereceli_dugumler) == 0:
        print("Sonuç: Euler Devresi Mümkün.")
        # --- DÜZELTME BURADA ---
        # Başlangıç olarak kenarı olan (dereceler'de olan) bir düğümü seç.
        # Eğer graf tamamen boşsa (0 kenar) None döndür.
        if not dereceler:
            print("Graf boş, yol yok.")
            return "Yok", None # Graf boşsa
        
        # Kenarı olan ilk düğümden başla
        baslangic = list(dereceler.keys())[0] 
        return "Devre", baslangic
        # --- DÜZELTME SONU ---
        
    elif len(tek_dereceli_dugumler) == 2:
        print("Sonuç: Euler Yolu Mümkün.")
        # Başlangıç tek derecelilerden biri olmalı
        return "Yol", tek_dereceli_dugumler[0] 
    else:
        print(f"Sonuç: Euler Yolu/Devresi Mümkün Değil ({len(tek_dereceli_dugumler)} tek dereceli düğüm).")
        return "Yok", None

# --- Yolu Bulan Algoritma ---

# Bu değişkenler her sahne değişiminde sıfırlanacak
graph_komsu_kenarlar = defaultdict(list)
bulunan_yol_kenarlari = []
kullanilmis_kenarlar_seti = set()

def bul_euler_yolunu(mevcut_dugum):
    """
    Hierholzer'in algoritması (DFS tabanlı) 
    Global 'bulunan_yol_kenarlari' listesini doldurur.
    Kullandığı 'graph_komsu_kenarlar' globaldir.
    """
    for kenar_index in graph_komsu_kenarlar[mevcut_dugum]:
        if kenar_index not in kullanilmis_kenarlar_seti:
            kullanilmis_kenarlar_seti.add(kenar_index)
            u, v = kenarlar[kenar_index] # Global kenar listesini kullanır
            diger_dugum = v if u == mevcut_dugum else u
            bul_euler_yolunu(diger_dugum)
            bulunan_yol_kenarlari.append(kenar_index)

# --- Çizim Fonksiyonları ---

def ciz_grafigi(ekran, aktif_kenar_indeksleri, kullanilmis_kenarlar_idx=set(), aktif_dugum=None):
    """
    Sadece 'aktif_kenar_indeksleri' setinde olan kenarları çizer.
    """
    ekran.fill(MAVI)
    
    # --- YENİ: Paralel Köprüleri Dinamik Çizme ---
    # Hangi köprülerin paralel olduğunu sayalım
    cizilecek_kenarlar = defaultdict(list)
    for i in aktif_kenar_indeksleri:
        u, v = kenarlar[i]
        # (A,B) ile (B,A) aynıdır
        key = tuple(sorted((u, v))) 
        cizilecek_kenarlar[key].append(i)

    font = pygame.font.Font(None, 30)

    # 1. Kenarları Çiz
    for (u, v), indeksler in cizilecek_kenarlar.items():
        baslangic_pos = dugumler[u]
        bitis_pos = dugumler[v]
        
        # Birden fazla paralel köprü varsa aralarını aç
        toplam = len(indeksler)
        for i, kenar_idx in enumerate(indeksler):
            renk = GRI 
            if kenar_idx in kullanilmis_kenarlar_idx:
                renk = YESIL
            
            # Aralığı hesapla (dikey veya yatay olarak hafifçe kaydır)
            # Bu basit bir kaydırma, mükemmel değil ama çalışır
            offset = 10 * (i - (toplam - 1) / 2)
            
            # Dikey mi yatay mı kaydıracağına karar ver
            if abs(baslangic_pos[0] - bitis_pos[0]) > abs(baslangic_pos[1] - bitis_pos[1]):
                # Daha çok yatay giden köprü, dikey kaydır
                start = (baslangic_pos[0], baslangic_pos[1] + offset)
                end = (bitis_pos[0], bitis_pos[1] + offset)
            else:
                # Daha çok dikey giden köprü, yatay kaydır
                start = (baslangic_pos[0] + offset, baslangic_pos[1])
                end = (bitis_pos[0] + offset, bitis_pos[1])
                
            pygame.draw.line(ekran, renk, start, end, 4)

    # 2. Düğümleri Çiz (Kenarların üstünde olması için)
    for dugum in dugumler:
        konum = dugumler[dugum]
        renk = KIRMIZI
        if dugum == aktif_dugum:
            renk = SARI 
        pygame.draw.circle(ekran, renk, konum, 20) 
        yazi = font.render(dugum, True, BEYAZ)
        ekran.blit(yazi, (konum[0] - yazi.get_width() // 2, konum[1] - yazi.get_height() // 2))

# --- Algoritmayı Hazırlama Fonksiyonu ---

def hazirla_ve_calistir_algoritma(aktif_kenar_indeksleri):
    """
    Verilen kenar indekslerine göre algoritmayı kurar ve çalıştırır.
    Global 'bulunan_yol_kenarlari' listesini doldurur.
    """
    global graph_komsu_kenarlar, bulunan_yol_kenarlari, kullanilmis_kenarlar_seti
    
    # 1. Algoritma değişkenlerini sıfırla
    graph_komsu_kenarlar.clear()
    bulunan_yol_kenarlari.clear()
    kullanilmis_kenarlar_seti.clear()
    
    # 2. Sadece aktif kenarları kullanarak grafı kur
    aktif_kenar_listesi_tuple = []
    for i in aktif_kenar_indeksleri:
        u, v = kenarlar[i]
        graph_komsu_kenarlar[u].append(i)
        graph_komsu_kenarlar[v].append(i)
        aktif_kenar_listesi_tuple.append((u,v))
        
    # 3. Dereceleri kontrol et ve başlangıç düğümünü bul
    dereceler = hesapla_dereceler(aktif_kenar_listesi_tuple)
    yol_durumu, baslangic_dugumu = euler_yolu_kontrol(dereceler)
    
    if yol_durumu == "Yok":
        return None, [] # Animasyon yok
        
    # 4. Yolu bul
    bul_euler_yolunu(baslangic_dugumu)
    
    # Yolu tersine çevir ve animasyon için döndür
    animasyon_yolu = list(reversed(bulunan_yol_kenarlari))
    print(f"Hesaplanan {yol_durumu} animasyon yolu (indeksler): {animasyon_yolu}")
    return baslangic_dugumu, animasyon_yolu

# --- Ana Oyun Döngüsü ---
def main():
    
    program_durumu = "SAHNE_IMKANSIZ"
    aktif_kenar_indeksleri = SAHNE_IMKANSIZ_KENARLARI
    
    # Orijinal (imkansız) grafiği analiz et
    print("--- SAHNE 1: İMKANSIZ PROBLEM (7 Köprü) ---")
    hazirla_ve_calistir_algoritma(aktif_kenar_indeksleri)
    
    animasyon_yolu = []
    mevcut_animasyon_adimi = 0
    kullanilan_animasyon_kenarlari = set()
    son_adim_zamani = 0.0
    animasyon_aktif_dugum = None

    calisiyor = True
    saat = pygame.time.Clock()
    
    font_buyuk = pygame.font.Font(None, 50)
    font_kucuk = pygame.font.Font(None, 30)

    while calisiyor:
        # --- Olay (Event) İşleme ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                calisiyor = False
            
            if event.type == pygame.KEYDOWN:
                # --- SAHNE 1 -> SAHNE 2 (PATH) ---
                if event.key == pygame.K_SPACE and program_durumu == "SAHNE_IMKANSIZ":
                    print("\n--- SAHNE 2: EULER YOLU (6 Köprü) ---")
                    program_durumu = "SAHNE_PATH_ANIMASYON"
                    aktif_kenar_indeksleri = SAHNE_PATH_KENARLARI
                    
                    # Yolu hesapla
                    baslangic, yol = hazirla_ve_calistir_algoritma(aktif_kenar_indeksleri)
                    
                    # Animasyonu kur
                    animasyon_yolu = yol
                    mevcut_animasyon_adimi = 0
                    kullanilan_animasyon_kenarlari.clear()
                    animasyon_aktif_dugum = baslangic
                    son_adim_zamani = time.time()
                    
                # --- SAHNE 2 -> SAHNE 3 (DEVRE) ---
                elif event.key == pygame.K_c and program_durumu == "SAHNE_PATH_BITTI":
                    print("\n--- SAHNE 3: EULER DEVRESİ (7 Köprü - Yeni) ---")
                    program_durumu = "SAHNE_DEVRE_ANIMASYON"
                    aktif_kenar_indeksleri = SAHNE_DEVRE_KENARLARI
                    
                    # Devreyi hesapla
                    baslangic, yol = hazirla_ve_calistir_algoritma(aktif_kenar_indeksleri)

                    # Animasyonu kur
                    animasyon_yolu = yol
                    mevcut_animasyon_adimi = 0
                    kullanilan_animasyon_kenarlari.clear() # Sıfırla
                    animasyon_aktif_dugum = baslangic
                    son_adim_zamani = time.time()

        # --- Animasyon Mantığı ---
        if program_durumu == "SAHNE_PATH_ANIMASYON" or program_durumu == "SAHNE_DEVRE_ANIMASYON":
            simdiki_zaman = time.time()
            if (simdiki_zaman - son_adim_zamani > 1.0): # Her 1 saniyede bir
                if mevcut_animasyon_adimi < len(animasyon_yolu):
                    kenar_index = animasyon_yolu[mevcut_animasyon_adimi]
                    kullanilan_animasyon_kenarlari.add(kenar_index)
                    
                    u, v = kenarlar[kenar_index]
                    animasyon_aktif_dugum = v if u == animasyon_aktif_dugum else u
                    
                    mevcut_animasyon_adimi += 1
                    son_adim_zamani = simdiki_zaman
                else:
                    # Animasyon bitti
                    if program_durumu == "SAHNE_PATH_ANIMASYON":
                        program_durumu = "SAHNE_PATH_BITTI"
                    elif program_durumu == "SAHNE_DEVRE_ANIMASYON":
                        program_durumu = "SAHNE_DEVRE_BITTI"
                    animasyon_aktif_dugum = None 

        # --- Çizim ---
        cizim_kenarlari = set(aktif_kenar_indeksleri)
        
        # Devreye hazırlık sahnesinde, yeni köprüyü de (gri) göster
        if program_durumu == "SAHNE_PATH_BITTI":
            cizim_kenarlari.add(7) # 7. köprüyü (A-B) gri olarak ekle
            
        ciz_grafigi(ekran, cizim_kenarlari, kullanilan_animasyon_kenarlari, animasyon_aktif_dugum)
        
        # --- Ekran Üstü Yazıları (Duruma bağlı) ---
        if program_durumu == "SAHNE_IMKANSIZ":
            yazi_imkansiz = font_buyuk.render("Euler Yolu Mümkün Değil!", True, BEYAZ, SIYAH)
            ekran.blit(yazi_imkansiz, (WIDTH//2 - yazi_imkansiz.get_width()//2, 20))
            yazi_devam = font_kucuk.render("Yol animasyonu için SPACE tuşuna basın", True, BEYAZ)
            ekran.blit(yazi_devam, (WIDTH//2 - yazi_devam.get_width()//2, 70))
            
        elif program_durumu == "SAHNE_PATH_BITTI":
            yazi_path_bitti = font_buyuk.render("Euler Yolu Tamamlandı!", True, BEYAZ, SIYAH)
            ekran.blit(yazi_path_bitti, (WIDTH//2 - yazi_path_bitti.get_width()//2, 20))
            yazi_devam = font_kucuk.render("Devre animasyonu için 'C' tuşuna basın", True, BEYAZ)
            ekran.blit(yazi_devam, (WIDTH//2 - yazi_devam.get_width()//2, 70))
            
        elif program_durumu == "SAHNE_DEVRE_BITTI":
            yazi_devre_bitti = font_buyuk.render("Euler Devresi Tamamlandı!", True, BEYAZ, SIYAH)
            ekran.blit(yazi_devre_bitti, (WIDTH//2 - yazi_devre_bitti.get_width()//2, 20))

        pygame.display.flip()
        saat.tick(60) 

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()