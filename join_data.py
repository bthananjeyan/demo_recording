import h5py
import numpy as np
from demo_recorder import *
import sys

if __name__ == "__main__":
    
    for directory in sys.argv[1:]:
        psm1_sync = read_file(directory + "/psm1_sync.p")
        psm2_sync = read_file(directory + "/psm2_sync.p")
        psm1 = read_file(directory + "/psm1.p")
        psm2 = read_file(directory + "/psm2.p")
        t_sync = np.ravel(psm1_sync[:,0])
        t = np.ravel(psm1[:,0])
        with h5py.File(directory + '/data.h5', 'w') as hf:
            hf.create_dataset('psm1_sync', data=psm1_sync)
            hf.create_dataset('psm2_sync', data=psm2_sync)
            hf.create_dataset('t_sync', data=t_sync)
            hf.create_dataset('t', data=t)
            hf.create_dataset('psm1', data=psm1)
            hf.create_dataset('psm2', data=psm2)
