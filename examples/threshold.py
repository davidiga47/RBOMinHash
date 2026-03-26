
import json
from pathlib import Path
import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utilities as ut
import rbo_min_hash as rmh

def over_thresh():
    # Parameters loading
    with open("thresh_parameters.json", "r") as file:
        params = json.load(file)
    directory=Path(params["directory"])
    
    #LSH scheme creation
    loaded=ut.load_rankings(directory)           #List of the rankings
    seed=np.random.randint(1,1001)
    lsh=rmh.RBOMinHash(params["p"], params["num_hashes"], seed)  
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
        
    similar=lsh.most_similar(query, params['threshold'])
    res=[]
    for elm in similar:
        if elm[1]==query_index:
            continue
        for i,file in enumerate(rankings.keys()):
            if i == elm[1]:
                res.append(file)
                break
    
    #Computation of k nearest neighbors using RBO
    actual_similar=rmh.exact_most_similar(list(rankings.values()), query,
                                        params['p'], params['threshold'])
    actual_res=[]
    for elm in actual_similar:
        if elm[1]==query_index:
            continue
        for i,file in enumerate(rankings.keys()):
            if i == elm[1]:
                actual_res.append(file)
                break
    
    recall=len(set(res) & set(actual_res))/len(set(res) | set(actual_res))
    
    
    return (recall,
            res,
            actual_res)

def eg2():   
    
    print("\n")
    
    similar_exp=over_thresh()
    
    #Fetching of the results
    recall=similar_exp[0]
    res=similar_exp[1]
    actual_res=similar_exp[2]
    
    
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
    # print(f"AVERAGE RATIO P.COLLISION/RBO: {avg_ratio}")
    
    print("\n")
    
    
if __name__=="__main__":
    eg2()
    
