
def avg_res(l):
    return sum(l) / len(l) if l else 0

def compute_avgs():
    recall = []
    ratio = []
    
    building_time = []
    hashing_time = []
    query_lsh = []
    query_rbo = []
    memory = []
    
    with open("0.2_threshold.txt") as f:
        for line in f:
            if "MEAN RECALL" in line:
                recall.append(float(line.split(":")[1]))
            elif "MEAN RATIO" in line:
                ratio.append(float(line.split(":")[1]))
    
            elif "MEAN BUILDING TIME OF THE LSH SCHEMES" in line:
                building_time.append(float(line.split(":")[1].split()[0]))
            elif "MEAN HASHING TIME" in line:
                hashing_time.append(float(line.split(":")[1].split()[0]))
            elif "MEAN QUERY TIME FOR LSH" in line:
                query_lsh.append(float(line.split(":")[1].split()[0]))
            elif "MEAN QUERY TIME FOR RBO" in line:
                query_rbo.append(float(line.split(":")[1].split()[0]))
            elif "MEAN MEMORY UTILIZATION" in line:
                memory.append(float(line.split(":")[1].split()[0]))
    
    
    
    print("RECALL:", avg_res(recall))
    print("RATIO (RBO/p.collisions):", avg_res(ratio))
    
    print("BUILDING TIME FOR THE LSH:", avg_res(building_time))
    print("HASHING TIME:", avg_res(hashing_time))
    print("QUERY TIME WITH LSH:", avg_res(query_lsh))
    print("QUERY TIME WITHOUT LSH:", avg_res(query_rbo))
    print("MEMORY UTILIZATION BY LSH:", avg_res(memory))
    
    
if __name__=="__main__":
    print("\n")
    compute_avgs()
    print("\n")
    