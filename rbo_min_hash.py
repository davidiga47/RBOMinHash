import numpy as np 
from mpmath import nsum, inf

class RBO_LSH:
    def __init__(self, p, num_hashes, seed):
        assert 0 < p < 1 and num_hashes > 0

        #random generator for reproducibility
        self.rand_gen = np.random.default_rng(seed)

        # extract num_hashes functions from the LSH scheme (these are parametrized by d and r)
        self.d = list(self.rand_gen.geometric(1 - p, size=num_hashes))
        self.r = [{} for _ in range(num_hashes)]
        self.num_hashes = num_hashes

        # List of hashed ranking
        # Specifically, ranking_dataset[i] contains a list of self.num_hashes numbers corresponding to one value for each function extracted from the LSH
        self.ranking_dataset = [] 
        
        
    def get_ranking_hash(self, ranking):
        # we assume ranking is a list of hashable values (e.g., integers)
        hashed_ranking = []
        for hash_iter in range(self.num_hashes):
            min_val = None
            
            for i in range(min(len(ranking), self.d[hash_iter])):
                if ranking[i] not in self.r[hash_iter]:
                    #should we generate a random integer within a very large range? like [1, (1/(1-p))**2] or larger
                    #this would help numerical stability
                    self.r[hash_iter][ranking[i]] = self.rand_gen.random() 
                if min_val is None or self.r[hash_iter][ranking[i]] < min_val:
                    min_val = self.r[hash_iter][ranking[i]]
                
            #NOTE: if the ranking is smaller than d, we are stopping earlier. This is slightly different than the theoretical algorithm
            #Not sure if we want to make this closer to theory, or whether this variant is reasonable in practice
            
            hashed_ranking.append(min_val)

        #Note: we might store this as a numpy array rather than a Python list and we can compute distances more efficiently
        return hashed_ranking

    def get_rbo_similarity(self, h1, h2):
        #returns rbo similarity given hashes h1 and h2 for two rankings
        
        #Note: implementing h1 and h2 as numpy array would simplify this and make it faster
        assert len(h1) == len(h2)

        k = len(h1)
        cumulative = 0
        for i in range(k):
            if h1[i] == h2[i]: #these are values in (0,1), should we do something like abs(h1[i] - h2[i]) < eps? (say, with eps=0.00001) --- I think this would be more numerically stable
                cumulative += 1
        return cumulative / k
    
    def get_rbo_similarity_by_index(self, i1, i2):
        #returns rbo similarity given hashes h1 and h2 for two rankings
        
        h1=self.ranking_dataset[i1]
        h2=self.ranking_dataset[i2]
        
        #Note: implementing h1 and h2 as numpy array would simplify this and make it faster
        assert len(h1) == len(h2)

        k = len(h1)
        cumulative = 0
        for i in range(k):
            if h1[i] == h2[i]: #these are values in (0,1), should we do something like abs(h1[i] - h2[i]) < eps? (say, with eps=0.00001) --- I think this would be more numerically stable
                cumulative += 1
        return cumulative / k

    def add_ranking(self, ranking):
        hashed_ranking = self.get_ranking_hash(ranking)
        self.ranking_dataset.append(hashed_ranking)

    def nearest_neighbors(self, query, k):
        #returns (approximately) k-closest rankings to the query

        #TODO: make this function faster!

        hash_query = self.get_ranking_hash(query)
        similarity_idx_pair = []
        for i, hash_ranking in enumerate(self.ranking_dataset): #linear scan for testing purposes
            sim = self.get_rbo_similarity(hash_query, hash_ranking)
            similarity_idx_pair.append( (sim, i) )
        
        return sorted(similarity_idx_pair, reverse=True)[:k]
    

#computes the RBO similarity between lists x and y
def rbo_sim(x, y, p=0.9, k=None):
    if k is None or k>max(len(x), len(y)):
        k = max(len(x), len(y))
    x_set = set()
    y_set = set()
    cumulative = 0.0
    A_d=0
    for d in range(1, k + 1):
        if d <= len(x):
            x_set.add(x[d - 1])
        if d <= len(y):
            y_set.add(y[d - 1])
        overlap = len(x_set.intersection(y_set))
        A_d = overlap / d
        cumulative += (p ** (d - 1)) * A_d
    final_int=A_d*k
    cumulative += float(nsum(lambda d: p**(d-1)*(final_int+d-k)/d, [k+1, inf]))
    return (1 - p) * cumulative

def exact_nearest_neighbor(ranking_datasets, ranking_query, p, k):
    similarity_idx_pair = []
    for i, rd in enumerate(ranking_datasets):
        sim = rbo_sim(rd, ranking_query, p=p)
        similarity_idx_pair.append( (sim, i) )

    return sorted(similarity_idx_pair, reverse=True)[:k]

if __name__ == '__main__':
    # QUICK AND DIRTY TESTING

    # generate some random rankings
    rnd = np.random.default_rng(42)
    num_rankings = 500
    num_queries = 10
    ranking_len = 1000
    p = 0.9
    ranking_dataset = [rnd.permutation(np.arange(ranking_len)).tolist() for _ in range(num_rankings)] #generate random permutation of {1,...,ranking_len} as a ranking
    queries = [rnd.permutation(np.arange(ranking_len)).tolist() for _ in range(num_queries)]

    #build LSH
    num_hashes = 200
    lsh = RBO_LSH(p, num_hashes, 74)
    for ranking in ranking_dataset:
        lsh.add_ranking(ranking)
    
    # evaluate queries:
    k = 3 #top-3

    for i, query in enumerate(queries):
        lsh_response = lsh.nearest_neighbors(query, k)
        exact_response = exact_nearest_neighbor(ranking_dataset, query, p, k)

        print(f'Query #{i}')
        print('LSH response: ', lsh_response)
        print('Exact response: ', exact_response)
        print()
    
    
    # lsh=RBO_LSH(0.9,100,42)
    # lsh.add_ranking([1,2,3,4,5])
    # lsh.add_ranking([1,2,3,4,5])
    # print(lsh.get_rbo_similarity_by_index(0, 1))
    # print(rbo_sim([1,2,3,4,5],[1,2,3,4,5],0.9))
    
    data1=["ciao", "sono", "davide"]
    data2=["ciao", "sono", "davide"]
    print(rbo_sim(data1,data2))