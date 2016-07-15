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

def startCallback():
    global record_process
    if record_process != None:
        print "You are already recording"
        return
    start_listening()

def stopCallback():
    global record_process
    if record_process == None:
        print "Nothing currently recording"
        return
    record_process.terminate()
    record_process = None


def exitCallback():
    global record_process
    if record_process != None:
        record_process.terminate()
    top.destroy()
    sys.exit()


def start_listening(interval=.01):
    directory = E.get()
    if not os.path.exists(directory):
        os.makedirs(directory)
        os.makedirs(directory + "/left_endoscope")
        os.makedirs(directory + "/right_endoscope")

    imgsub = ImageSubscriber()
    time.sleep(4)
    count = 0

    while True:
        now = rospy.get_rostime()
        scipy.misc.imsave(directory + "/left_endoscope/" + str(now) + '.jpg', imgsub.left_image)
        scipy.misc.imsave(directory + "/right_endoscope/" + str(now) + '.jpg', imgsub.right_image)
        count += 1
        time.sleep(interval)

if __name__ == '__main__':

    psm1 = robot("PSM1")
    psm2 = robot("PSM2")

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

