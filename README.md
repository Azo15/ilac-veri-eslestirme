# 💊 İlaç Veri Setleri Eşleştirme (Record Linkage) & Pharma Matching Engine

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?style=for-the-badge&logo=jupyter&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F89939?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 🇹🇷 Türkçe Dokümantasyon

Bu proje, farklı kaynaklardan elde edilen ve ortak bir birleştirme anahtarı (ID/Barkod vb.) bulunmayan iki devasa ilaç veri setinin (TİTCK ve ATC Listeleri) **Metin Madenciliği (Text Mining)** ve **Bulanık Eşleştirme (Fuzzy Matching)** yöntemleriyle eşleştirilmesini amaçlamaktadır.

### 🎯 Projenin Amacı
Projenin temel hedefi; Türkiye İlaç ve Tıbbi Cihaz Kurumu (TİTCK) listesinde bulunan ~15.500 ilaç kaydını, uluslararası ATC (Anatomik Terapötik Kimyasal) sınıflama sistemine ait ~17.900 kayıtlık veri tabanıyla yüksek doğruluk oranında çaprazlayıp eşleştirmektir.

Eşleştirme işleminde salt "İlaç Adı" kullanılması yetersiz kalacağı için **İlaç Adı**, **Etkin Madde** ve **Firma** bilgileri birleştirilerek ortak bir metin uzayı oluşturulmuştur.

### 🛠️ Kullanılan Teknolojiler ve Yöntemler
- **Python** & **Jupyter Notebook**
- **Pandas** & **NumPy** (Veri Manipülasyonu ve Analizi)
- **Scikit-learn** (Makine Öğrenmesi ve Vektörizasyon)
- **Regex (Düzenli İfadeler)** (Veri Temizleme)

#### Eşleştirme Algoritması (TF-IDF & Cosine Similarity)
On binlerce satırlık veri setlerini klasik satır-satır karşılaştırma algoritmalarıyla (Levenshtein vb.) taramak son derece maliyetli ve yavaş olacağından, projede **TF-IDF Vektörizasyonu** ve **Kosinüs Benzerliği (Cosine Similarity)** tercih edilmiştir.

Dil farklılıklarını (*parasetamol* vs *paracetamol*) tolere edebilmek için metinler kelime bazında değil, **Karakter N-Gram (2-4 harfli hece grupları)** bazında vektörlere ayrıştırılmış ve iki uzay arasındaki vektörel açılar/benzerlikler hesaplanarak eşleşme skorları çıkarılmıştır.

### 🚀 Çalışma Adımları
1. **Veri Yükleme:** TİTCK (`.csv`) ve ATC (`.xlsx`) veri setlerinin okunması.
2. **Veri Temizleme (Pre-processing):** Türkçe karakterlerin dönüştürülmesi, küçük harfe çevirme, noktalama işaretlerinin ve fazlalık boşlukların temizlenmesi.
3. **Kombinasyon:** Her iki liste için de `İlaç Adı + Etkin Madde + Firma` bilgilerinin tek bir `Combined_Text` sütununda birleştirilmesi.
4. **Vektörizasyon:** ATC listesi üzerinden `char_wb` analyzer ile TF-IDF matrisinin eğitilmesi ve TİTCK listesinin bu uzaya dönüştürülmesi.
5. **Kosinüs Benzerliği:** Her bir TİTCK kaydına karşılık gelen en yüksek benzerlik skoruna sahip ATC kaydının bulunması.
6. **Dışa Aktarma:** Benzerlik skoru `%70 ve üzeri` olan verilerin filtrelenip `eslesmis_veriler.csv` olarak dışa aktarılması.

---

## 🇬🇧 English Documentation

### 📌 Overview
**Pharma Record Linkage** is a high-performance data processing pipeline designed to merge and cross-reference two large, unstructured pharmaceutical datasets that lack a common primary key or barcode identifier:
1. **TİTCK Dataset:** ~15,500 medicine records from the Turkish Medicines and Medical Devices Agency.
2. **ATC Dataset:** ~17,900 international records classified under the Anatomical Therapeutic Chemical system.

By combining **Text Mining**, **Character N-Gram Vectorization**, and **Fuzzy String Matching**, the engine identifies matching cross-border drug records with high accuracy and speed.

### 🎯 Key Objectives
* **Unsupervised Record Linkage:** Match disparate datasets without relying on explicit database keys.
* **Unified Text Space:** Merge distinct attributes (`Drug Name`, `Active Ingredient`, and `Manufacturer/Company`) into a comprehensive search context to reduce false positives.
* **Typo & Language Tolerance:** Overcome language and spelling variations (e.g., *parasetamol* vs. *paracetamol*) across international standards.

### 🛠️ Methodology & Technical Details
Standard row-by-row fuzzy matching algorithms suffer from heavy computational complexity. To overcome this, the engine leverages **TF-IDF Vectorization** paired with **Cosine Similarity**:

1. **Preprocessing & Normalization:** Standardizes Turkish non-ASCII characters and strips noise via regex.
2. **Contextual Aggregation:** Combines `Brand Name + Active Ingredient + Company` into a single representation per entry.
3. **Sub-word N-Gram Tokenization:** Uses `char_wb` (character N-grams within word boundaries, length 2–4) to vectorize text across language barriers.
4. **Cosine Similarity Computation:** Computes vector angles to determine match scores and exports pairs with confidence >= 70% to `eslesmis_veriler.csv`.

---

## 📂 Repository Structure

- record_linkage_project.ipynb   # Main workflow notebook with full ETL and matching pipeline
- titck_liste_18.04.csv          # TİTCK raw dataset (~15,500 records)
- ATC_14_04.xlsx                 # ATC raw dataset (~17,900 records)
- eslesmis_veriler.csv           # Exported output with similarity confidence scores
- proje_raporu.md                # Detailed project documentation (TR)
- README.md                      # Project documentation

---

## 💡 Kurulum ve Kullanım / Getting Started

### Gereksinimler / Prerequisites
pip install pandas numpy scikit-learn openpyxl jupyter

### Projeyi Çalıştırma / Running the Project
git clone https://github.com/Azo15/Pharma-Record-Linkage.git
cd Pharma-Record-Linkage
jupyter notebook record_linkage_project.ipynb

---

## 👤 Author
**Azo İsmail**  
*Software Engineering Student @ Kırklareli University*  
* GitHub: [@Azo15](https://github.com/Azo15)
