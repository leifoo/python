#!/usr/bin/env python

import os
import sys
import re
import argparse
import subprocess

sys.path.append(os.path.abspath("/home/lxf470/project/python/util/utils/"))
from utils import remove_suffix, find_all

data_types = ['str', 'int', 'float', 'list',  'bool', 'set'] # 'tuple', 'dict'

def generate_dcc(var):
    name, typ, val = var
    string = ''
    if typ == 'str':
        string = f"dcc.Dropdown([{val}], {val}, id='dropdown-selection-{name}')"
    elif typ == 'set':
        string = f"dcc.Dropdown([{val}], {val}, id='dropdown-selection-{name}')"
    elif typ == 'bool':
        string = f"daq.BooleanSwitch(on={val}, label='{name}', labelPosition='top', id='booleanSwitch-{name}')"
    elif typ == 'float':
        string = f"dcc.Input(value='{val}', type='number', id='input-{typ}-{name}')"
    elif typ == 'int':
        string = f"dcc.Input(value='{val}', type='number', id='input-{typ}-{name}')"
    elif typ == 'list':
        string = f"dcc.Input(value='{val}', type='text', id='input-{typ}-{name}')"
    elif typ not in data_types:
        if val != '':
            string = f"dcc.Dropdown([{val}], {val}, id='dropdown-selection-{name}')"
        else:
            string = f"dcc.Dropdown(['{typ}'], '{typ}', id='dropdown-selection-{name}')"
    else:
        string = f"dcc.Input(value='{val}', type='text', id='input-{typ}-{name}')"
    return string

# Create a parser
parser = argparse.ArgumentParser(description='Convert functions to Dash Core Components')

parser.add_argument('input', nargs=1, type=str,
                   help='Input Python file')
parser.add_argument('-c', '--component', nargs=1, type=str,
                   help='Dash Core Component (DCC) output type')
parser.add_argument('output', nargs='?', type=str,
                   help='Output file name (default = output.txt)')

args = parser.parse_args()
print(args)

# Input
input_name = 'input'
ifile = args.input[0]
if os.path.exists(ifile):
    base = os.path.basename(ifile)
    name_tuple = os.path.splitext(base)
    input_name = ''.join(name_tuple[:-1])
    print(ifile, base, name_tuple, input_name)
else:
    print(f'{args.input[0]} does not exist!')

# DCC
dcc = "dcc.Input"
if args.component:
    dcc = args.component[0]

# Output file name
fname = f'{input_name}'

if args.output: 
    fname = remove_suffix(args.output, '.txt')

ofile = fname+'_dash.txt'
# print(ofile)

class_names = []
para_list = []

# Search class name, constructor in file
with open(ifile, 'r') as fp:
    # read all lines using readline()
    string = fp.read()

    # find all the classes
    class_indexes = find_all(string, 'class')

    for i in class_indexes:
        e = string.find(':', i)
        class_names.append(string[i+5:e].strip(' \n'))

    # print(class_indexes, class_names)

    # Parse all the inputs
    for i, start in enumerate(class_indexes):
        s = start
        e = len(string) if i == len(class_indexes)-1 else class_indexes[i+1]
        
        j = string.find('__init__', s, e)
        if j == -1:
            raise('No constructor __init__ !')
        else:
            m = string.find('(', j, e)
            n = string.find(')', m, e)
            p = string[m+1:n]
            p_list = p.split(',')
            paras = [x.strip('\n ') for x in p_list]
            para_list.append(paras)

# print(para_list)

inputs = []

for q in para_list:
    input = []
    for p in q:
        inputName = ''
        inputType = ''
        inputDefaultValue = ''

        if p != '' and p != 'self':
            i = p.find(':')
            j = p.find('=')
            # print(p, i, j)

            if i != -1:
                inputName = p[:i]
                if j != -1:
                    inputType = p[i+1:j]
                    inputDefaultValue = p[j+1:]
                else:
                    inputType = p[i+1:]
            else:
                if j != -1:
                    inputName = p[:j]
                    inputDefaultValue = p[j+1:]
                else:
                    inputName = p
            
            inputName = inputName.strip()
            inputType = inputType.strip()
            inputDefaultValue = inputDefaultValue.strip()
        
            input.append((inputName, inputType, inputDefaultValue))
    
    inputs.append(input[:])

# print(f'inputs = {inputs}')

inputs_clean = []
dcc_list = []

for items in inputs:
    temp_list = []
    temp_dcc = []

    for name, typ, val in items:
        input_list = [name, '', '']
        if typ != '':
            for dt in data_types:
                if re.search(dt, typ, re.IGNORECASE):
                    input_list[1] = dt
            if input_list[1] == '':
                input_list[1] = typ

        if val != '':
            input_list[2] = val

        temp_list.append(tuple(input_list))
        temp_dcc.append(generate_dcc(input_list))

    inputs_clean.append(temp_list)
    dcc_list.append(',\n'.join(temp_dcc[:]))

# print(inputs_clean)
for i in range(len(class_names)):
    print(f'\n{class_names[i]}\n')
    print(f'{dcc_list[i]}\n')

# Write to file
if args.output:
    with open(ofile, "w") as text_file:
        text_file.write(dcc_list)