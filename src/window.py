from tkinter import Tk, Canvas, NW
from tkinter import *
from PIL import Image, ImageTk
import cv2
import effects
import os


def show_frames(frames_label, cap, effects_manager):
    frame = cap.read()[1]

    frame_with_effect = cv2.cvtColor(
        effects_manager.apply_effect(frame), cv2.COLOR_BGR2RGBA)

    img = Image.fromarray(frame_with_effect)

    imgtk = ImageTk.PhotoImage(image=img)
    frames_label.imgtk = imgtk
    frames_label.configure(image=imgtk)
    frames_label.grid(row=0, column=1)
    frames_label.after(60, lambda: show_frames(
        frames_label, cap, effects_manager))
    return frames_label


def move(e, label):
    label.config(text=f"Coordinates: x:{e.x} y:{e.y}")


def main():
    root = Tk()

    # Video
    cap = cv2.VideoCapture(0)
    effects_manager = effects.EffectsManager()
    frames_label = show_frames(Label(root), cap, effects_manager)

    # Buttons
    width = 25
    height = 40

    arrow_left = ImageTk.PhotoImage(
        Image.open("imgs/arrow_left.png").resize((width, height), Image.ANTIALIAS))

    arrow_right = ImageTk.PhotoImage(
        Image.open("imgs/arrow_right.png").resize((width, height), Image.ANTIALIAS))

    Button(root, image=arrow_left, width=width + 25,
           height=height, borderwidth=0, command=effects_manager.previous_effect).grid(row=0, column=0)
    Button(root, image=arrow_right, width=width + 25,
           height=height, borderwidth=0, command=effects_manager.next_effect).grid(row=0, column=2)

    # Stickers
    sticker_paths = os.listdir("imgs/stickers")
    stickers_qty = len(sticker_paths)

    stickers_bar = Frame(root)
    stickers_bar.grid(row=2, columnspan=stickers_qty)

    stickers_canvas = Canvas(stickers_bar, height=80, width=600)
    stickers_canvas.grid(row=2, columnspan=stickers_qty)

    scroll_bar = Scrollbar(stickers_bar, orient=HORIZONTAL,
                           command=stickers_canvas.xview)
    scroll_bar.grid(row=1, columnspan=stickers_qty, sticky=E+W)

    stickers_canvas.configure(xscrollcommand=scroll_bar.set)
    stickers_canvas.bind('<Configure>', lambda e: stickers_canvas.configure(
        scrollregion=stickers_canvas.bbox("all")))

    aux_frame = Frame(stickers_bar)
    stickers_canvas.create_window((0, 0), window=aux_frame)

    for i in range(stickers_qty):
        sticker_image = ImageTk.PhotoImage(
            Image.open(f"imgs/stickers/{sticker_paths[i]}").resize((80, 80), Image.ANTIALIAS))

        sticker = Label(aux_frame, image=sticker_image)
        sticker.image = sticker_image
        sticker.grid(row=1, column=i)

    # Sticker movement
    frames_label.update()
    frames_label_h = frames_label.winfo_height()
    frames_label_w = frames_label.winfo_width()

    x = frames_label_w / 2
    y = frames_label_h / 2

    l = Label(root, text="")
    l.grid(row=4, column=1)

    frames_label.bind('<B1-Motion>', lambda e: move(e, l))

    root.mainloop()


if __name__ == "__main__":
    main()
