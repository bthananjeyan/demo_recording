import Tkinter
from Tkinter import *
import pickle, time
from multiprocessing import Process
import os
from robot import *
import numpy as np
from ImageSubscriber import ImageSubscriber
import scipy
import sys
import multiprocessing
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats

current_force_capacitor_value = np.array([1., 0.], dtype=np.float32)

def force_callback(msg):

    current_force_capacitor_value =  msg.data
    print(current_force_capacitor_value)

def startCallback():
    global record_process, exit
    print "start"
    if record_process != None:
        print "You are already recording"
        return
    if exit.is_set():
        exit.clear()
    record_process=Process(target=start_listening,args=(exit,))
    record_process.start()

def stopCallback():
    global record_process,exit
    print "stop"
    if record_process == None:
        print " Nothing currently recording"
        return
    exit.set()
    record_process.terminate()
    record_process.join()
    record_process = None


def exitCallback():
    global record_process,exit
    print "exit"
    if record_process != None:
        exit.set()
        record_process.terminate()
        record_process.join()
        
    top.destroy()
    sys.exit()

def dump_image_dict(d):
    for key in d.keys():
        scipy.misc.imsave(str(key), d[key])


def start_listening(exit, interval=.04):
    directory = E.get()
    directory = "../" + directory
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
    with open("camera_to_robot.p", "rb") as f:
        cmat = pickle.load(f)
    with open(directory + "/camera_to_robot.p", "w+") as f:
        pickle.dump(cmat, f)

    rospy.Subscriber("/force/capsense", numpy_msg(Floats), force_callback, queue_size=1)

    time.sleep(2)
    count = 0
    
    left_images = {}
    right_images = {}

    f = open(directory + "/psm1_sync.p", "a")
    f2 = open(directory + "/psm2_sync.p", "a")

    while not exit.is_set():

        now = rospy.get_rostime()
        now = int((now.secs + now.nsecs/1e9) * 1e3) # in milliseconds

        left = imgsub.left_image
        right = imgsub.right_image

        
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
        one = [now] + list(pos1) + rot1 + list(grip1) + list(joint1) + list(masterpose1) + list(masterjoint1) + list(current_force_capacitor_value)
        two = [now] + list(pos2) + rot2 + list(grip2) + list(joint2) + list(masterpose2) + list(masterjoint2) + list(current_force_capacitor_value)


        left_images[directory + "/left_endoscope/" + str(now) + '.jpg'] = left
        right_images[directory + "/right_endoscope/" + str(now) + ".jpg"] = right
        print len(left_images.keys())
        if len(left_images.keys()) >= 100:
            l = Process(target=dump_image_dict, args=(left_images,))
            l.start()
            r = Process(target=dump_image_dict, args=(right_images,))
            r.start()
            left_images = {}
            right_images ={}

        pickle.dump(one, f)
        pickle.dump(two, f2)
        time.sleep(interval)
    l = Process(target=dump_image_dict, args=(left_images,))
    l.start()
    r = Process(target=dump_image_dict, args=(right_images,))
    r.start()
        
        

if __name__ == '__main__':


    exit=multiprocessing.Event()
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

