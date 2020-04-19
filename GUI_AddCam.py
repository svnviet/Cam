from tkinter import *


class AddCam(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master.title("Add cam")
        self.grid()

        self.frame1 = Frame(self)
        self.frame1.pack(fill=X)

        self.lbl1 = Label(self.frame1, text="IP", width=8)
        self.lbl1.pack(side=LEFT, padx=5, pady=5)

        self.entry1 = Entry(self.frame1)
        self.entry1.pack(fill=X, padx=5, expand=True)

        self.frame2 = Frame(self)
        self.frame2.pack(fill=X)

        self.lbl2 = Label(self.frame2, text="Account", width=8)
        self.lbl2.pack(side=LEFT, padx=5, pady=5)

        self.entry2 = Entry(self.frame2)
        self.entry2.pack(fill=X, padx=5, expand=True)

        self.frame3 = Frame(self)
        self.frame3.pack(fill=X)

        self.lbl3 = Label(self.frame3, text="Password", width=8)
        self.lbl3.pack(side=LEFT, padx=5, pady=5)

        self.entry3 = Entry(self.frame3)
        self.entry3.pack(fill=X, padx=5, expand=True)

        self.saveButton = Button(self, text="Save")
        self.saveButton.pack(side=RIGHT, padx=5, pady=5)


root = Tk()
root.geometry("300x300+300+300")
app = AddCam(root)
root.mainloop()
