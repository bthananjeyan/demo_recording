import h5py
import numpy as np
from demo_recorder import *
import sys

def join_data(args):
    for directory in args:
        psm1_sync = read_file(directory + "/psm1_sync.p")
        psm2_sync = read_file(directory + "/psm2_sync.p")
        t_sync = np.ravel(psm1_sync[:,0])

        f = open(directory + "/camera_to_robot.p", "rb")
        cmat = pickle.load(f)
        f.close()

        # Uncomment when ready
        # f = open(directory + "/camera_to_psm1.p", "rb")
        # psm1_transform = pickle.load(f)
        # f.close()

        # f = open(directory + "/camera_to_psm2.p", "rb")
        # psm2_transform = pickle.load(f)
        # f.close()

        with h5py.File(directory + '/data.h5', 'w') as hf:
            hf.create_dataset('psm1_sync', data=psm1_sync)
            hf.create_dataset('psm2_sync', data=psm2_sync)
            hf.create_dataset('t_sync', data=t_sync)
            hf.create_dataset('camera_to_robot', data=cmat)
            # Uncomment When Ready
            # hf.create_dataset('psm1_transform', data=psm1_transform)
            # hf.create_dataset('psm2_transform', data=psm2_transform)



if __name__ == "__main__":
    
    for directory in sys.argv[1:]:
        directory = "../" + directory
        psm1_sync = read_file(directory + "/psm1_sync.p")
        psm2_sync = read_file(directory + "/psm2_sync.p")
        t_sync = np.ravel(psm1_sync[:,0])

        f = open(directory + "/camera_to_robot.p", "rb")
        cmat = pickle.load(f)
        f.close()


        # Uncomment when ready
        # f = open(directory + "/camera_to_psm1.p", "rb")
        # psm1_transform = pickle.load(f)
        # f.close()

        # f = open(directory + "/camera_to_psm2.p", "rb")
        # psm2_transform = pickle.load(f)
        # f.close()

        with h5py.File(directory + '/data.h5', 'w') as hf:
            hf.create_dataset('psm1_sync', data=psm1_sync)
            hf.create_dataset('psm2_sync', data=psm2_sync)
            hf.create_dataset('t_sync', data=t_sync)
            hf.create_dataset('camera_to_robot', data=cmat)
            # Uncomment When Ready
            # hf.create_dataset('psm1_transform', data=psm1_transform)
            # hf.create_dataset('psm2_transform', data=psm2_transform)
