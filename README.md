# Pharma-DSS: İlaç Tedarik Zinciri İçin Bulanık ÇKKV Modeli

Bu depo, Türkiye'deki ilaç tedarik zincirinde yaşanan erişilebilirlik sorunları ve krizlere yönelik stratejik çözüm alternatiflerini değerlendiren, Python tabanlı bir Karar Destek Sistemi (KDS) algoritmasını içermektedir.

Geliştirilen model, uzman değerlendirmelerindeki belirsizlikleri analitik olarak yönetebilmek amacıyla Bulanık TOPSIS ve Bulanık VIKOR Çok Kriterli Karar Verme (ÇKKV) yöntemlerini hibrit bir yapıda çalıştırmaktadır.

## Proje Özeti
* **Amaç:** Hayati ilaç tedarik zincirinde karşılaşılan lojistik, finansal ve yapısal riskleri minimize edecek en optimal stratejik alternatifi matematiksel modelleme ile saptamak.
* **Kullanılan Yöntemler:** Üçgensel Bulanık Sayılar (ÜBS), Bulanık TOPSIS (İdeal Çözüme Yakınlık) ve Bulanık VIKOR (Uzlaşık Grup Faydası).
* **Nihai Sonuç:** Algoritma çıktılarına göre, kriz yönetimi ve risk azaltma kapasitesi açısından en başarılı strateji "Merkezi Dijital Dağıtım ve Önceliklendirme Sistemi (A1)" olarak belirlenmiştir.

## Kullanılan Teknolojiler
* Python 3.11 (Çekirdek Algoritma)
* NumPy (Bulanık sayı aritmetiği ve çok boyutlu matris işlemleri)
* Pandas (Veri manipülasyonu ve matris yapılandırması)
* Matplotlib & Seaborn (Veri görselleştirme ve analitik raporlama)

## Karşılaştırmalı Analiz Sonuçları
Sistem, girdi olarak verilen karar matrisini işleyerek TOPSIS için Yakınlık Katsayısı ($C_i$) ve VIKOR için Uzlaşık İndeks ($Q_i$) değerlerini dinamik olarak hesaplar ve görselleştirir.

<img width="2389" height="1313" alt="image" src="https://github.com/user-attachments/assets/ccac1523-9edc-4582-bafb-2c61cb59a672" />

## Kurulum ve Çalıştırma
Geliştirilen modeli yerel ortamda çalıştırmak ve farklı karar senaryolarını test etmek için aşağıdaki adımları izleyebilirsiniz:

1. Depoyu klonlayın: 
   `git clone https://github.com/KULLANICI_ADIN/Pharma-DSS.git`
2. Gerekli kütüphaneleri yükleyin: 
   `pip install numpy pandas matplotlib seaborn`
3. Modeli çalıştırın: 
   `python ckkv_model.py`
