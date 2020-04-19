# import pickle
# import cv2
# import pandas as pandas
# from datetime import datetime
# from utils import CFEVideoConf, image_resize



# a = [1,5,6,7,3,8,9,2,4,0]

# def sort(in_put,low,hight):
#     m=0
#     n=len(in_put)-1
#     c=int(len(in_put)/2-1)
#     print(in_put[m])
#     while True:
#         # print(in_put[m])
#         if in_put[m] >= in_put[c]:
#             # print(in_put[m])
#             while True:
#                 if in_put[n] <= in_put[c]:
#                     d = in_put[n]
#                     in_put[n]=in_put[m]
#                     in_put[m]=d
#                     break
#                 n = n - 1
#                 if m>=n:
#                     break
#         m = m + 1
#         if m>=n:
#             # sort(intput[2:])
#             # sort(intput[2:])
#             print(m,n)
#             break
# sorl(a)
# print(a)

# b = [1,1,2,1,3,1,4,1,5,1, 1,2,2,2,3,2,4,2,5,2]
# a = [5,2, 4,2, 3,2, 2,2, 1,2, 5,1, 4,1, 3,1, 2,1, 1,1]
# print(a)
# # x=20
# # while x > 0:
# #     a.append(x)
# #     x=x-1
# # print(a)

# def selec_sort_local(int_put):
#     count=0
#     complete=bool(0)
#     bool

#     # sắp xếp theo trục Y
#     while True:

#         while count<int(len(int_put)-2):
                
#             if int_put[count+1]>int_put[count+3]:

#                 int_put[count]    = int_put[count]  + int_put[count+2]
#                 int_put[count+2]  = int_put[count]  - int_put[count+2]
#                 int_put[count]    = int_put[count]  - int_put[count+2]

#                 int_put[count+1]    = int_put[count+1]  + int_put[count+3]
#                 int_put[count+3]    = int_put[count+1]  - int_put[count+3]
#                 int_put[count+1]    = int_put[count+1]  - int_put[count+3]

#                 complete = 1

#             count=count+2
#         if complete==0:
#             break
#         else:
#             count=0
#             complete=0

#     count=0
#     complete=bool(0)

#     # sắp xếp theo trục X
#     while True:

#         while count<int(len(int_put)-2):
                
#             if int_put[count]>int_put[count+2]:
#                 int_put[count]    = int_put[count]  + int_put[count+2]
#                 int_put[count+2]  = int_put[count]  - int_put[count+2]
#                 int_put[count]    = int_put[count]  - int_put[count+2]

#                 int_put[count+1]  = int_put[count+1]  + int_put[count+3]
#                 int_put[count+3]  = int_put[count+1]  - int_put[count+3]
#                 int_put[count+1]  = int_put[count+1]  - int_put[count+3]

#                 complete = 1

#             count=count+2
#         if complete==0:
#             break
#         else:
#             count=0
#             complete=0
       
# selec_sort_local(a)
# print(a)
# print(b)

# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.stats import truncnorm
# def truncated_normal(mean=0, sd=1, low=0, upp=10):
#     return truncnorm(
#         (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)
# class NeuralNetwork:
    
#     def __init__(self, 
#                  no_of_in_nodes, 
#                  no_of_out_nodes, 
#                  no_of_hidden_nodes,
#                  learning_rate):
#         self.no_of_in_nodes = no_of_in_nodes
#         self.no_of_out_nodes = no_of_out_nodes 
#         self.no_of_hidden_nodes = no_of_hidden_nodes
#         self.learning_rate = learning_rate  
#         self.create_weight_matrices()   
    

#     def create_weight_matrices(self):
#         rad = 1 / np.sqrt(self.no_of_in_nodes)
#         X = truncated_normal(mean=0, sd=1, low=-rad, upp=rad)
#         self.weights_in_hidden = X.rvs((self.no_of_hidden_nodes, 
#                                        self.no_of_in_nodes))
#         rad = 1 / np.sqrt(self.no_of_hidden_nodes)
#         X = truncated_normal(mean=0, sd=1, low=-rad, upp=rad)
#         self.weights_hidden_out = X.rvs((self.no_of_out_nodes, 
#                                         self.no_of_hidden_nodes))
             
    
#     def train(self):
#         pass
    
#     def run(self):
#         pass
    
    
# if __name__ == "__main__":
#     simple_network = NeuralNetwork(no_of_in_nodes = 3, 
#                                    no_of_out_nodes = 2, 
#                                    no_of_hidden_nodes = 4,
#                                    learning_rate = 0.1)
#     print(simple_network.weights_in_hidden)
#     print(simple_network.weights_hidden_out)
# [[ 0.10607641 -0.05716482  0.55752363]
#  [ 0.33701589  0.05461437  0.5521666 ]
#  [ 0.11990863 -0.29320233 -0.43600856]
#  [-0.18218775 -0.20794852 -0.39419628]]
# [[  4.82634085e-04  -4.97611184e-01  -3.25708215e-01  -2.61086173e-01]
#  [ -2.04995922e-01  -7.08439635e-02   2.66347839e-01   4.87601670e-01]]


import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import of
import pickle


class App:
    print("App")

    def __init__(self, window, window_title, video_source):
        print("__init__App")
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="chụp", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
        # self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        print("update")
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    print("MyVideoCapture")

    def __init__(self, video_source=0):
        print("__init__MyVideoCapture")
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        print("get_frame")
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            frame = of.face.recognizeface(labels, face_cascade, recognizer, detector, frame)
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        print("__del__")
        if self.vid.isOpened():
            self.vid.release()


# Create a window and pass it to the Application object
face_cascade = cv2.CascadeClassifier('library/cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face_LBPHFaceRecognizer.create()
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer.read("recognizers/face-trainner.yml")

labels = {"person_name": 1}
with open("pickles/face-labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}

App(tkinter.Tk(), "Tkinter and OpenCV", 0)
tkinter.mainloop()
# App(tkinter.Tk(), "Tkinter and OpenCV", 1)
