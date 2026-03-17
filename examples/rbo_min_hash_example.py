
import json
from pathlib import Path
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utilities as ut
import rbo_min_hash as rmh



def eg1():
    """This example computes the hash values of two rankings using the 
    RBOMinHash LSH scheme, then computes the probability of collision of the
    hashes and compares it to the actual RBO similarity of the two rankings
    
    PARAMETERS:
        p: User's persistence
        perm_len: Length of the permutation r used during hashing
        num_hashes: Number of different hash functions used to hash a ranking
        data1, data2: The rankings to be hashed
        directory: (OPTIONAL) The directory from which to load the rankings

    """
    
    # Parameters loading
    with open("eg1_parameters.json", "r") as file:
        params = json.load(file)
        
    #extraction of the rankings
    if params["directory"] is not None:
        directory=Path(params["directory"])
        rankings=ut.load_rankings(directory)
        data1=rankings[params["data1"]]
        data2=rankings[params["data2"]]
    else:
        data1=params["data1"]
        data2=params["data2"]
    
    #Creates backup copy of data to print later, if it will be encoded
    print_data1=data1
    print_data2=data2
        
    # Create the LSH scheme
    lsh = rmh.RBO_LSH(params["p"],params["num_hashes"],params["seed"])
    
    # If needed encodes the rankings
    translator=dict()
    data1_int = all(isinstance(x, int) for x in data1)
    data2_int = all(isinstance(x, int) for x in data2)
    if not data1_int:
        data1=ut.encode_ranking(data1,translator)
    if not data2_int:
        data2=ut.encode_ranking(data2,translator)
        
    # Hashing of the rankings
    lsh.add_ranking(data1)
    lsh.add_ranking(data2)
    # print(lsh.nearest_neighbors(data1, 2))
    
    #Print of the results
    print(f"Persistence: {params['p']}\nNumber of values in the hash: {params['num_hashes']}")
    print(f"\ndata1: {print_data1}\ndata2: {print_data2}")
    p_collisions=lsh.get_rbo_similarity_by_index(0, 1)
    print("\nEstimated probability of hashes collision for data1 and data2 is", p_collisions)
    actual_rbo = rmh.rbo_sim(data1, data2, p=params["p"])
    print("RBO similarity for data1 and data2 is", actual_rbo)
    if p_collisions>0:
        print(f"RATIO: {actual_rbo/p_collisions}")
        print("(Ratio should be in [1,2])")


if __name__ == "__main__":       
    print("\n")
    eg1()
    print("\n")
    
