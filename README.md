# 💊 İlaç Veri Setleri Eşleştirme (Record Linkage) Projesi

Bu proje, farklı kaynaklardan elde edilen ve ortak bir birleştirme anahtarı (ID/Barkod vb.) bulunmayan iki devasa ilaç veri setinin (TİTCK ve ATC Listeleri) **Metin Madenciliği (Text Mining)** ve **Bulanık Eşleştirme (Fuzzy Matching)** yöntemleriyle eşleştirilmesini amaçlamaktadır.

## 🎯 Projenin Amacı
Projenin temel hedefi; Türkiye İlaç ve Tıbbi Cihaz Kurumu (TİTCK) listesinde bulunan ~15.500 ilaç kaydını, uluslararası ATC (Anatomik Terapötik Kimyasal) sınıflama sistemine ait ~17.900 kayıtlık veri tabanıyla yüksek doğruluk oranında çaprazlayıp eşleştirmektir.

Eşleştirme işleminde salt "İlaç Adı" kullanılması yetersiz kalacağı için **İlaç Adı**, **Etkin Madde** ve **Firma** bilgileri birleştirilerek ortak bir metin uzayı oluşturulmuştur.

## 🛠️ Kullanılan Teknolojiler ve Yöntemler
- **Python** & **Jupyter Notebook**
- **Pandas** & **NumPy** (Veri Manipülasyonu ve Analizi)
- **Scikit-learn** (Makine Öğrenmesi ve Vektörizasyon)
- **Regex (Düzenli İfadeler)** (Veri Temizleme)

### Eşleştirme Algoritması (TF-IDF & Cosine Similarity)
On binlerce satırlık veri setlerini klasik satır-satır karşılaştırma algoritmalarıyla (Levenshtein vb.) taramak son derece maliyetli ve yavaş olacağından, projede **TF-IDF Vektörizasyonu** ve **Kosinüs Benzerliği (Cosine Similarity)** tercih edilmiştir.

Dil farklılıklarını (*parasetamol* vs *paracetamol*) tolere edebilmek için metinler kelime bazında değil, **Karakter N-Gram (2-4 harfli hece grupları)** bazında vektörlere ayrıştırılmış ve iki uzay arasındaki vektörel açılar/benzerlikler hesaplanarak eşleşme skorları çıkarılmıştır.

## 🚀 Çalışma Adımları

1. **Veri Yükleme:** TİTCK (`.csv`) ve ATC (`.xlsx`) veri setlerinin okunması.
2. **Veri Temizleme (Pre-processing):** 
   - Türkçe karakterlerin dönüştürülmesi.
   - Metinlerin küçük harfe çevrilmesi.
   - Noktalama işaretlerinin (%, -, /, vb.) ve fazlalık boşlukların temizlenmesi.
3. **Kombinasyon:** Her iki liste için de `İlaç Adı + Etkin Madde + Firma` bilgilerinin tek bir `Combined_Text` sütununda birleştirilmesi.
4. **Vektörizasyon:** ATC listesi üzerinden `char_wb` analyzer ile TF-IDF matrisinin eğitilmesi ve TİTCK listesinin bu uzaya dönüştürülmesi.
5. **Kosinüs Benzerliği:** Her bir TİTCK kaydına karşılık gelen en yüksek benzerlik skoruna sahip ATC kaydının bulunması.
6. **Dışa Aktarma:** Benzerlik skoru `%70 ve üzeri` olan verilerin filtrelenip `eslesmis_veriler.csv` olarak dışa aktarılması.

## 📂 Dosya Yapısı
- `record_linkage_project.ipynb`: Projenin tüm veri temizleme ve makine öğrenmesi adımlarını barındıran kaynak kod.
- `titck_liste_18.04.csv` & `ATC_14_04.xlsx`: Ham veri setleri.
- `eslesmis_veriler.csv`: Algoritma sonucunda üretilen nihai eşleşme tablosu.
- `proje_raporu.md`: Uygulanan adımların Türkçe akademik/proje özeti.

## 💡 Kurulum ve Kullanım
Projeyi lokalinizde çalıştırmak için aşağıdaki kütüphanelerin yüklü olduğundan emin olun:

```bash
pip install pandas numpy scikit-learn openpyxl jupyter
```
Ardından terminal üzerinden klasöre gidip Jupyter Notebook'u başlatabilirsiniz:
```bash
jupyter notebook record_linkage_project.ipynb
```
Azo İsmail - GitHub Contribution