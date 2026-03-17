
import json
import ann_example as ann
from pathlib import Path
import utilities as ut
import sys

def multi_query_experiment():
    
    with open("ann_parameters.json", "r") as file:
        params = json.load(file)
    files=params['multi_query']
    
    res_dir = "results/" + str(params['num_neighbors']) + " neighbors"
    Path(res_dir).mkdir(exist_ok=True)
    
    res_path=res_dir+"/multi_query.txt"
    results=open(res_path, "w")
    sys.stdout=results

    for file in files:
        if file < 10:
            query="file0"+str(file)+".txt"
        else:
            query="file"+str(file)+".txt"
        ut.update_json("ann_parameters.json", "query", query)
        ann.eg1()
    
    results.close()
    ut.update_json("ann_parameters.json", "query", "file42.txt")
        

if __name__=="__main__":
    multi_query_experiment()
    
    