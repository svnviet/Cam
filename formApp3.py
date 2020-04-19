import PIL
import os
import pickle
import tkinter
from tkinter import *
from tkinter import messagebox, ttk

from PIL.ImageTk import PhotoImage
from PIL import Image, ImageTk
from pystray import MenuItem as item

# ---Face recognize---
import cv2
import of

BASIC_DIR = os.path.abspath(os.path.dirname(__file__))
root = Tk()




class App(Frame):


    def __init__(self, master=None, ):
        tkinter.Frame.__init__(self, master)
        self.master = master
        icon = PhotoImage(file='./icons/icon-small.png')
        master.tk.call('wm', 'iconphoto', master._w, icon)
        self.init_window()
        self.btnAddCam = None
        self.alive = True

    def init_window(self):
        self.master.title('CAM AI')
        self.pack(fill=BOTH, expand=True)
        self.vid = []

        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        # w = (ws - 700)
        # h = (hs - 400)
        self.master.maxsize(1366, 768)
        self.master.minsize(800, 600)
        # self.master.state('zoomed')
        # self.master.geometry('%dx%d+0+0' % (((ws - 200) * 4), ((hs - 100) * 4)))
        self.master.geometry('1366x768+0+0')

        # open video_source (by default this will try to open the computer webcam)
        # self.vid = CounterObject(self.video_source)
        # Top Frame
        self.headerTOP = Frame(self)
        self.headerTOP.pack(fill=X)
        # self.appName = Label(self.headerTOP, text='icons')
        # self.appName.pack(side=TOP, anchor=NW, padx=5)
        # self.buttonSetting = Button(self.headerTOP, text='Setting', command=self.settingApp)
        # self.buttonSetting.pack(side=TOP, anchor=N, padx=5, pady=5)
        #
        # self.addCam = Button(self.headerTOP, text='Add Cam', command=self.addCam)
        # self.addCam.pack(side=TOP)

        self.menuBar = Menu(self.master)
        self.master.config(menu=self.menuBar)

        self.img1 = PhotoImage(file="./icons/Logo.gif")
        self.menuBar.add_cascade(label='Icon', compound='left')

        self.settingMenu = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label="Setting", menu=self.settingMenu)
        # self.settingMenu.add_command(label="Open")
        # self.settingMenu.add_separator()
        # self.settingMenu.add_command(label="Exit")
        self.settingMenu.add_command(label="Setting App", command=self.settingApp)

        self.addcamMenu = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_command(label="Add Cam", command=self.addCam)
        # Main frame
        # Create a canvas that can fit the above video source size
        self.frameCam = Frame(self, width=(ws - 200), height=(hs - 100), bg='gray1')
        self.frameCam.pack(fill=X, side=LEFT, padx=5, pady=2)
        # a.add_cam(0)

        # mảng vị trí sắp xếp
        arrange_cam = [0, 0, 0, 1, 0, 2, 0, 3, 1, 0, 1, 1, 1, 2, 1, 3, 2, 0, 2, 1, 2, 2, 2, 3, 3, 0, 3, 1, 3, 2, 3, 3]
        # mảng trạng thái của các cam
        self.vid = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

        # chọn vị trí cam chạy
        self.vid[1] = MyVideoCapture(0)

        # xét vị trí cam và hiển thị
        for x in range(0, 16):
            camera(self.vid[x - 1], self.frameCam, ws, hs, arrange_cam[x * 2], arrange_cam[(x * 2) + 1])
            # cam1.update()
            # a.add_cam(0)

        self.delay = 10
        # Right Frame

        self.rightFrame = Frame(self, width=200, height=10, borderwidth=1, relief=FLAT)
        self.rightFrame.pack(side=TOP, anchor=NW)

        self.lbListcam = Button(self.rightFrame, text='List Camera', relief=FLAT)
        self.lbListcam.grid(row=0, column=0, sticky=NW)

        self.canvasFrame = Canvas(self, height=100)
        self.listCam = Frame(self.canvasFrame, width=300, height=100, bg='gray1')
        # self.listCam.pack(fill=X, side=TOP, anchor=NW)
        self.scrollBar = Scrollbar(self.canvasFrame, orient='vertical', command=self.canvasFrame.yview)

        self.canvasFrame.configure(yscrollcommand=self.scrollBar.set)
        self.scrollBar.pack(side=RIGHT, fill=Y)
        self.canvasFrame.pack(side=TOP, fill=BOTH, expand=True, anchor=NW)

        self.canvasFrame.create_window((4, 4), window=self.listCam, anchor=NW, tags=self.listCam)
        self.listCam.bind('<Configure>',
                          lambda x: self.canvasFrame.configure(scrollregion=self.canvasFrame.bbox('all')))
        self.listCam.bind('<Down>', lambda x: self.canvasFrame.yview_scroll(3, 'units'))
        self.listCam.bind('<Up>', lambda x: self.canvasFrame.yview_scroll(-3, 'units'))
        self.listCam.bind('<MouseWheel>', lambda x: self.canvasFrame.yview_scroll(int(-1 * (x.delta / 40)), 'units'))
        self.listCam._widgets = []
        rows = 16
        columns = 1
        self.iconDestroyCamRight = PhotoImage(file='./icons/destroyCam64.png')
        for row in range(rows):
            current_row = []
            current_column = []
            for column in range(columns):
                label = tkinter.Label(self.listCam,
                                      borderwidth=0, width=39, height=2)
                label.grid(row=row + 1, column=column, sticky="nsew", padx=1, pady=1)

                btn = tkinter.Button(self.listCam, text='X', borderwidth=0, width=34, height=2,
                                     image=self.iconDestroyCamRight)
                btn.grid(row=row + 1, column=column + 1, sticky='nsew', padx=1, pady=1)
                current_row.append(label)
                current_column.append(btn)
            self.listCam._widgets.append(current_row)
        for column in range(columns):
            self.listCam.grid_columnconfigure(column, weight=1)
        # self.scroll = Scrollbar(self.rightFrame)
        # self.scroll.pack(side=RIGHT, fill=Y)
        # ---bottom rightFrame---

        self.bottomRightFrame = Frame(self, width=200, height=400, relief=RIDGE, bg='gray60', borderwidth=1)
        self.bottomRightFrame.pack(side=TOP, padx=2, pady=2, fill=X)

        self.lblShowInfoCam = Label(self.bottomRightFrame, text='Thông tin chi tiết :')
        self.lblShowInfoCam.pack(side=TOP, anchor=NW)

        # Bottom frame
        self.Bottom = tkinter.Frame(width=ws, height=80, bg='light grey')
        self.Bottom.pack(side=BOTTOM)

        # -------------------------------

    def run(self):
        self.update()

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

    def addCam(self):
        if self.btnAddCam == None or not tkinter.Toplevel.winfo_exists(self.btnAddCam):
            self.btnAddCam = tkinter.Toplevel(self.master)

            self.master.title("Add cam")
            self.pack(fill=BOTH, expand=True)

            self.frame1 = Frame(self.btnAddCam, self)
            self.frame1.pack(fill=X)

            self.lbl1 = Label(self.frame1, text="IP", width=8)
            self.lbl1.pack(side=LEFT, padx=5, pady=5)

            self.entry1 = Entry(self.frame1)
            self.entry1.pack(fill=X, padx=5, expand=True)

            self.frame2 = Frame(self.btnAddCam, self)
            self.frame2.pack(fill=X)

            self.lbl2 = Label(self.frame2, text="Account", width=8)
            self.lbl2.pack(side=LEFT, padx=5, pady=5)

            self.entry2 = Entry(self.frame2)
            self.entry2.pack(fill=X, padx=5, expand=True)

            self.frame3 = Frame(self.btnAddCam, self)
            self.frame3.pack(fill=X)

            self.lbl3 = Label(self.frame3, text="Password", width=8)
            self.lbl3.pack(side=LEFT, padx=5, pady=5)

            self.entry3 = Entry(self.frame3)
            self.entry3.pack(fill=X, padx=5, expand=True)

            self.saveButton = Button(self.btnAddCam, text="Save", command=self.addCamToFame)
            self.saveButton.pack(side=RIGHT, padx=5, pady=5)



            self.alive = True
            self.readdCam()

    def readdCam(self):
        if self.alive == True and tkinter.Toplevel.winfo_exists(self.btnAddCam):
            pass
        else:
            self.alive = False
    # def addCamToFame(self):
    #     cameraIP = self.entry1.get()
    #     if cameraIP == '0':
    #         messagebox.showinfo('Succu', 'You have conected to Camera Ip : ' + self.entry1.get())
    #         MyVideoCapture.get_frame()
    def addCamToFame(self):
        cameraip = int(self.entry1.get())
        cap = cv2.VideoCapture(cameraip)
        if not cap.isOpened():
            raise IOError("Cannot open webcam")

        while True:
            ret, self.webCam = cap.read()
            # self.Cam1 = cv2.resize(self.Cam1, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            cv2.imshow('Input', self.webCam)

            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def messagebox(self):
        pass

    # def update(self):
    #     print("update")
    #     # Get a frame from the video source
    #     frame_image = []
    #     for x in range(0, len(self.vid)):
    #         ret, frame = self.vid[x].get_frame()
    #         frame_image.append(frame)
    #         # print("frame_image : " + str(len(frame_image)))
    #
    #     self.photo = []
    #     for x in range(0, len(frame_image)):
    #         self.photo.append(PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame_image[x])))
    #         self.Cam1.create_image(x * 320, 0, image=self.photo[x], anchor=tkinter.NW)
    #
    #     self.master.after(10, self.update)

    def settingApp(self):
        btnSettingApp = tkinter.Toplevel(self)
        self.master.title("Setting cam")
        self.pack(fill=BOTH, expand=True)

        self.frame1 = Frame(btnSettingApp, self)
        self.frame1.pack(fill=X)

        self.lbl1 = Label(self.frame1, text="Counter", width=8)
        self.lbl1.pack(side=LEFT, padx=5, pady=5)

        self.toggle1 = Button(self.frame1, text="On", command=self.convert1)
        self.toggle1.pack(side=RIGHT, padx=10, pady=10)

        self.frame2 = Frame(btnSettingApp, self)
        self.frame2.pack(fill=X)

        self.lbl2 = Label(self.frame2, text="Recognition", width=10)
        self.lbl2.pack(side=LEFT, padx=5, pady=5)

        self.toggle2 = Button(self.frame2, text="On", command=self.convert2)
        self.toggle2.pack(side=RIGHT, padx=10, pady=10)

        self.frame3 = Frame(btnSettingApp, self)
        self.frame3.pack(fill=X)

        self.toggle3 = Button(self.frame3, text="Close cam")
        self.toggle3.pack(side=RIGHT, padx=10, pady=10)

    def convert1(self, tog=[0]):

        tog[0] = not tog[0]
        if tog[0]:
            self.toggle1.config(text='On')
        else:
            self.toggle1.config(text='Off')

    def convert2(self, tog=[0]):

        tog[0] = not tog[0]
        if tog[0]:
            self.toggle2.config(text='On')
        else:
            self.toggle2.config(text='Off')

    def on_quitCam(self):
        self.quit()

