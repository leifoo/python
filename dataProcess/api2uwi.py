import pandas as pd
import argparse
import sys
import os

# python .\api2uwi.py .\OT_UWI_42_FA_Level2.csv
parser = argparse.ArgumentParser(description='Read API from CSV file and format it to UWI format for IHS')
parser.add_argument('input', nargs='+', type=str,
                   help='Input file name')
args = parser.parse_args()

ifile = args.input[0]
ofile = 'output_api.txt'

if not ifile:
    sys.exit('Error: No input file!')

if os.path.exists(ifile):
    print('Retrieve data from '+ifile)
    df = pd.read_csv(ifile, header=None, names=['API'])
    # df.reindex()

    # print(df)

    df['API'] = "'" + df['API'].str.replace('-', '') + "'" + ','
    # df['API'].replace('-', '', regex=True, inplace=True)

    df.iloc[-1, -1] = df.iloc[-1, -1][:-1]

    print(df['API'])

    print(df['API'].str.startswith("'f", na=False))
    df = df[df['API'].str.match(pat = "('42.)")]
    print(df)

    print('Total number: ', len(df.index))
    df['API'].to_csv(ifile[:-4]+'_UWI.txt', header=None, index=None, sep=' ', mode='w')

else:
    sys.exit('Error: invalid input file!')

