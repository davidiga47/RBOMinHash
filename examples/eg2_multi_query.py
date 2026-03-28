
import json
import eg2_multi_run as ann
import utilities as ut

def eg2_multi_query():
    
    with open("ann_parameters.json", "r") as file:
        params = json.load(file)
    files=params['queries']
    original_query=params['query']
    res_path = "results/ann_experiment/" + str(params['num_neighbors']) + "_neighbors.txt"
    results=open(res_path, "w")

    for query in files:
        ut.update_json("ann_parameters.json", "query", query)
        print(f"\nRunning experiment with query file: {query}")
        ann.eg2_multi_run(results)
    

    results.close()
    ut.update_json("ann_parameters.json", "query", original_query)
        

if __name__=="__main__":
    print("\n")
    eg2_multi_query()
    print("\n")
    
    