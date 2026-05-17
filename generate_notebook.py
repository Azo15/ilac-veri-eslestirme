import nbformat as nbf

nb = nbf.v4.new_notebook()

text_1 = """# Veri Madenciliği Projesi: İlaç Veri Setleri Eşleştirme (Record Linkage)
**Proje Amacı:** TİTCK ve ATC ilaç listelerindeki ilaçları metin madenciliği ve Bulanık Eşleştirme (Fuzzy Matching) yöntemleriyle eşleştirmek.

Bu projede HIZ ve DOĞRULUK sağlamak için **TF-IDF Vektörizasyonu** ve **Kosinüs Benzerliği (Cosine Similarity)** algoritması kullanılmıştır."""

code_1 = """import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')"""

text_2 = """## 1. Verilerin Yüklenmesi
TİTCK ve ATC verilerini okuyoruz."""

code_2 = """# TİTCK verisini virgül ayracıyla okuyoruz (ParserError'u önlemek için sep=',')
df_titck = pd.read_csv('titck_liste_18.04.csv', sep=',')
print(f"TİTCK Satır Sayısı: {len(df_titck)}")
display(df_titck.head(3))

# ATC Excel dosyasını okuyoruz
df_atc = pd.read_excel('ATC_14_04.xlsx')
print(f"ATC Satır Sayısı: {len(df_atc)}")
display(df_atc.head(3))"""

text_3 = """## 2. Veri Temizleme ve Normalleştirme (Pre-processing)
İki listedeki isimleri standart bir hale getirmek için Türkçe karakterleri dönüştüren, noktalama işaretlerini silen ve metni küçülten bir temizleme fonksiyonu tanımlıyoruz."""

code_3 = """def clean_text(text):
    if pd.isna(text):
        return ""
    
    text = str(text).lower()
    
    # Türkçe karakter dönüşümü
    char_map = {'ı': 'i', 'i': 'i', 'ş': 's', 'ğ': 'g', 'ü': 'u', 'ö': 'o', 'ç': 'c', 'â': 'a'}
    for turk_char, eng_char in char_map.items():
        text = text.replace(turk_char, eng_char)
        
    # Sadece harf ve rakamları bırak, noktalama işaretlerini sil
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    
    # Birden fazla boşluğu tek boşluğa düşür ve kenar boşluklarını temizle
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Temizlenmiş sütunları oluşturuyoruz
df_titck['Ilac_Adi_Clean'] = df_titck['Ilac_Adi'].apply(clean_text)
df_atc['Ilac_Adi_Clean'] = df_atc['İlaç Adı'].apply(clean_text)

print("Temizleme işlemi tamamlandı.")"""

text_4 = """## 3. TF-IDF ve Cosine Similarity ile Eşleştirme (Fuzzy Matching)
ATC listesindeki ilaç isimleri üzerinden bir "Kelime Uzayı" (TF-IDF Matrisi) oluşturup, TİTCK listesindeki her bir ilaç için bu uzaydaki en benzer ATC ilacını Kosinüs Benzerliği ile bulacağız."""

code_4 = """# N-gram tabanlı (harf grupları) TF-IDF Vektörizatörü
# analyzer='char_wb', ngram_range=(2, 4) kelime bazlı değil, hece/harf grubu bazlı eşleşme sağlar (yazım hatalarına çok dayanıklıdır).
vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4))

# ATC listesi bizim referans (arama yapacağımız) uzayımız
atc_clean_names = df_atc['Ilac_Adi_Clean'].tolist()
tfidf_matrix_atc = vectorizer.fit_transform(atc_clean_names)

# TİTCK listesindeki isimleri aynı uzaya dönüştürüyoruz
titck_clean_names = df_titck['Ilac_Adi_Clean'].tolist()
tfidf_matrix_titck = vectorizer.transform(titck_clean_names)

print("TF-IDF matrisleri oluşturuldu. Benzerlik hesaplaması başlatılıyor...")

# Belleği yormamak için batch'ler halinde Kosinüs Benzerliği hesaplıyoruz
batch_size = 1000
best_matches = []

for i in range(0, tfidf_matrix_titck.shape[0], batch_size):
    end_idx = min(i + batch_size, tfidf_matrix_titck.shape[0])
    
    # Batch içindeki TİTCK isimlerinin, tüm ATC matrisi ile benzerliği
    cosine_sim_batch = cosine_similarity(tfidf_matrix_titck[i:end_idx], tfidf_matrix_atc)
    
    # Her satır için en yüksek benzerlik skorunu ve indeksini alıyoruz
    best_scores = np.max(cosine_sim_batch, axis=1)
    best_indices = np.argmax(cosine_sim_batch, axis=1)
    
    for score, idx in zip(best_scores, best_indices):
        best_matches.append({
            'best_match_idx': idx,
            'match_score': score
        })
        
print("Eşleştirme hesaplaması tamamlandı!")"""

text_5 = """## 4. Sonuç Tablosunun Oluşturulması ve Dışa Aktarma
Belirlediğimiz eşleşme oranının (Örn: %80) üzerindeki kayıtları kabul edeceğiz.
Ödevin istediği kolonlar: `TITCK_ID`, `TITCK_Ilac_Adi`, `ATC_Barkod`, `ATC_Kodu`, `ATC_Durumu`, `Match Score`"""

code_5 = """# MATCH SCORE THRESHOLD (Benzerlik Sınırı)
THRESHOLD = 0.80

results = []

for idx_titck, match_info in enumerate(best_matches):
    score = match_info['match_score']
    idx_atc = match_info['best_match_idx']
    
    if score >= THRESHOLD:
        row_titck = df_titck.iloc[idx_titck]
        row_atc = df_atc.iloc[idx_atc]
        
        results.append({
            'TITCK_ID': row_titck['ID'],
            'TITCK_Ilac_Adi': row_titck['Ilac_Adi'],
            'ATC_Barkod': row_atc['Barkod'],
            'ATC_Kodu': row_atc['ATC Kodu'],
            'ATC_Durumu': row_atc['Durumu'],
            'Match Score': round(score * 100, 2)  # Yüzdelik cinsten
        })

df_results = pd.DataFrame(results)

print(f"Toplam TİTCK Kaydı: {len(df_titck)}")
print(f"Başarıyla Eşleştirilen Kayıt Sayısı (Score >= {THRESHOLD*100}%): {len(df_results)}")

# Sonuçları göster
display(df_results.head(10))

# Nihai CSV dosyasına kaydet
df_results.to_csv('eslesmis_veriler.csv', index=False, encoding='utf-8-sig')
print("\\n'eslesmis_veriler.csv' dosyası başarıyla kaydedildi.")"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text_1),
    nbf.v4.new_code_cell(code_1),
    nbf.v4.new_markdown_cell(text_2),
    nbf.v4.new_code_cell(code_2),
    nbf.v4.new_markdown_cell(text_3),
    nbf.v4.new_code_cell(code_3),
    nbf.v4.new_markdown_cell(text_4),
    nbf.v4.new_code_cell(code_4),
    nbf.v4.new_markdown_cell(text_5),
    nbf.v4.new_code_cell(code_5)
]

with open('record_linkage_project.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
