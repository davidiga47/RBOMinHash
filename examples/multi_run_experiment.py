
import json
import ann_example as ann

def run_experiment():
    with open("ann_parameters.json", "r") as file:
        params = json.load(file)
    
    res = [0 for _ in range(9)]
    for i in range(params['num_runs']):
        tmp = ann.ann()
        for j in range(9):
            res[j] = (res[j] * i + tmp[j]) / (i+1)
    
    return res
    
    
def eg1():
    
    res = run_experiment()
    with open("ann_parameters.json", "r") as file:
        params = json.load(file)
    
    print(f"\nEXPERIMENT WITH {params['num_runs']} RUNS:")
    print(f"QUERY FILE: {params['query']}")
    
    print("\nPARAMETERS:")
    print(f"\nPersistence: {params['p']}\nNumber of values in the hash: {params['num_hashes']}\nNumber of neighbors: {params['num_neighbors']}")
    
    print("\nRESULTS:")
    print(f"\nMEAN PRECISION: {res[0]}")
    print(f"MEAN RECALL: {res[1]}")
    print(f"MEAN RATIO (RBO/p. collision): {res[2]}")
    print(f"\nMEAN BUILDING TIME OF THE LSH SCHEMES: {res[3]:.6f} seconds")
    print(f"MEAN ELAPSED TIME: {res[4]:.6f} seconds")
    print(f"MEAN HASHING TIME: {res[7]:.6f} seconds")
    print(f"MEAN QUERY TIME FOR LSH: {res[5]:.6f} seconds")
    print(f"MEAN QUERY TIME FOR RBO: {res[6]:.6f} seconds")
    print(f"TOTAL ELAPSED TIME: {(res[4] * params['num_runs']):.6f} seconds")
    print(f"\nMEAN MEMORY UTILIZATION: {res[8]:.2f} MB")
    print("\n")
    
    
if __name__=="__main__":
    eg1()
    
    