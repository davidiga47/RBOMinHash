
import json
import sys
from pathlib import Path
import multi_run_experiment as ann
import utilities as ut

def both_multi():
    
    original_stdout = sys.stdout
    
    with open("ann_parameters.json", "r") as file:
        params = json.load(file)
    files=params['multi_query']
    
    res_dir = "results/" + str(params['num_neighbors']) + " neighbors"
    Path(res_dir).mkdir(exist_ok=True)
    
    res_path=res_dir+"/both_multi.txt"
    results=open(res_path, "w")

    for file in files:
        if file < 10:
            query="file0"+str(file)+".txt"
        else:
            query="file"+str(file)+".txt"
        ut.update_json("ann_parameters.json", "query", query)
        sys.stdout=original_stdout
        print(f"Running experiment on {query}")
        sys.stdout=results
        ann.eg1()
    
    sys.stdout=original_stdout
    results.close()
    ut.update_json("ann_parameters.json", "query", "file42.txt")
        

if __name__=="__main__":
    print("\n")
    both_multi()
    print("\n")
    
    