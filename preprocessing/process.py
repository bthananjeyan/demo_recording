import numpy as np
import h5py
import sys

def process_demo(demo_directory):
	# Load data
	with h5py.File("../" + demo_directory + '/data.h5','r') as hf:
		psm1_sync = np.array(hf.get('psm1_sync'))
		psm2_sync = np.array(hf.get('psm2_sync'))
	# Fix times
	temp = np.ones((psm1_sync.shape[0], 1)) * psm1_sync[0,0]
	psm1_sync[:,0] -= temp
	psm2_sync[:,0] -= temp
	# Throw out bad features
	good_features = np.r_[0:psm1_sync.shape[1]]
	psm1_sync = psm1_sync[:, good_features]
	psm2_sync = psm2_sync[:, good_features]
	return psm1_sync, psm2_sync

if __name__ == "__main__":

	for demo in sys.argv[1:]:
		process_demo(demo)
