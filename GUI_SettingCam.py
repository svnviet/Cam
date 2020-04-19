from tkinter import *


class SettingCam(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master.title("Setting cam")
        self.pack(fill=BOTH, expand=True)

        self.frame1 = Frame(self)
        self.frame1.pack(fill=X)

        self.lbl1 = Label(self.frame1, text="Counter", width=8)
        self.lbl1.pack(side=LEFT, padx=5, pady=5)

        self.toggle1 = Button(self.frame1, text="On", command=self.convert1)
        self.toggle1.pack(side=RIGHT, padx=10, pady=10)

        self.frame2 = Frame(self)
        self.frame2.pack(fill=X)

        self.lbl2 = Label(self.frame2, text="Recognition", width=10)
        self.lbl2.pack(side=LEFT, padx=5, pady=5)

        self.toggle2 = Button(self.frame2, text="On", command=self.convert2)
        self.toggle2.pack(side=RIGHT, padx=10, pady=10)

        self.frame3 = Frame(self)
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


root = Tk()
root.geometry("300x300+300+300")
app = SettingCam(root)
root.mainloop()
