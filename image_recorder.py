import Tkinter
from Tkinter import *
import pickle, time
from multiprocessing import Process
import os
from robot import *
import numpy as np
import IPython
from ImageSubscriber import ImageSubscriber
import scipy
import matplotlib.pyplot as plt
import sys

def startCallback():
    global record_process
    print "start"
    if record_process != None:
        print "You are already recording"
        return
    record_process=Process(target=start_listening)
    record_process.start()

def stopCallback():
    global record_process
    print "stop"
    if record_process == None:
        print " Nothing currently recording"
        return
    record_process.terminate()
    record_process = None


def exitCallback():
    global record_process
    print "exit"
    if record_process != None:
        record_process.terminate()
    top.destroy()
    sys.exit()

def dump_image_dict(d):
    for key in d.keys():
        scipy.misc.imsave(key, d[key])


def start_listening(interval=.01):
    directory = E.get()
    if not os.path.exists(directory):
        os.makedirs(directory)
        os.makedirs(directory + "/left_endoscope")
        os.makedirs(directory + "/right_endoscope")
    open(directory + "/psm1_sync.p", "w+").close()
    open(directory + "/psm2_sync.p", "w+").close()
    open(directory + "/camera_info.p", "w+").close()

    psm1 = robot("PSM1")
    psm2 = robot("PSM2")

    imgsub = ImageSubscriber()

    imgsub.dump_camera_info(directory + "/camera_info.p")
    f = open("camera_to_robot.p", "rb")
    cmat = pickle.load(f)
    f.close()
    f = open(directory + "/camera_to_robot.p", "w+")
    pickle.dump(cmat, f)
    f.close()


    time.sleep(4)
    count = 0
    
    left_images = {}
    right_images = {}

    while True:

        now = rospy.get_rostime()
        now = now.secs + now.nsecs/1e9

        left = imgsub.left_image
        right = imgsub.right_image

        f = open(directory + "/psm1_sync.p", "a")
        f2 = open(directory + "/psm2_sync.p", "a")
        pose1 = psm1.get_current_cartesian_position()
        pose2 = psm2.get_current_cartesian_position()
        pos1 = pose1.position
        pos2 = pose2.position
        rot1 = [pose1.tb_angles.yaw_deg, pose1.tb_angles.pitch_deg, pose1.tb_angles.roll_deg]
        rot2 = [pose2.tb_angles.yaw_deg, pose2.tb_angles.pitch_deg, pose2.tb_angles.roll_deg]
        joint1 = psm1.get_current_joint_position()
        joint2 = psm2.get_current_joint_position()
        masterpose1 = psm1.get_master_position_cartesian_current()
        masterpose2 = psm1.get_master_position_cartesian_current()
        masterjoint1 = psm1.get_master_joint_current()
        masterjoint2 = psm1.get_master_joint_current()
        grip1 = [joint1[-1] * 180 / np.pi]
        grip2 = [joint2[-1] * 180 / np.pi]
        one = [now] + list(pos1) + rot1 + list(grip1) + list(joint1) + list(masterpose1) + list(masterjoint1)
        two = [now] + list(pos2) + rot2 + list(grip2) + list(joint2) + list(masterpose2) + list(masterjoint2)

        left_images[directory + "/left_endoscope/" + str(now) + '.jpg'] = left
        right_images[directory + "/right_endoscope/" + str(now) + "jpg"] = right

        if len(left_images.keys()) > 300:
            dump_image_dict(left_images)
            dump_image_dict(right_images)
            left_images = {}
            right_images ={}

        pickle.dump(one, f)
        pickle.dump(two, f2)

        time.sleep(interval)

if __name__ == '__main__':



    directory = "default"
    record_process = None

    top = Tkinter.Tk()
    top.title('Image Recorder')
    top.geometry('400x200')


    B = Tkinter.Button(top, text="Start Recording", command = startCallback)
    C = Tkinter.Button(top, text="Stop Recording", command = stopCallback)
    D = Tkinter.Button(top, text="Exit", command = exitCallback)
    E = Entry(top)


    B.pack()
    C.pack()
    D.pack()
    E.pack()

    E.delete(0, END)
    E.insert(0, "default")

    top.mainloop()

