#!/usr/bin/env python
# coding: utf8
"""Usage: main.py [-h | --help] <columns> <rows> <pii> <file> [<seed>]

    Options:
        -h --help    show the Data Generator Menu

    Arguments:
        columns    (Int) total number of columns
        rows       (Int) total number of rows
        pii        (Int) total number of PII in columns
        file       (String) output file
        seed       (Optional) value of random seed for faker

"""
from docopt import docopt  # Command Line using docstrings tool
import random  # Used to randomize seeding of generator
from csv_gen import CsvGenerator, create_faker


if __name__ == "__main__":
    args = docopt(__doc__)

    # Create random seed to be used for the generator.
    if args["<seed>"] is None:
        seed = random.randint(0, 2**16)
    else:
        seed = int(args["<seed>"])

    # Initialize an example Faker instance and CSV Generator.
    fake = create_faker(seed)
    gen = CsvGenerator(
        int(args["<columns>"]),
        int(args["<rows>"]),
        int(args["<pii>"]),
        fake)
    gen.write(args["<file>"], True)
