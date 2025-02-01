# Define output folder
output_dir = "$REANA_WORKSPACE"

# Define the final target rule
rule all:
    input:
        "hist_result_Scouting_2024I_test.pkl"

# Rule for skimming
rule skimming:
    input:
        "axo_studies.py",
        "2024_data_filelist.json"
    output:
        "hist_result_Scouting_2024I_test.pkl"
    resources:
        kerberos=True
    container:
        #"registry.cern.ch/docker.io/reanahub/reana-demo-agc-cms-ttbar-coffea:1.0.0"
        "docker.io/coffeateam/coffea-dask-almalinux9:latest"
    shell:
        """
        python3 axo_studies.py 
        """

# Rule for datacarding
#rule datacarding:
#    input:
#        "output/skimming/DY_Skim.root"
#    output:
#        config['output_file']
#    params:
#        year = "2022postEE"
#    container:
#        "registry.cern.ch/docker.io/reanahub/reana-demo-agc-cms-ttbar-coffea:1.0.0"
#    shell:
#        """
#        mkdir -p {output_dir}/output/datacards
#        cd /code/CMSSW_13_0_10/src/SUS_ex/Analysis2 && \
#        source /cvmfs/cms.cern.ch/cmsset_default.sh && \
#        cmsenv && \
#        ./FinalSelection_mutau.exe {params.year} {output_dir}/{input} {output_dir}/{output} DY DY
#        """
