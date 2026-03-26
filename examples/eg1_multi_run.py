
import json
import rbo_min_hash_example as ex
import sys

def run_experiment():
    with open("rbo_parameters.json", "r") as file:
        params = json.load(file)
    
    res = 0
    for i in range(params['num_runs']):
        #print(f"Run #{i+1}")
        tmp = ex.eg1()
        res = ((res * i) + (tmp[0]/tmp[1])) / (i + 1)
    
    return res
    
    
def eg1(out=None):
    
    res = run_experiment()
    
    if out is not None:
        original_stdout=sys.stdout
        sys.stdout=out
    
    with open("rbo_parameters.json", "r") as file:
        params = json.load(file)
    
    print(f"\nEXPERIMENT WITH {params['num_runs']} RUNS:")
    
    print("\nPARAMETERS:")
    print(f"\nPersistence: {params['p']}\nNumber of values in the hash: {params['num_hashes']}")
    print(f"\n MEAN RATIO: {res}")
    print("\n")
    
    if out is not None:
        sys.stdout=original_stdout
    
    
if __name__=="__main__":
    print("\n")
    eg1()
    print("\n")
    
    