# İlaç Veri Setleri Arasında Kayıt Eşleştirme ve Veri Normalleştirme Proje Raporu

**Öğrenci Adı Soyadı:** [Adınızı Soyadınızı Yazın]
**Öğrenci Numarası:** [Öğrenci Numaranızı Yazın]
**Ders:** Veri Madenciliği

## 1. Projenin Amacı
Bu projenin temel amacı, farklı kaynaklardan elde edilen ve ortak bir anahtarı bulunmayan (TİTCK ve ATC) iki farklı ilaç veri setini metin madenciliği teknikleri kullanarak eşleştirmektir. Eşleştirme işlemi sadece "İlaç Adı" ile sınırlı bırakılmamış; doğruluk payını artırmak ve dil farklılıklarını tolere etmek adına "Etkin Madde" ve "Firma" bilgileri de analize dahil edilmiştir.

## 2. Veri Temizleme ve Normalleştirme Adımları
Farklı kurumlardan gelen listelerde oluşabilecek yazım hatalarını ve format farklılıklarını gidermek için şu ön işlem (pre-processing) adımları uygulanmıştır:
- **Karakter Dönüşümü:** Veri setlerinde bulunan Türkçe karakterler (ı, ş, ğ, ü, ö, ç, vb.) İngilizce karşılıklarına (i, s, g, u, o, c) dönüştürülmüştür.
- **Büyük/Küçük Harf Standardizasyonu:** Tüm metinler küçük harfe çevrilmiştir.
- **Gereksiz Karakter Temizliği:** Tire (-), yüzde (%), parantez () gibi noktalama işaretleri ile fazladan bırakılan boşluklar Regular Expression (RegEx) yöntemleri ile temizlenerek sadeleştirilmiş metinler elde edilmiştir.
- **Kombinasyon:** TİTCK verisindeki `İlaç Adı` + `Etkin Madde` + `Firma` bilgileri tek bir havuzda birleştirilmiştir. Aynı işlem ATC tarafında da yapılmış; İngilizce/Latince adlandırmayı temsil eden `ATC Adı` bilgisi, etkin madde olarak kabul edilip `İlaç Adı` ve `Firma Adı` ile birleştirilerek ortak bir referans metin uzayı (Combined Text) oluşturulmuştur.

## 3. Eşleştirme Algoritması ve Uygulanan Yöntemler
Eşleştirme işlemi için satır satır arama yapmak (örneğin salt Levenshtein kullanmak) 15.000 ve 17.000 satırlık matrislerde hem çok maliyetli hem de uzun süreceği için çok daha hızlı ve güvenilir olan **TF-IDF ve Kosinüs Benzerliği (Cosine Similarity)** algoritması tercih edilmiştir.

- **TF-IDF ile Karakter N-Gram Yaklaşımı:** İlaç ve etkin madde isimlerindeki *parasetamol / paracetamol* veya *kapsül / caps* gibi dil farklılıklarından kaynaklı uyuşmazlıkları aşmak için metinler doğrudan kelime kelime değil, **2 ila 4 harfli hece gruplarına (character n-grams)** bölünerek TF-IDF matrisine aktarılmıştır. Bu sayede yazım hataları veya varyasyonlar yüksek oranda tolere edilmiştir.
- **Kosinüs Benzerliği (Cosine Similarity):** TİTCK listesindeki her bir kombine metin, oluşturulan ATC TF-IDF matrisi üzerinde taranmış ve en yüksek benzerliği gösteren (vektörel olarak birbirine en yakın) kayıtlar bulunmuştur.

## 4. Sonuç ve Teslim Edilen Çıktılar
Yapılan analiz sonucunda Kosinüs Benzerliği skoru **%70 ve üzerinde** olan kayıtlar başarılı eşleşme (Exact/Fuzzy Match) olarak kabul edilmiştir. (İlaç, firma ve madde birleşimi sonucu oluşan uzun metinlerde %70 eşik değeri optimum başarıyı sağlamıştır).

Elde edilen sonuçlar; `TITCK_ID`, `TITCK_Ilac_Adi`, `ATC_Barkod`, `ATC_Kodu`, `ATC_Durumu` ve `Match Score` kolonlarını içerecek şekilde filtrelenerek **eslesmis_veriler.csv** adlı dosyaya aktarılmıştır. Kodların tamamı projeye ait Jupyter Notebook dosyasında mevcuttur.
