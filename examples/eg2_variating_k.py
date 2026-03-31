
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import json

import eg2_multi_run as exp
import utilities as ut


def eg2_multi_query():
    
    with open("ann_parameters.json", "r") as file:
        params = json.load(file)
    files=params['queries']
    original_query=params['query']
    res=[]

    for query in files:
        ut.update_json("ann_parameters.json", "query", query)
        print(f"\nRunning experiment with query file: {query}")
        res.append(exp.run_experiment()[:3])
    
    res = [sum(col) / len(col) for col in zip(*res)]
    
    ut.update_json("ann_parameters.json", "query", original_query)
    return res

def variating_k():
    res=dict()
    for i in range(1,5):
        hashes = 5 * i
        print(f"\nRunning experiment with {hashes} hash functions")
        ut.update_json("ann_parameters.json", "num_hashes", hashes)
        res[hashes]=eg2_multi_query()
    ut.update_json("ann_parameters.json", "num_hashes", 100)
    return res


def plot_results(results, metric_names, output_file="metrics_plot.png"):

    # Converting the dictionary into a dataframe
    df = pd.DataFrame(results).T

    # Assigning labels
    df.columns = metric_names

    # X-axis name setting
    df = df.reset_index()
    df = df.rename(columns={"index": "x"})

    # Long format for seaborn
    df_long = df.melt(
        id_vars="x",
        var_name="metric",
        value_name="value"
    )

    sns.set_theme(style="whitegrid", context="paper")

    fig, ax = plt.subplots()

    # Plot
    sns.lineplot(
        data=df_long,
        x="x",
        y="value",
        hue="metric",
        marker="o",
        ax=ax
    )
    
    xlabel="Number of hash functions used"
    
    plt.xlabel(xlabel)
    plt.ylabel("Metric value")
    plt.title("Metrics trend")
    plt.legend(title="Metric")

    fig.tight_layout()
    fig.savefig(output_file, dpi=300)
    plt.close(fig)
    # plt.show()



if __name__=="__main__":
    plot_results(variating_k(), ["precision","recall","average ratio"], 
                 output_file="results/ann_experiment/variating_k.png")
    
    
    
