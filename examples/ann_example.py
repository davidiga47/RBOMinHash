
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
        perm_len: Length of the permutation r used during hashing
        num_hashes: Number of different hash functions used to hash a ranking
        num_neighbors: Number of neighbors to compute for the query
        query: File containing the query ranking
        skip_query_file: If true skips the query file while computing neighbors
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
    
    rankings=ut.load_rankings(directory)           #List of the rankings
    
    #LSH scheme creation
    matrix=rmh.RBOMinHash(params["p"], params["perm_len"], 
                          params["num_hashes"])  
    
    signatures=dict()   #Key:filename, Value:hashes
    translator=dict()   #Dict used to encode strings
    
    # Start counting building time for experiments
    start_building = time.perf_counter()  

    #Computation of the hashes
    for file in rankings.keys():
        ranking=rankings[file]
        file_int = all(isinstance(x, int) for x in ranking)
        if not file_int:    #Then it needs to be encoded
            ranking=ut.encode_ranking(ranking,translator)
        signatures[file] = matrix.copy()    #Create new instance of the scheme
        signatures[file].update(ranking)    #Inserts the ranking, so to hash it
    
    end_building = time.perf_counter()
    build_time = end_building - start_building
    
    distances=dict()    #For each file, p. of collision with query file
    ratios=dict()       #For each file, ratio p. of collision/actual RBO sim.
    
    #Computation of p. of hash collision between query and each other file
    for file in signatures.keys():
        if params["skip_query_file"] and file==params["query"]:
            continue
        distances[file]=signatures[params["query"]].rbo(signatures[file])
        ratios[file]=distances[file]   #Later it will compute RBO and the ratio
    res=ut.top_keys(distances, params["num_neighbors"])
    
    #Same as before with actual RBO similarity
    actual_distances=dict()     
    for file in signatures.keys():
        if params["skip_query_file"] and file==params["query"]:
            continue
        actual_distances[file]=rmh.rbo_sim(
            ut.encode_ranking(rankings[file],translator), 
            ut.encode_ranking(rankings[params["query"]],translator), 
            p=params["p"])
        ratios[file]/=actual_distances[file]
    actual_res=ut.top_keys(actual_distances, params["num_neighbors"])
    
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
    
    return (precision, recall, avg_ratio, build_time, elapsed_time, mem_use, 
            res, actual_res, distances, actual_distances)

def eg1():   
    
    print("\n")
    
    ann_exp=ann()
    
    #Fetching of the results
    precision=ann_exp[0]
    recall=ann_exp[1]
    avg_ratio=ann_exp[2]
    build_time=ann_exp[3]
    elapsed_time=ann_exp[4]
    mem_use=ann_exp[5]
    res=ann_exp[6]
    actual_res=ann_exp[7]
    distances=ann_exp[8]
    actual_distances=ann_exp[9]
    
    
    #Fetching of the parameters
    with open("ann_parameters.json", "r") as file:
        params = json.load(file)
    
    #Print of the results
    print(f"QUERY FILE: {params['query']}")
    print("PARAMETERS:\n")
    print(f"Persistence: {params['p']}\nLength of permutation: {params['perm_len']}\nNumber of values in the hash: {params['num_hashes']}")
    
    print(f"\nAPPROXIMATE NEAREST {params['num_neighbors']} NEIGHBORS FOR {params['query']}:\n")
    for i in range(params['num_neighbors']):
        print(f"{i+1}: {res[i]} | DISTANCE: {distances[res[i]]}")
        
    print(f"\nNEAREST {params['num_neighbors']} NEIGHBORS FOR {params['query']}:\n")
    for i in range(params['num_neighbors']):
        print(f"{i+1}: {actual_res[i]} | DISTANCE: {actual_distances[actual_res[i]]}")
    
    print(f"\nPRECISION: {precision}")    
    print(f"RECALL: {recall}")
    print(f"AVERAGE RATIO P.COLLISION/RBO: {avg_ratio}")
    print(f"\nBUILDING TIME OF THE LSH SCHEMES: {build_time:.6f} seconds")
    print(f"TOTAL ELAPSED TIME: {elapsed_time:.6f} seconds")
    print(f"MEMORY UTILIZATION: {mem_use:.2f} MB")
    
    print("\n")
    
    
if __name__=="__main__":
    eg1()
    
