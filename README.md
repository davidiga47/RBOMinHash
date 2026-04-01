# 📊 RBOMinHash

**RBOMinHash** è uno schema di *Locality-Sensitive Hashing (LSH)* con distorsione progettato per la similarità **Rank-Biased Overlap (RBO)** tra ranking.

---

## 📁 Struttura

L'implementazione principale si trova nel file rbo_min_hash.py



All’interno è definita la classe `RBOMinHash`, che espone i seguenti metodi.

---

## ⚙️ Metodi principali

### 🔹 `get_ranking_hash(r)`
Calcola l’hash del ranking `r`.

---

### 🔹 `get_rbo_similarity(r1, r2)`
Stima la similarità **RBO** tra i ranking `r1` e `r2` utilizzando i loro hash.

---

### 🔹 `get_rbo_similarity_by_index(i1, i2)`
Stima la similarità **RBO** tra due ranking già presenti nello schema, identificati dagli indici `i1` e `i2`.

---

### 🔹 `add_ranking(r)`
Aggiunge il ranking `r` allo schema calcolandone e memorizzandone l’hash.

---

### 🔹 `nearest_neighbors(q, k)`
Restituisce i `k` ranking più simili (nearest neighbors) rispetto al ranking di query `q`.

---

### 🔹 `most_similar(q, t)`
Restituisce tutti i ranking nello schema con similarità RBO stimata **maggiore di una soglia `t`** rispetto al ranking `q`.

---

## 🚀 Uso tipico

```python
from rbo_min_hash import RBOMinHash

rbomh = RBOMinHash()

rbomh.add_ranking(r1)
rbomh.add_ranking(r2)

sim = rbomh.get_rbo_similarity(r1, r2)
neighbors = rbomh.nearest_neighbors(q, k=5)