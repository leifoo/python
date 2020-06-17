import pandas as pd
import argparse
import sys
import os

parser = argparse.ArgumentParser(description='Read UWI from CSV file and format it for OneTrax')
parser.add_argument('input', nargs='+', type=str,
                   help='Input file name')
args = parser.parse_args()

ifile = args.input[0]
ofile = 'output.txt'

if not ifile:
    sys.exit('Error: No input file!')

if os.path.exists(ifile):
    print('Retrieve data from '+ifile)
    df = pd.read_csv(ifile)

    df_uwi = df['UWI'].apply(str).str

    df['API'] = "'" + df_uwi.slice(stop=2) + '-' + df_uwi.slice(start=2, stop=5) + '-' + df_uwi.slice(start=5, stop=10) + "'" + ','
    df.iloc[-1, -1] = df.iloc[-1, -1][:-1]

    # df['API'] = "'" + df_uwi.slice(stop=2) + '-' + df_uwi.slice(start=2, stop=5) + '-' + df_uwi.slice(start=5, stop=10) + "'" + ',' 
    # df.iloc[-1, -1] = df.iloc[-1, -1][:-1]

    print(df['UWI'].tail())
    print(df['API'].tail())

    df['API'].to_csv(ifile[:-4]+'_uwi2api.txt', header=None, index=None, sep=' ', mode='w')
    # df['API'].to_csv(ifile[:-4]+'_uwi2api.csv')
    # print([x for x in df['API']])

else:
    sys.exit('Error: invalid input file!')

