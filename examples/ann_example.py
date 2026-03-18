
import json
from pathlib import Path
import numpy as np
import sys
import os
import time
import psutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utilities as ut
import rbo_min_hash as rmh

def ann():
    """This example loads a directory containing rankings, then selects a query
    ranking and computes its k nearest neighbors according to the probability
    of hash collisions with the loaded files, using the LSH scheme RBOMinHash 
    to perform the hashing.
    
    PARAMETERS:
        p: User's persistence
        num_hashes: Number of different hash functions used to hash a ranking
        num_neighbors: Number of neighbors to compute for the query
        query: File containing the query ranking
        directory: The directory from which to load the rankings

    """
    #Get the Pid to later compute the memory utilization
    process = psutil.Process(os.getpid())
    
    # Start counting elapsed time for experiments
    start_elapsed = time.perf_counter() 
    
    # Parameters loading
    with open("ann_parameters.json", "r") as file:
        params = json.load(file)
    directory=Path(params["directory"])
    loaded=ut.load_rankings(directory)           #List of the rankings
    
    #LSH scheme creation
    lsh=rmh.RBO_LSH(params["p"], params["num_hashes"], params['seed'])  
    translator=dict()   #Dict used to encode strings
    
    # Start counting building time for experiments
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
    query=rankings[params['query']]
    query_index=params['query'].replace("file","")
    query_index=int(query_index.replace(".txt",""))
         
    end_building = time.perf_counter()
    build_time = end_building - start_building
    start_querying=time.perf_counter()
    
    #Computation of k nearest neighbors using LSH
    neighbors=lsh.nearest_neighbors(query, params['num_neighbors']+1)
    end_querying=time.perf_counter()
    query_time_lsh=end_querying-start_querying
    res=[]
    for elm in neighbors:
        if elm[1]==query_index:
            continue
        for i,file in enumerate(rankings.keys()):
            if i == elm[1]:
                res.append(file)
                break
    
    #Computation of k nearest neighbors using RBO
    start_querying=time.perf_counter()
    actual_neighbors=rmh.exact_nearest_neighbor(list(rankings.values()), query,
                                        params['p'], params['num_neighbors']+1)
    end_querying=time.perf_counter()
    query_time_rbo=end_querying-start_querying
    actual_res=[]
    for elm in actual_neighbors:
        if elm[1]==query_index:
            continue
        for i,file in enumerate(rankings.keys()):
            if i == elm[1]:
                actual_res.append(file)
                break
    
    distances=dict()        #For each file, p. of collision with query file
    actual_distances=dict() #For each file, RBO similarity with query file     
    ratios=dict()           #For each file, ratio p. of collision/actual RBO sim.
    lsh.add_ranking(query)
    for i,file in enumerate(rankings.keys()):
        distances[file]=lsh.get_rbo_similarity_by_index(i, -1)
        actual_distances[file]=rmh.rbo_sim(query, rankings[file], p=params['p'])
        ratios[file]=distances[file]/actual_distances[file]
    
    #Metrics 
    precision=0
    for i in range(params['num_neighbors']):
        if res[i]==actual_res[i]:
            precision+=1
    precision/=params["num_neighbors"]
    recall=len(set(res) & set(actual_res))/params['num_neighbors']
    avg_ratio=np.mean(np.array(list(ratios.values())))
    
    end_elapsed = time.perf_counter()
    elapsed_time = end_elapsed - start_elapsed
    mem_use=process.memory_info().rss / 1024**2
    
    return (precision, 
            recall,
            avg_ratio,
            build_time,
            elapsed_time,
            query_time_lsh,
            query_time_rbo,
            hashing_time,
            mem_use, 
            res,
            actual_res,
            distances,
            actual_distances)

def eg1():   
    
    print("\n")
    
    ann_exp=ann()
    
    #Fetching of the results
    precision=ann_exp[0]
    recall=ann_exp[1]
    avg_ratio=ann_exp[2]
    build_time=ann_exp[3]
    elapsed_time=ann_exp[4]
    query_time_lsh=ann_exp[5]
    query_time_rbo=ann_exp[6]
    hashing_time=ann_exp[7]
    mem_use=ann_exp[8]
    res=ann_exp[9]
    actual_res=ann_exp[10]
    distances=ann_exp[11]
    actual_distances=ann_exp[12]
    
    
    #Fetching of the parameters
    with open("ann_parameters.json", "r") as file:
        params = json.load(file)
    
    #Print of the results
    print(f"QUERY FILE: {params['query']}")
    print("PARAMETERS:\n")
    print(f"Persistence: {params['p']}\nNumber of values in the hash: {params['num_hashes']}")
    
    print(f"\nAPPROXIMATE NEAREST {params['num_neighbors']} NEIGHBORS FOR {params['query']}:\n")
    for i in range(params['num_neighbors']):
        print(f"{i+1}: {res[i]} | DISTANCE: {distances[res[i]]}")
        
    print(f"\nNEAREST {params['num_neighbors']} NEIGHBORS FOR {params['query']}:\n")
    for i in range(params['num_neighbors']):
        print(f"{i+1}: {actual_res[i]} | DISTANCE: {actual_distances[actual_res[i]]}")
    
    print(f"\nPRECISION: {precision}")    
    print(f"RECALL: {recall}")
    print(f"AVERAGE RATIO P.COLLISION/RBO: {avg_ratio}")
    print(f"\nBUILDING TIME OF THE LSH SCHEME: {build_time:.6f} seconds")
    print(f"HASHING TIME: {hashing_time:.6f} seconds")
    print(f"QUERY TIME FOR THE LSH SCHEME: {query_time_lsh:.6f} seconds")
    print(f"QUERY TIME FOR THE ACTUAL RBO: {query_time_rbo:.6f} seconds")
    print(f"TOTAL ELAPSED TIME: {elapsed_time:.6f} seconds")
    print(f"\nMEMORY UTILIZATION: {mem_use:.2f} MB")
    
    print("\n")
    
    
if __name__=="__main__":
    eg1()
    
