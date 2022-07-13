import argparse
import pandas as pd
import re
import sys
import os.path


'''Get list of files with specific extension
   '''
def get_list_files(path, extension):
    for file in os.listdir(path):
        if file.endswith(extension):
            yield(file)


''' Select only date and Price columns.
    Return a new dataframe grouped by month-year
    '''
def merge_csv(path):
    csv_files = list(get_list_files(path, "csv"))
    flag = True
    left_df = pd.DataFrame()
    right_df = pd.DataFrame()
    for file in csv_files:
        if re.search("merged", file):
            print("ignore ", file)
            continue
        if flag:
            left_df = pd.read_csv(path+file)
            flag = False
            continue

        temp_df=pd.read_csv(path+file)
        if len(temp_df) > len(left_df):
            right_df = left_df
            left_df = temp_df
        else:
            right_df = temp_df
        
        left_df = pd.merge(left_df, right_df, how='left', on=['date'])

    # Make-up result
    left_df['date'] = pd.to_datetime(left_df['date'], dayfirst=True, format='%m%y', infer_datetime_format=True)
    left_df.sort_values(by='date')

    return left_df


# Main process
if __name__ == '__main__':
    # Parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-path', type=str, required=True)
    args = parser.parse_args()
    root_path = args.path

    # Check input file is valid or not
    if not os.path.exists(root_path):
        print("Invalid path: ", root_path)
        sys.exit(1)

    print(merge_csv(root_path))
