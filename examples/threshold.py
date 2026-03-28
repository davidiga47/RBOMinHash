
import json
from pathlib import Path
import sys
import os
import numpy as np
import time
from pympler import asizeof

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utilities as ut
import rbo_min_hash as rmh

def over_thresh():
    
    start_elapsed = time.perf_counter() 
    
    # Parameters loading
    with open("thresh_parameters.json", "r") as file:
        params = json.load(file)
    directory=Path(params["directory"])
    
    #LSH scheme creation
    loaded=ut.load_rankings(directory)           #List of the rankings
    seed=np.random.randint(1,1001)
    lsh=rmh.RBOMinHash(params["p"], params["num_hashes"], seed)  
    translator=dict()   #Dict used to encode strings
    
    start_building = time.perf_counter()
    
    #Encoding and hashing of the rankings
    rankings=dict()
    hashing_time=0
    for file in loaded.keys():
        rank=loaded[file]
        rank_int = all(isinstance(x, int) for x in rank)
        if not rank_int:
            rank=ut.encode_ranking(rank, translator)
        rankings[file]=rank
        start_hashing=time.perf_counter()
        lsh.add_ranking(rank)
        end_hashing=time.perf_counter()
        hashing_time += (end_hashing - start_hashing)

    #Isolation of the query ranking
    for i,k in enumerate(rankings.keys()):
        if k == params['query']:
            query = rankings[k]
            query_index = i
            break
        
    end_building = time.perf_counter()
    build_time = end_building - start_building
    start_querying=time.perf_counter()
        
    similar=lsh.most_similar(query, params['threshold'])
    end_querying=time.perf_counter()
    query_time_lsh=end_querying-start_querying
    res=[]
    for elm in similar:
        if elm[1]==query_index:
            continue
        for i,file in enumerate(rankings.keys()):
            if i == elm[1]:
                res.append(file)
                break
    
    mem_use = asizeof.asizeof(lsh)
    
    start_querying=time.perf_counter()
    #Computation of k nearest neighbors using RBO
    actual_similar=rmh.exact_most_similar(list(rankings.values()), query,
                                        params['p'], params['threshold'])
    end_querying=time.perf_counter()
    query_time_rbo=end_querying-start_querying
    actual_res=[]
    for elm in actual_similar:
        if elm[1]==query_index:
            continue
        for i,file in enumerate(rankings.keys()):
            if i == elm[1]:
                actual_res.append(file)
                break
    try:
        recall=len(set(res) & set(actual_res))/len(set(res) | set(actual_res))
    except ZeroDivisionError:
        recall=0
    
    ratios=dict()           
    lsh.add_ranking(query)
    for i,file in enumerate(rankings.keys()):
        ratios[file]=lsh.get_rbo_similarity_by_index(i, -1)
        ratios[file]/=rmh.rbo_sim(query, rankings[file], p=params['p'])

    avg_ratio=np.mean(np.array(list(ratios.values())))
    
    end_elapsed = time.perf_counter()
    elapsed_time = end_elapsed - start_elapsed
    
    return (recall,
            avg_ratio,
            build_time,
            elapsed_time,
            query_time_lsh,
            query_time_rbo,
            hashing_time,
            mem_use, 
            res,
            actual_res
            )

def eg3():   
    
    print("\n")
    
    similar_exp=over_thresh()
    
    #Fetching of the results
    recall=similar_exp[0]
    avg_ratio=similar_exp[1]
    build_time=similar_exp[2]
    elapsed_time=similar_exp[3]
    query_time_lsh=similar_exp[4]
    query_time_rbo=similar_exp[5]
    hashing_time=similar_exp[6]
    mem_use=similar_exp[7]
    res=similar_exp[8]
    actual_res=similar_exp[9]
    
    
    #Fetching of the parameters
    with open("thresh_parameters.json", "r") as file:
        params = json.load(file)
    
    #Print of the results
    print(f"QUERY FILE: {params['query']}")
    print("\nPARAMETERS:\n")
    print(f"Persistence: {params['p']}\nNumber of values in the hash: {params['num_hashes']}")
    
    print(f"\nFILES WITH APPROXIMATE SIMILARITY OVER {params['threshold']}:\n")
    for i in range(len(res)):
        print(f"{i+1}: {res[i]}")
    if not res:
        print("--No files--")
        # print(f"{i+1}: {res[i]} | DISTANCE: {distances[res[i]]}")
        
    print(f"\nFILES WITH EXACT RBO SIMILARITY OVER {params['threshold']}:\n")
    for i in range(len(actual_res)):
        print(f"{i+1}: {actual_res[i]}")
        # print(f"{i+1}: {actual_res[i]} | DISTANCE: {actual_distances[actual_res[i]]}")
    if not actual_res:
        print("--No files--")
     
    print(f"\nRECALL: {recall}")
    print(f"AVERAGE RATIO P.COLLISION/RBO: {avg_ratio}")
    print(f"\nBUILDING TIME OF THE LSH SCHEME: {build_time:.6f} seconds")
    print(f"HASHING TIME: {hashing_time:.6f} seconds")
    print(f"QUERY TIME FOR THE LSH SCHEME: {query_time_lsh:.6f} seconds")
    print(f"QUERY TIME FOR THE ACTUAL RBO: {query_time_rbo:.6f} seconds")
    print(f"TOTAL ELAPSED TIME: {elapsed_time:.6f} seconds")
    print(f"\nMEMORY USED BY THE LSH SCHEME: {(mem_use/1024):.2f} KB")
    
    print("\n")
    
    
if __name__=="__main__":
    eg3()
    
