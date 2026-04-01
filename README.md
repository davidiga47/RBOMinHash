# RBOMinHash

**RBOMinHash** is a *Locality-Sensitive Hashing (LSH)* scheme with distortion for the **Rank-Biased Overlap (RBO)** similarity.

---

The scheme is implemented as a Python class in the rbo_min_hash.py file, and consists in the following methods:

### `get_ranking_hash(r)`
Computes the hash of ranking `r`.

### `get_rbo_similarity(r1, r2)`
Estimates the **RBO** similarity between rankings `r1` and `r2` using their hashes.

### `get_rbo_similarity_by_index(i1, i2)`
Estimates the **RBO** similarity between the rankings of the scheme having indexes `i1` and `i2`.

### `add_ranking(r)`
Adds ranking `r` to the scheme with its hash.

### `nearest_neighbors(q, k)`
Computes the `k` nearest neighbors in the scheme for query ranking `q`.

### `most_similar(q, t)`
Returns all the rankings in the scheme having estimated RBO similarity **over threshold `t`** wrt query ranking `q`.

---

## Use example

```python
from rbo_min_hash import RBOMinHash

lsh = RBOMinHash()

lsh.add_ranking(r1)
lsh.add_ranking(r2)

sim = lsh.get_rbo_similarity(r1, r2)
neighbors = lsh.nearest_neighbors(q, 5)

For more detailed examples see the `examples` subdirectory
[Click here for more informations about RBO](https://dl.acm.org/doi/abs/10.1145/1852102.1852106)
[Click here for more informations about LSH](https://en.wikipedia.org/wiki/Locality-sensitive_hashing)
