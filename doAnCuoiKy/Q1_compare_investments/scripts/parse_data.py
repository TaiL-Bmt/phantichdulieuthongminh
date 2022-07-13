import argparse
import pandas as pd
import re
import sys
import os.path

''' Select only Date and price columns.
    Return a new dataframe grouped by month-year
    '''
def extract_data(input_file, output_file):
    # Parse name of file
    base_name = os.path.basename(input_file)
    base_name = re.split('\.', base_name)[0] + "_price"

    # Process data
    df = pd.read_csv(input_file, usecols = ['date','price'])
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, format='%d%m%y', infer_datetime_format=True)
    df['price'].replace('\.', '', regex=True, inplace = True)
    df['price'].replace('\,', '.', regex=True, inplace = True)
    df['price'] = df['price'].astype('float64')
    df.columns = df.columns.str.replace('price', base_name)
    result = df.date.dt.to_period("M")
    g = df.groupby(result)
    g.mean().to_csv(output_file)


# Main process
if __name__ == '__main__':
    # Parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-in', type=str, required=True)
    parser.add_argument('--output', '-out', type=str, required=True)
    args = parser.parse_args()
    input_file = args.input
    output_file = args.output


    # Check input file is valid or not
    if not os.path.exists(input_file):
        print("Invalid input file: ", input_file)
        sys.exit(1)

    extract_data(input_file, output_file)
