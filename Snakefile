import json
import math

N_FILES_MAX_PER_SAMPLE = config["n_files_max_per_sample"] # Maximum files per chunk
INPUT_JSON = config["input_json"]
PLOTS = config["plots"]

# Read JSON and compute the number of chunks per sample
with open(INPUT_JSON, "r") as json_file:
    data = json.load(json_file)

sample_names = list(data.keys())

num_chunks = {
    sample: math.ceil(len(data[sample]["files"]) / N_FILES_MAX_PER_SAMPLE)
    for sample in sample_names
}

# Generate expected outputs dynamically
json_files = []
output_files = []
output_plots = []

for sample, max_index in num_chunks.items():
    for index in range(1, max_index + 1):
        json_files.append(f"filelist_{sample}_{index}.json")
        output_files.append(f"histograms/hist_result_{sample}_{index}.pkl")

for sample in sample_names:
    for plot in PLOTS:
        output_plots.append(f"{plot}_{sample}.png")

# Define the final target rule
rule all:
    input:
        json_files,
        output_files,
        output_plots

# Rule for generating input json files
rule prepare:
    input: 
        "prepare_workspace.py",
        INPUT_JSON
    output:
        json_files
    resources:
        kerberos=True
    container:
        "docker.io/coffeateam/coffea-dask-almalinux9:latest"
    shell:
        """
        python3 prepare_workspace.py --json {INPUT_JSON} --nfiles {N_FILES_MAX_PER_SAMPLE}
        """

# Rule for skimming
rule skim:
    input:
        "axo_studies.py"
    output:
        "histograms/hist_result_{sample}_{index}.pkl"
    resources:
        kerberos=True
    container:
        "docker.io/coffeateam/coffea-dask-almalinux9:latest"
    params:
        sample_name="{sample}",
        index="{index}"
    shell:
        """
        python3 axo_studies.py --sample_name {params.sample_name} --index {params.index}
        """

# Rule for merging and plotting
rule plot:
    input:
        output_files,
        "combine_hists.py",
        "plotting.py"
    output:
        output_plots
    resources:
        kubernetes_memory_limit="1850Mi"
    container:
        "docker.io/coffeateam/coffea-dask-almalinux9:latest"
    shell:
        """
        python3 combine_hists.py --files histograms/hist_result_{sample}_*.pkl --output histograms/all_hists_{sample}.pkl
        python3 plotting.py --file histograms/all_hists_{sample}.pkl --vars {PLOTS}
        """
