from tkinter import Tk, Canvas, NW
from tkinter import *
from PIL import Image, ImageTk
import cv2


win = Tk()
cap = cv2.VideoCapture(0)


def show_frames():
    frame = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(frame)

    imgtk = ImageTk.PhotoImage(image=img)
    main_label.imgtk = imgtk
    main_label.configure(image=imgtk)
    main_label.after(60, show_frames)


width = 25
height = 40

arrow_left = ImageTk.PhotoImage(
    Image.open("imgs/arrow_left.png").resize((width, height), Image.ANTIALIAS))

arrow_right = ImageTk.PhotoImage(
    Image.open("imgs/arrow_right.png").resize((width, height), Image.ANTIALIAS))

Label(win, image=arrow_left, width=width,
      height=height).grid(row=0, column=0)
Label(win, image=arrow_right, width=width,
      height=height).grid(row=0, column=2)

main_label = Label(win)
main_label.grid(row=0, column=1)

show_frames()

win.mainloop()
