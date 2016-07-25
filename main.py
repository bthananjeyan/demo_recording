import numpy as np
import sys
import os

if __name__ == "__main__":
    demos =  [demo for demo in os.listdir(os.getcwd()) if (demo != '.git' and demo != 'preprocessing' and demo != 'recording' and demo[-2:] != "py" and demo[-3:] != "pyc" and demo[0] != ".")]
    sys.path.insert(0, os.getcwd() + '/preprocessing')
    from process import *

    demonstrations = []
    for demo in demos:
    	print "Processing ", demo
        demonstrations.append(process_demo(demo))

    # TSC code here


    # Experiment code here

    