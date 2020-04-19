from tkinter import *

root = Tk()

canvas = Canvas(root, height=200)
frame = Frame(canvas, bg='gray1')

scrollbar = Scrollbar(root, orient='vertical', command=canvas.yview)

canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

canvas.create_window((4, 4,), window=frame, anchor=NW, tags=frame)
frame.bind('<Configure>', lambda x: canvas.configure(scrollregion=canvas.bbox('all')))
root.bind(('<Down>'), lambda x: canvas.yview_scroll(3, 'units'))
root.bind(('<Up>'), lambda x: canvas.yview_scroll(-3, 'units'))

root.bind('<MouseWheel>', lambda x: canvas.yview_scroll(int(-1 * (x.delta / 40)), 'units'))
frame._widgets = []
rows = 16
columns = 1
iconDestroyCamRight = PhotoImage(file='./icons/destroyCam64.png')
for row in range(rows):
    current_row = []
    current_column = []
    for column in range(columns):
        label = Label(frame, text="Ip cam",
                      borderwidth=0, width=39, height=2)
        label.grid(row=row + 1, column=column, sticky="nsew", padx=1, pady=1)

        btn = Button(frame, text='X', borderwidth=0, width=34, height=2,
                     image=iconDestroyCamRight)
        btn.grid(row=row + 1, column=column + 1, sticky='nsew', padx=1, pady=1)
        current_row.append(label)
        current_column.append(btn)
    frame._widgets.append(current_row)
for column in range(columns):
    frame.grid_columnconfigure(column, weight=1)

root.mainloop()
