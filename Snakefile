import json

INPUT_JSON = config["input_json"]
PLOTS = config["plots"]

# Read JSON and compute the number of chunks per sample
with open(INPUT_JSON, "r") as json_file:
    data = json.load(json_file)

sample_names = list(data.keys())

# Generate expected outputs dynamically
output_files = []
output_plots = []

for sample in sample_names:
    for plot in PLOTS:
        output_files.append(f"histograms/hist_result_{sample}.pkl")
        output_plots.append(f"{plot}_{sample}.png")

# Define the final target rule
rule all:
    input:
        output_plots

# Rule for skimming
rule skim:
    input:
        "axo_studies.py",
        INPUT_JSON
    output:
        "histograms/hist_result_{sample}.pkl"
    resources:
        kerberos=True
    container:
        "docker.io/coffeateam/coffea-dask-almalinux9:latest"
    shell:
        """
        mkdir histograms
        python3 axo_studies.py 
        """

# Rule for and plotting
rule plot:
    input:
        output_files,
        "plotting.py"
    output:
        output_plots
    resources:
        kubernetes_memory_limit="1850Mi"
    container:
        "docker.io/coffeateam/coffea-dask-almalinux9:latest"
    shell:
        """
        python3 plotting.py --file histograms/hist_result_{sample}.pkl --vars {PLOTS}
        """
