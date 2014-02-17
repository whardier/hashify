# -*- coding: utf-8 -*-

import os
import sys

import argparse

import path

## ┏┳┓┏━┓╻┏┓╻
## ┃┃┃┣━┫┃┃┗┫
## ╹ ╹╹ ╹╹╹ ╹

def main():

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('--files-from')

    parser.add_argument('source')

    parser.add_argument('destination')

    args = parser.parse_args()
    print args
    source_filter = {}

    source_path = path.path(args.source)
    destination_path = path.path(args.destination)

    if args.files_from:
        files_from = path.path(args.files_from)
        source_iter = files_from.lines(retain=False)
    else:
        source_iter = source_path.walk(errors='warn')

    for p in source_iter:
        print path.path(p).relpath(source_path)

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass

