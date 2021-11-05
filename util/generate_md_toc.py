#!/usr/bin/env python3

import sys
import argparse
import json
import re


def main():
    args = get_args()
    for filename in args.files:
        with open(filename, 'r') as files:
            toc_string = ''
            count = 1
            for line in files.readlines():
                if line.startswith('#'):
                    contents = re.sub('\n', '', line).split(' ')
                    level = len(contents[0])
                    count += 1
                    toc_string += '    ' * (level - 1)
                    if args.bullet:
                        toc_string += '* '
                    else:
                        toc_string += '{}. '.format(count)
                    toc_string += '[{}](#{})\n'\
                            .format(' '.join(contents[1:]),
                                    '-'.join([re.sub('[^a-z]', '', x.lower()) for x in contents[1:]]))

        print('-' * len(filename))
        print(filename)
        print('# Table of Contents')
        print(toc_string[:-1])
        print('-' * len(filename))



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='N', type=str, nargs='+',
                        help=('File(s) to analyze'))
    parser.add_argument('-b', '--bullet', action='store_true', default=False,
                        help='Use bullets instead of numbers')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    sys.exit(main())