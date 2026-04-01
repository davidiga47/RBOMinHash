RBOMinHash

RBOMinHash is an LSH scheme with distortion for the Rank-Biased Overlap (RBO) similarity
The class, in the rbo_min_hash.py file, consists in the following methods:
	
	-get_ranking_hash(r): computes the hash of ranking r
	-get_rbo_similarity(r1,r2): estimates the RBO similarity between rankings r1 and r2 using their hashes
	-get_rbo_similarity_by_index(i1,i2): estimates the RBO similarity between the rankings with indexes i1 and i2 in the scheme
	-add_ranking(r): adds the hash of the ranking r to the scheme
	-nearest_neighbors(q,k): computes the k nearest neighbors in the scheme for query ranking q
	-most_similar(q,t): computes the rankings in the scheme with estimated RBO over threshold t wrt query ranking q