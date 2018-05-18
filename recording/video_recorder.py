from multiprocessing import Process, Queue
import cv2
import time
import Tkinter
from Tkinter import *
class _Camera(Process):

    def __init__(self, camera, cmd_q, res, codec, fps):
        Process.__init__(self)
        
        self.res = res
        self.fps = fps

        self.camera = camera
        self.fourcc = cv2.cv.CV_FOURCC(*codec)
        
        self.cmd_q = cmd_q
        self.recording = False
        self.out = None
        
    def run(self):
        while True:
            if not self.cmd_q.empty():
                cmd = self.cmd_q.get()
                if cmd[0] == 'stop':
                    self.out.release()
                    self.recording = False
                elif cmd[0] == 'start':
                    filename = cmd[1]
                    self.out = cv2.VideoWriter(filename, self.fourcc, self.fps, self.res)
                    self.recording = True
                    
            if self.recording:
                ret_val, frame = self.camera.read()
                print 'reading'
                
                if ret_val:
                    self.out.write(frame)
                    cv2.imshow('frame',frame)
                    cv2.waitKey(1)

class VideoRecorder:

    def __init__(self, device_id=0, res=(640, 480), codec='XVID', fps=30):
        '''
        Create video recorder object.
        
        Args:
            device_id: index of device
            res: resolution of recording and saving. defaults to (640, 480)
            codec: codec used for encoding video. default to XVID. 
            fps: fps of vide captures. defaults to 30
        '''
        self._res = res
        self._codec = codec
        self._fps = fps
        
        self._cmd_q = Queue()
        
        self._actual_camera = None
        self._actual_camera = cv2.VideoCapture(device_id)
        
        self._recording = False
        self._started = False
        
    def start(self):
        self._started = True
        self._camera = _Camera(self._actual_camera, self._cmd_q, self._res, self._codec, self._fps)
        self._camera.start()

    def start_recording(self):
        if not self._started:
            raise Exception("Must start the video recorder first by calling .start()!")
        if self._recording:
            raise Exception("Cannot record a video while one is already recording!")
        self._recording = True
        self._cmd_q.put(('start', E.get()))
        
    def stop_recording(self):
        if not self._recording:
            raise Exception("Cannot stop a video recording when it's not recording!")
        self._cmd_q.put(('stop',))
        self._recording = False

    def stop(self):
        if not self._started:
            raise Exception("Cannot stop a video recorder before starting it!")
        self._started = False
        #self._actual_camera.release()
        self._camera.terminate()
        cv2.destroyAllWindows()
        sys.exit()

if __name__ == "__main__":
    vr=VideoRecorder()
    vr.start()
    top = Tkinter.Tk()
    top.title('Video Camera')
    top.geometry('400x200')


    B = Tkinter.Button(top, text="Start Recording", command = vr.start_recording)
    C = Tkinter.Button(top, text="Stop Recording", command = vr.stop_recording)
    D = Tkinter.Button(top, text="Exit", command = vr.stop)
    E = Entry(top)


    B.pack()
    C.pack()
    D.pack()
    E.pack()

    E.delete(0, END)
    E.insert(0, "test.avi")

    top.mainloop()