class MyVideoCapture:

    def __init__(self, cameraIP):
        # Open the video source
        self.vid = cv2.VideoCapture(cameraIP)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", cameraIP)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            # frame = of.face.recognizeface(labels, face_cascade, recognizer, detector, frame)
            if ret:
                frame = cv2.cv2.resize(frame, (320, 270))
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


# Create a window and pass it to the Application object
face_cascade = cv2.CascadeClassifier('library/cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face_LBPHFaceRecognizer.create()
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer.read("recognizers/face-trainner.yml")

labels = {"person_name": 1}
with open("pickles/face-labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}


class camera:
    def __init__(self, vid, frameCam, ws, hs, x, y):
        self.frameCam = frameCam
        self.ws = ws
        self.hs = hs
        self.vid = vid
        self.cam = tkinter.Canvas(self.frameCam, width=((ws - 780) / 4), height=((hs - 100) / 4), bg='gray50')
        if vid != None:
            self.update()

        # self.cam.mainloop()
        # --tao menu popup---
        self.iconShowCam = PhotoImage(file='./icons/showCam.png')
        self.iconSettingCam = PhotoImage(file='./icons/settingCam.png')
        self.iconOff = PhotoImage(file='./icons/off-icon.png')
        self.iconAddCam = PhotoImage(file='./icons/on-addCam.png')
        menuCam = Menu(self.cam, tearoff=0)
        menuCam.add_command(label='Add Cam', command=lambda: self.settingApp('Add_Cam'), underline=0, compound='left',
                            image=self.iconAddCam)
        menuCam.add_command(label='Show', underline=0, command=lambda: self.settingApp('Show'), compound='left',
                            image=self.iconShowCam)
        menuCam.add_command(label='Nhận diện khuôn mặt', command=lambda :self.settingApp('Nhận diện khuôn mặt'),compound='left',
                            image=self.iconOff
                            , accelerator='Off')
        menuCam.add_command(label='Đếm số lượng người', command=lambda :self.settingApp('Đếm số lượng người'), compound=LEFT,
                            image=self.iconOff, accelerator='Off')
        menuCam.add_command(label='Nhận Diện Biển số xe ', command=lambda: self.settingApp('Setting'), underline=0, compound='left',
                            image=self.iconOff, accelerator='Off')
        menuCam.add_command(label='Destroy Cam', command=lambda: self.settingApp('Destroy_Cam'), underline=0,
                            compound='left', image=self.iconOff)

        def popup(event):
            menuCam.post(event.x_root, event.y_root)

        self.cam.bind('<Button-3>', popup)
        self.cam.grid(row=x, column=y)

    def settingApp(event, method):
        if method == 'Add_Cam':
            pass
            print('Add_Cam')
        elif method == 'Show':
            pass
            print('Show')
        elif method == 'Setting':
            pass
            print('Setting')
        elif method == 'Destroy_Cam':
            pass
            print('Destroy_Cam')

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.cam.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.cam.after(10, self.update)


def on_closing():
    if messagebox.askokcancel('Quit', 'Do you want to quit?'):
        root.destroy()


root.protocol('WM_DELETE_WINDOW', on_closing)
app = App(root)
root.mainloop()
