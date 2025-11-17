# Königsberg'in 7 Köprüsü: Euler Yolu Simülatörü

Bu proje, Python ve Pygame kullanılarak geliştirilmiş, Graf Teorisi'nin doğuşuna yol açan ünlü "Königsberg'in 7 Köprüsü" probleminin interaktif bir görselleştirmesidir.

Proje, bir grafın neden "imkansız" olduğunu, nasıl "Euler Yolu" (Eulerian Path) ve "Euler Devresi" (Eulerian Circuit) haline getirilebileceğini adım adım gösterir.



## 🎯 Projenin Amacı

Bu simülatörün temel amacı, Leonhard Euler'in graf teorisi üzerine kurduğu temel teoremleri görsel ve interaktif bir şekilde açıklamaktır:
1.  **İmkansız Problemi Göstermek:** Orijinal Königsberg grafiğinin neden çözümsüz olduğunu (4 tek dereceli düğüm) göstermek.
2.  **Euler Yolu'nu Canlandırmak:** Grafı 2 tek dereceli düğüme sahip olacak şekilde düzenleyerek (bir köprü kaldırarak) bir Euler Yolu'nun nasıl bulunduğunu canlandırmak.
3.  **Euler Devresi'ni Canlandırmak:** Grafı tüm düğümleri çift dereceli olacak şekilde düzenleyerek (farklı bir köprü ekleyerek) bir Euler Devresi'nin (başladığı yere dönen yol) nasıl bulunduğunu canlandırmak.

## 🛠️ Teknik Detaylar

* **Dil:** Python
* **Kütüphane:** `Pygame` (Görselleştirme ve interaktif kontroller için)
* **Temel Algoritma:** Euler yolu/devresini bulmak için **DFS (Derinlik Öncelikli Arama)** tabanlı bir algoritma (Hierholzer'in algoritmasının bir varyantı) kullanılmıştır.
* **Veri Yapıları:** Graf, düğümleri (node) ve kenarları (edge) temsil eden listeler ve `defaultdict` (komşuluk listesi için) kullanılarak modellenmiştir.

## 🚀 Nasıl Kullanılır?

Programı çalıştırdığınızda, üç farklı sahne ile karşılaşırsınız:

1.  **Sahne 1: İmkansız Problem**
    * Königsberg'in orijinal 7 köprülü hali gösterilir.
    * Ekranda "Euler Yolu Mümkün Değil!" yazar.
    * **Kontrol:** Sonraki adıma geçmek için `SPACE` tuşuna basın.

2.  **Sahne 2: Euler Yolu (Path)**
    * Graf, bir köprü kaldırılarak 6 köprülü hale (2 tek dereceli düğüm) getirilir.
    * Algoritma çalışır ve bulunan Euler Yolu (bir düğümde başlayıp farklı bir düğümde biten) adım adım canlandırılır.
    * **Kontrol:** Animasyon bittiğinde sonraki adıma geçmek için `C` tuşuna basın.

3.  **Sahne 3: Euler Devresi (Circuit)**
    * Graf, tüm düğümleri çift dereceli olacak şekilde yeniden düzenlenir.
    * Algoritma çalışır ve bulunan Euler Devresi (bir düğümde başlayıp aynı düğümde biten) adım adım canlandırılır.