
import json
import ann_example as ann
from pathlib import Path
import utilities as ut
import sys

def multi_query_experiment():
    
    original_stdout = sys.stdout
    
    with open("ann_parameters.json", "r") as file:
        params = json.load(file)
    files=params['multi_query']
    original_query=params['query']
    
    res_dir = "results/" + str(params['num_neighbors']) + "_neighbors"
    if params['num_neighbors'] == 1:
        res_dir="results/1_neighbor"
    Path(res_dir).mkdir(exist_ok=True)
    
    res_path=res_dir+"/multi_query.txt"
    results=open(res_path, "w")

    for query in files:
        ut.update_json("ann_parameters.json", "query", query)
        sys.stdout=original_stdout
        print(f"Running experiment with query file: {query}")
        sys.stdout=results
        ann.eg1()
    
    sys.stdout=original_stdout
    results.close()
    ut.update_json("ann_parameters.json", "query", original_query)
        

if __name__=="__main__":
    print("\n")
    multi_query_experiment()
    print("\n")
    
    