import argparse
import pandas as pd
import sys
import os.path
from parse_data import extract_data
from merge_data import merge_csv

'''Get list of files with specific extension
   '''
def get_list_files(path, extension):
    for file in os.listdir(path):
        if file.endswith(extension):
            yield(file)


# Parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--raw_data_path', '-in', type=str, required=True)
parser.add_argument('--processed_data_path', '-out', type=str, required=True)
args = parser.parse_args()
raw_path = args.raw_data_path
processed_path = args.processed_data_path


# Main process
if __name__ == '__main__':
    # Check arguments is valid or not
    if not os.path.exists(raw_path):
        print("Invalid input file: ", raw_path)
        sys.exit(1)

    # Check output path
    if not os.path.exists(processed_path):
        os.mkdir(processed_path)
    else:
        for file in os.listdir(processed_path):
            os.remove(os.path.join(processed_path, file))

    csv_files = list(get_list_files(raw_path, "csv"))
    print(csv_files)

    # Extract data from raw data
    for file in csv_files:
        extract_data(raw_path+file, processed_path+file)

    # Merge all process data
    merged_df = merge_csv(processed_path)
    merged_df.to_csv(processed_path+'merged.csv', index=False)

    print("Finished")
