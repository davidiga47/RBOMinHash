
import json
import eg3_multi_run as threshold
import utilities as ut

def eg3_multi_query():
    
    with open("thresh_parameters.json", "r") as file:
        params = json.load(file)
    files=params['queries']
    original_query=params['query']
    res_path = "results/threshold_experiment/" + str(params['threshold']) + "_threshold.txt"
    results=open(res_path, "w")

    for query in files:
        ut.update_json("thresh_parameters.json", "query", query)
        print(f"\nRunning experiment with query file: {query}")
        threshold.eg3_multi_run(results)
    

    results.close()
    ut.update_json("threshold_parameters.json", "query", original_query)
        

if __name__=="__main__":
    print("\n")
    eg3_multi_query()
    print("\n")
    
    