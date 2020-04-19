# -------import package of PythonGui---------
import time
import tkinter
from tkinter import *
# --------import package of RecognitionFace-----------#
import PIL.Image
import PIL.ImageTk
import cv2
import os
import pickle
# --------import package of ObjectTracker---------#
from imutils.video import FPS
import numpy as np
import imutils
import time
import dlib
import argparse

# --------------
import ofRecogintion
# import PeopleCounter
from iiiTrackerObject.centroidtracker import CentroidTracker
from iiiTrackerObject.trackableobject import TrackableObject

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Create a recognition on the Application object
face_cascade = cv2.CascadeClassifier('library/cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face_LBPHFaceRecognizer.create()
detector = cv2.CascadeClassifier('library/cascades/data/haarcascade_frontalface_default.xml')
recognizer.read("recognizers/face-trainner.yml")
labels = {"person_name": 1}
with open("pickles/face-labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}

# Create a ObjectTracker on the Application object
# ap = argparse.ArgumentParser()
# ap.add_argument('-c', '--condifidence', type=float, default=0.2, help='minimum probability to filter weak detections')
# ap.add_argument('-s', '--skips-frames', type=int, default=50, help='# of skip frames between detections')
# args = vars(ap.parse_args())
# CLASSES = ['background', ' aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair',
#            'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train',
#            'tymonitor']
# print('[INFO]loading model...')
# prototxtPath = os.path.join(BASE_DIR, 'library/MobileNetSSD_deploy.prototxt')
# modelPath = os.path.join(BASE_DIR, 'library/MobileNetSSD_deploy.caffemodel')
# net = cv2.dnn.readNetFromCaffe(prototxtPath, modelPath)
# print('LOADING CAMERA .......')


class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        icon = PhotoImage(file='icons/Logo.gif')
        window.tk.call('wm', 'iconphoto', window._w, icon)
        ws = window.winfo_screenwidth()
        hs = window.winfo_screenheight()
        w = (ws - 700)
        h = (hs - 400)
        window.minsize(1280, 840)
        window.geometry('%dx%d+100+100' % (w, h))

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
        # self.vid = CounterObject(self.video_source)
        # Create a form template

        # Top Frame
        self.headerTop = tkinter.Frame(window, width=ws, bg='light grey', height=60)
        self.headerTop.pack(side=TOP)

        # Left Frame
        self.headerRight = tkinter.Frame(window, width=200, height=hs, bg='gray30')
        self.headerRight.pack(side=RIGHT)

        # Main frame
        # Create a canvas that can fit the above video source size
        self.frameCam1 = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.frameCam1.pack(side=TOP, anchor=NW)

        # # Button that lets the user take a snapshot
        self.btn_snapshot = tkinter.Button(window, text="chụp", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
        #

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 10
        self.update()

        # Bottom frame
        self.Bottom = tkinter.Frame(width=ws, height=1, bg='light grey')
        tkinter.Button(window, text='Turn On Counter People', width=20, height=3, command=self.counterPeople).pack(
            side=BOTTOM, anchor=NW, ipadx=10)
        tkinter.Button(window, text='Turn On Recognition Faces', width=20, height=3).pack(side=BOTTOM, anchor=NW,
                                                                                          ipadx=10)
        self.Bottom.pack(side=BOTTOM)
        # -------------------------------
        self.window.mainloop()

    def counterPeople(self):
        pass

    def recognitionface(self):
        pass

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.frameCam1.create_image(0, 0, image=self.photo, anchor=NW)

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            frame = ofRecogintion.face.recognizeface(self, labels, face_cascade, recognizer, detector, frame)
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


class CounterObject:
    ct = CentroidTracker(maxDisappeared=50, maxDistance=50)
    trackers = []
    trackersObjects = []
    label = []
    totalFrames = 0
    totalDown = 0
    totalUp = 0
    fps = FPS().start()
    time.sleep(2)
    writer = None

    def __init__(self, video_source=0):
        # Open video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError('Unable to open video suorce', video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, framePeopleCounter = self.vid.read()


# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")
