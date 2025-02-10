import argparse
from coffea.util import load, save
import glob
import os
import sys

def getArgs():
    parser = argparse.ArgumentParser(description="Combine histograms from multiple files.")
    parser.add_argument("--files", nargs="+", help="Input files (wildcards allowed)")
    parser.add_argument("--output", required=True, help="Output file name")

    args = parser.parse_args()

    # Expand wildcards and collect file paths
    file_list = []
    for pattern in args.files:
        expanded_files = glob.glob(pattern)
        if expanded_files:
            file_list.extend(expanded_files)
        else:
            file_list.append(pattern)  # Keep the original if no match (handles explicit filenames)

    # Remove duplicates and check if files exist
    file_list = sorted(set(file_list))  # Sort for consistency and remove duplicates
    missing_files = [f for f in file_list if not os.path.isfile(f)]

    if missing_files:
        print(f"Error: The following files do not exist: {', '.join(missing_files)}", file=sys.stderr)
        sys.exit(1)

    return file_list, args.output

def main(file_list, output):

    hist_result_list = []
    for i in range(len(file_list)):
        hist_result_list.append(load(file_list[i]))

    datasets = list(hist_result_list[0].keys())
    hist_result = {}
    for dataset in datasets:
        hist_result[dataset] = {}
        hist_result[dataset]['hists'] = {}
        hist_list = list(hist_result_list[0][dataset]['hists'].keys())
        for hist_name in hist_list:
            print(hist_name)
            hist_result[dataset]['hists'][hist_name] = sum(
                [hist_result_list[i][dataset]['hists'][hist_name] for i in range(len(hist_result_list))]
            )

    save(hist_result, output)

    return



if __name__=="__main__":
    files, output = getArgs()
    print("Files to process:", files)

    main(files, output)
