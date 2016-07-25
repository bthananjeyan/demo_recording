import numpy as np
import h5py
import sys

def process_demo(demo_directory):
    # Load data
    with h5py.File("../" + demo_directory + '/data.h5','r') as hf:
        psm1_sync = np.matrix(hf.get('psm1_sync'))
        psm2_sync = np.matrix(hf.get('psm2_sync'))
        transform = np.matrix(hf.get('camera_to_robot'))

        # Uncomment when ready
        # psm1_transform = np.matrix(hf.get('camera_to_psm1'))
        # psm2_transform = np.matrix(hf.get('camera_to_psm2'))
        # psm1_invtransform = invert_rigid_transformation(psm1_transform)
        # psm2_invtransform = invert_rigid_transformation(psm2_transform)


    invtransform = np.zeros(transform.shape)
    invtransform[:3,:3] = transform[:3,:3].T
    invtransform[:,3] = -tranform[:,3]

    # Delete when ready
    psm1_invtransform = invtransform
    psm2_invtransform = invtransform


    # Fix times
    time = psm1_sync[:,0]
    temp = np.ones((psm1_sync.shape[0],1)) * psm1_sync[0,0]
    psm1_sync[:,0] -= temp
    psm2_sync[:,0] -= temp
    # Throw out bad features
    good_features = np.r_[0:psm1_sync.shape[1]]
    psm1_sync = psm1_sync[:, good_features]
    psm2_sync = psm2_sync[:, good_features]
    # Transform position
    psm1_sync[:,1:4] = transform_matrix(psm1_sync[:,1:4], psm1_invtransform)
    psm2_sync[:,1:4] = transform_matrix(psm2_sync[:,1:4], psm2_invtransform)
    # Featurize images
    left_end, right_end = featurize_images(demo_directory, time)
    demo_data = np.hstack((psm1_sync, psm2_sync, left_end, right_end))
    # Write processed data
    with h5py.File("../" + demo_directory + '/demo.h5','w') as hf:
        hf.create_dataset('demo_data', data=demo_data)
        hf.create_dataset('camera_to_robot', data=transform)
        hf.create_dataset('robot_to_camera', data=invtransform)

        # Uncomment When Ready
        # hf.create_dataset('psm1_transform', data=psm1_transform)
        # hf.create_dataset('psm2_transform', data=psm2_transform)

    return demo_data

def invert_rigid_transformation(transform):
    invtransform = np.zeros(transform.shape)
    invtransform[:3,:3] = transform[:3,:3].T
    invtransform[:,3] = -tranform[:,3]
    return invtransform

def transform_matrix(data, transform):
    return np.hstack((data, np.ones((data.shape[0], 1)))) * transform.T

def featurize_images(demo_directory, t):
    t = np.ravel(t).tolist()
    lst1 = []
    for time in t:
        img = np.array(cv2.imread("../" + demo_directory + "/left_endoscope/" + str(time) + ".jpg"))
        lst1.append(featurize_image(img))
    lst2 = []
    for time in t:
        img = np.array(cv2.imread("../" + demo_directory + "/right_endoscope/" + str(time) + ".jpg"))
        lst2.append(featurize_image(img))
    return np.matrix(lst1), np.matrix(lst2)

def featurize_image(img):
    return [1, 1, 1]


if __name__ == "__main__":

    for demo in sys.argv[1:]:
        process_demo(demo)
