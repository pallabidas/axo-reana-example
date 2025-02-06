import json
with open("2024_data_filelist.json", "r") as json_file:
    dataset = json.load(json_file)
    sample_names = []
    for sample, files in dataset.items():
        sample_names.append(sample)
print(sample_names)

# Define output folder
output_dir = "$REANA_WORKSPACE"

# Define the final target rule
rule all:
    input:
        expand("histograms/hist_result_{sample}_test.pkl", sample=sample_names)
        #expand("histograms/hist_result_{sample}_test.pkl", sample=config["sample"])

# Rule for skimming
rule skimming:
    input:
        "axo_studies.py",
        "2024_data_filelist.json",
    output:
        "histograms/hist_result_{sample}_test.pkl"
    resources:
        kerberos=True
    container:
        "docker.io/coffeateam/coffea-dask-almalinux9:latest"
    shell:
        """
        mkdir histograms
        python3 axo_studies.py 
        """

#rule plotting:
#    container:
#        "docker.io/coffeateam/coffea-dask-almalinux9:latest"
#    resources:
#        kubernetes_memory_limit="1850Mi"
#    output:
#        "histograms/plot_{sample}.png",
#    input:
#        "histograms/hist_result_{sample}_test.pkl",
#        "plotting.py"
#    shell:
#        "python3 plotting.py"
#
