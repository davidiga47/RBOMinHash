
import json
from pathlib import Path
import sys
import os
import numpy as np

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
    # Parameters loading
    with open("ann_parameters.json", "r") as file:
        params = json.load(file)
    directory=Path(params["directory"])
    
    #LSH scheme creation
    loaded=ut.load_rankings(directory)           #List of the rankings
    seed=np.random.randint(1,1001)
    lsh=rmh.RBOminHash(params["p"], params["num_hashes"], seed)  
    translator=dict()   #Dict used to encode strings
    
    #Encoding and hashing of the rankings
    rankings=dict()
    for file in loaded.keys():
        rank=loaded[file]
        rank_int = all(isinstance(x, int) for x in rank)
        if not rank_int:
            rank=ut.encode_ranking(rank, translator)
        rankings[file]=rank
        lsh.add_ranking(rank)

    #Isolation of the query ranking
    for i,k in enumerate(rankings.keys()):
        if k == params['query']:
            query = rankings[k]
            query_index = i
            break
        
    #Computation of k nearest neighbors using LSH
    neighbors=lsh.nearest_neighbors(query, params['num_neighbors']+1)
    res=[]
    for elm in neighbors:
        if elm[1]==query_index:
            continue
        for i,file in enumerate(rankings.keys()):
            if i == elm[1]:
                res.append(file)
                break
    
    #Computation of k nearest neighbors using RBO
    actual_neighbors=rmh.exact_nearest_neighbor(list(rankings.values()), query,
                                        params['p'], params['num_neighbors']+1)
    actual_res=[]
    for elm in actual_neighbors:
        if elm[1]==query_index:
            continue
        for i,file in enumerate(rankings.keys()):
            if i == elm[1]:
                actual_res.append(file)
                break
    
    #Metrics 
    precision=0
    for i in range(params['num_neighbors']):
        if res[i]==actual_res[i]:
            precision+=1
    precision/=params["num_neighbors"]
    recall=len(set(res) & set(actual_res))/params['num_neighbors']
    
    # distances=dict()        #For each file, p. of collision with query file
    # actual_distances=dict() #For each file, RBO similarity with query file     
    # ratios=dict()           #For each file, ratio p. of collision/actual RBO sim.
    # lsh.add_ranking(query)
    # for i,file in enumerate(rankings.keys()):
    #     distances[file]=lsh.get_rbo_similarity_by_index(i, -1)
    #     actual_distances[file]=rmh.rbo_sim(query, rankings[file], p=params['p'])
    #     ratios[file]=distances[file]/actual_distances[file]
    # avg_ratio=np.mean(np.array(list(ratios.values())))
    
    # return (precision, 
    #         recall,
    #         res,
    #         actual_res,
    #         distances,
    #         actual_distances,
    #         avg_ratio)
    
    return (precision, 
            recall,
            res,
            actual_res)

def eg1():   
    
    print("\n")
    
    ann_exp=ann()
    
    #Fetching of the results
    precision=ann_exp[0]
    recall=ann_exp[1]
    res=ann_exp[2]
    actual_res=ann_exp[3]
    
    
    #Fetching of the parameters
    with open("ann_parameters.json", "r") as file:
        params = json.load(file)
    
    #Print of the results
    print(f"QUERY FILE: {params['query']}")
    print("\nPARAMETERS:\n")
    print(f"Persistence: {params['p']}\nNumber of values in the hash: {params['num_hashes']}")
    
    print(f"\nAPPROXIMATE NEAREST {params['num_neighbors']} NEIGHBORS FOR {params['query']}:\n")
    for i in range(params['num_neighbors']):
        print(f"{i+1}: {res[i]}")
        # print(f"{i+1}: {res[i]} | DISTANCE: {distances[res[i]]}")
        
    print(f"\nNEAREST {params['num_neighbors']} NEIGHBORS FOR {params['query']}:\n")
    for i in range(params['num_neighbors']):
        print(f"{i+1}: {actual_res[i]}")
        # print(f"{i+1}: {actual_res[i]} | DISTANCE: {actual_distances[actual_res[i]]}")

    
    print(f"\nPRECISION: {precision}")    
    print(f"RECALL: {recall}")
    # print(f"AVERAGE RATIO P.COLLISION/RBO: {avg_ratio}")
    
    print("\n")
    
    
if __name__=="__main__":
    eg1()
    
