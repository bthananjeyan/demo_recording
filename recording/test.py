"""
This is a testing script.
"""

from demo_recorder import *
import sys


if __name__ == "__main__":

    directory = "../" + sys.argv[1]

    print read_file(directory + "/psm1_sync.p").shape
    print read_file(directory + "/psm2_sync.p").shape
