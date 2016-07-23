import numpy as np
import h5py
import sys

def process_demo(demo_directory):
	# Load data
	with h5py.File("../" + demo_directory + '/data.h5','r') as hf:
		psm1_sync = np.matrix(hf.get('psm1_sync'))
		psm2_sync = np.matrix(hf.get('psm2_sync'))
		transform = np.matrix(hf.get('camera_to_robot'))
	invtransform = np.zeros(transform.shape)
	invtransform[:3, :3] = transform[:3,:3].T
	invtransform[:, 3] = -tranform[:,3]
	# Fix times
	temp = np.ones((psm1_sync.shape[0], 1)) * psm1_sync[0,0]
	psm1_sync[:,0] -= temp
	psm2_sync[:,0] -= temp
	# Throw out bad features
	good_features = np.r_[0:psm1_sync.shape[1]]
	psm1_sync = psm1_sync[:, good_features]
	psm2_sync = psm2_sync[:, good_features]
	return psm1_sync, psm2_sync

def transform_matrix(data, transform):
	return np.hstack((data, np.ones((data.shape[0], 1)))) * transform.T

if __name__ == "__main__":

	for demo in sys.argv[1:]:
		process_demo(demo)
