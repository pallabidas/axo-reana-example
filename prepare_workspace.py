import os
import sys
import json
import argparse
parser = argparse.ArgumentParser(
    description="Prepare workspace"
)
parser.add_argument("--json", help="Sample name of the input json", required=True)
parser.add_argument("--nfiles", type=int, help="Number of files in each child json", required=True)
args = parser.parse_args()

INPUT_JSON = args.json
N_FILES_MAX_PER_SAMPLE = args.nfiles

json_list = []
with open(INPUT_JSON, "r") as fd:
    data = json.load(fd)
    for sample, files in data.items():
        files_dict = data[f"{sample}"]["files"]
        items = list(files_dict.items())

        for i in range(0, len(items), N_FILES_MAX_PER_SAMPLE):
            chunk_items = dict(items[i:i + N_FILES_MAX_PER_SAMPLE])
            chunk = {
                f"{sample}": {
                    "files": chunk_items
                }
            }
            output_file = f"filelist_{sample}_{(i // N_FILES_MAX_PER_SAMPLE) + 1}.json"

            # Write to a new JSON file
            with open(output_file, "w") as f:
                json.dump(chunk, f, indent=4)

            json_list.append(output_file)
            print(f"Saved {output_file}")

# Create the histograms directory if it doesn't exist
directory_name = "histograms"
os.makedirs(directory_name, exist_ok=True)
print(directory_name)
