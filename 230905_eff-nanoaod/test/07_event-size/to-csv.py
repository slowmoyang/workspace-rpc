#!/usr/bin/env python3
from pathlib import Path
import argparse
import pandas as pd


def run(input_path: Path):
    with open(input_path) as stream:
        _, columns, *df = stream.read().split('\n')
    columns = columns.split(' | ')
    df = [line.split(' ') for line in df
          if len(line) > 0]

    df = pd.DataFrame(df, columns=columns)

    output_path = input_path.with_suffix('.csv')
    print(f'writing to {output_path}')
    df.to_csv(output_path, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=Path, help='Help text')
    args = parser.parse_args()

    run(**vars(args))

if __name__ == "__main__":
    main()
