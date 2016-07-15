import Tkinter
from Tkinter import *
import pickle, time
import multiprocessing
import os
from robot import *
import numpy as np
import IPython
from ImageSubscriber import ImageSubscriber
import scipy
import matplotlib.pyplot as plt
from demo_recorder import read_file


if __name__ == "__main__":
	pts = read_file("default/psm1.p")
	print pts.shape
	for i in range(8):
		plt.plot(pts[:,i])
		plt.show()
	pts = read_file("default/psm2.p")
	print pts.shape
	for i in range(8):
		plt.plot(pts[:,i])
		plt.show()