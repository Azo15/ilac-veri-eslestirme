import nbformat as nbf

nb = nbf.v4.new_notebook()

text_1 = """# Veri Madenciliği Projesi: İlaç Veri Setleri Eşleştirme (Record Linkage)
**Proje Amacı:** TİTCK ve ATC ilaç listelerindeki ilaçları metin madenciliği ve Bulanık Eşleştirme (Fuzzy Matching) yöntemleriyle eşleştirmek.

Ödev kriterlerine uygun olarak, eşleştirme işleminde sadece 'İlaç Adı' değil, 'Etkin Madde' (ATC Adı) ve 'Firma' bilgileri de normalize edilip birleştirilerek tam eşleştirme sağlanmıştır."""

code_1 = """import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')"""

text_2 = """## 1. Verilerin Yüklenmesi
TİTCK ve ATC verilerini okuyoruz."""

code_2 = """df_titck = pd.read_csv('titck_liste_18.04.csv', sep=',')
print(f"TİTCK Satır Sayısı: {len(df_titck)}")
display(df_titck.head(2))

df_atc = pd.read_excel('ATC_14_04.xlsx')
print(f"ATC Satır Sayısı: {len(df_atc)}")
display(df_atc.head(2))"""

text_3 = """## 2. Veri Temizleme ve Normalleştirme (Pre-processing)
Ödev kriterlerine göre 'İlaç Adı', 'Etkin Madde' ve 'Firma' isimlerindeki dil ve yazım farklılıklarını gidermek için özel bir normalizasyon fonksiyonu tanımlıyoruz.
Özellikle Etkin Madde kısmındaki Türkçe/İngilizce farklılıklarını (örn: parasetamol vs paracetamol) tolere edebilmek için tüm metinleri standardize edip tek bir metin havuzunda (Combined_Text) birleştiriyoruz."""

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
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# TİTCK Sütunlarını Temizleme ve Birleştirme
df_titck['Ilac_Adi_Clean'] = df_titck['Ilac_Adi'].apply(clean_text)
df_titck['Etkin_Madde_Clean'] = df_titck['Etkin_Madde'].apply(clean_text)
df_titck['Firma_Clean'] = df_titck['Firma'].apply(clean_text)

# Tüm kritik bilgileri tek bir metinde birleştiriyoruz
df_titck['Combined_Text'] = df_titck['Ilac_Adi_Clean'] + " " + df_titck['Etkin_Madde_Clean'] + " " + df_titck['Firma_Clean']

# ATC Sütunlarını Temizleme ve Birleştirme (ATC Adı = Etkin Madde)
df_atc['Ilac_Adi_Clean'] = df_atc['İlaç Adı'].apply(clean_text)
df_atc['ATC_Adi_Clean'] = df_atc['ATC Adı'].apply(clean_text)
df_atc['Firma_Adi_Clean'] = df_atc['Firma Adı'].apply(clean_text)

df_atc['Combined_Text'] = df_atc['Ilac_Adi_Clean'] + " " + df_atc['ATC_Adi_Clean'] + " " + df_atc['Firma_Adi_Clean']

print("Veri temizleme, etkin madde normalizasyonu ve birleştirme tamamlandı.")"""

text_4 = """## 3. TF-IDF ve Cosine Similarity ile Bulanık Eşleştirme (Fuzzy Matching)
Levenshtein yerine 15.000 x 17.000 satırda çok daha hızlı ve başarılı olan TF-IDF harf grupları (n-gram) + Kosinüs Benzerliği kullanıyoruz. 
Bu yöntem paracetamol/parasetamol gibi farklılıkları harf gruplarındaki yüksek örtüşme sayesinde yakalar."""

code_4 = """# n-gram_range=(2, 4) ile kelimeleri 2, 3 ve 4 harfli parçalara bölüyoruz. (Örn: 'para', 'aras', 'rase' vb.)
vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4))

atc_combined_texts = df_atc['Combined_Text'].tolist()
tfidf_matrix_atc = vectorizer.fit_transform(atc_combined_texts)

titck_combined_texts = df_titck['Combined_Text'].tolist()
tfidf_matrix_titck = vectorizer.transform(titck_combined_texts)

print("Matrisler oluşturuldu. Eşleştirmeler hesaplanıyor...")

batch_size = 1000
best_matches = []

for i in range(0, tfidf_matrix_titck.shape[0], batch_size):
    end_idx = min(i + batch_size, tfidf_matrix_titck.shape[0])
    cosine_sim_batch = cosine_similarity(tfidf_matrix_titck[i:end_idx], tfidf_matrix_atc)
    
    best_scores = np.max(cosine_sim_batch, axis=1)
    best_indices = np.argmax(cosine_sim_batch, axis=1)
    
    for score, idx in zip(best_scores, best_indices):
        best_matches.append({'best_match_idx': idx, 'match_score': score})
        
print("Hesaplama tamamlandı!")"""

text_5 = """## 4. Sonuç Tablosu (Ödev Teslim Formatı)
Ödevde istenen `TITCK_ID`, `TITCK_Ilac_Adi`, `ATC_Barkod`, `ATC_Kodu`, `ATC_Durumu`, `Match Score` kolonlarından oluşan nihai tabloyu hazırlıyoruz."""

code_5 = """THRESHOLD = 0.70 # İlaç adı, firma ve etkin madde 3'lü birleştiği için threshold'u %70'e esnetiyoruz.

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
            'Match Score': round(score * 100, 2)
        })

df_results = pd.DataFrame(results)
print(f"Başarıyla Eşleştirilen Kayıt Sayısı: {len(df_results)}")

df_results.to_csv('eslesmis_veriler.csv', index=False, encoding='utf-8-sig')
print("\\n'eslesmis_veriler.csv' başarıyla kaydedildi.")
display(df_results.head(10))"""

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
