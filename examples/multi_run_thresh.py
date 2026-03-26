
import json
import threshold
import sys

def run_experiment():
    with open("thresh_parameters.json", "r") as file:
        params = json.load(file)
    
    res = [0 for _ in range(8)]
    for i in range(params['num_runs']):
        print(f"Run #{i+1}")
        tmp = threshold.over_thresh()
        for j in range(8):
            res[j] = (res[j] * i + tmp[j]) / (i+1)
    
    return res
    
    
def eg1(out=None):
    
    res = run_experiment()
    
    if out is not None:
        original_stdout=sys.stdout
        sys.stdout=out
    
    with open("thresh_parameters.json", "r") as file:
        params = json.load(file)
    
    print(f"\nEXPERIMENT WITH {params['num_runs']} RUNS:")
    print(f"QUERY FILE: {params['query']}")
    
    print("\nPARAMETERS:")
    print(f"\nPersistence: {params['p']}\nNumber of values in the hash: {params['num_hashes']}\nThreshold: {params['threshold']}")
    
    print("\nRESULTS:")
    print(f"MEAN RECALL: {res[0]}")
    print(f"MEAN RATIO: {res[1]}")
    print(f"\nMEAN BUILDING TIME OF THE LSH SCHEMES: {res[2]:.6f} seconds")
    print(f"MEAN ELAPSED TIME: {res[3]:.6f} seconds")
    print(f"MEAN HASHING TIME: {res[6]:.6f} seconds")
    print(f"MEAN QUERY TIME FOR LSH: {res[4]:.6f} seconds")
    print(f"MEAN QUERY TIME FOR RBO: {res[5]:.6f} seconds")
    print(f"TOTAL ELAPSED TIME: {(res[3] * params['num_runs']):.6f} seconds")
    print(f"\nMEAN MEMORY UTILIZATION: {res[7]:.2f} KB")
    print("\n")
    
    if out is not None:
        sys.stdout=original_stdout
    
    
if __name__=="__main__":
    print("\n")
    eg1()
    print("\n")
    
    