from tkinter import Tk, Canvas, NW
from tkinter import *
from PIL import Image, ImageTk, ImageGrab
import cv2
import effects
import os

image_counter = 0

sticker_paths = os.listdir("imgs/stickers")
stickers_qty = len(sticker_paths)

stickers_bar_imgs = list(range(stickers_qty))
stickers_imgs = list(range(stickers_qty))

initial_binds = list(range(stickers_qty))
binds = list(range(stickers_qty))


def take_picture(root, canvas):
    global image_counter

    x = root.winfo_rootx() + canvas.winfo_x() + 54
    y = root.winfo_rooty() + canvas.winfo_y() + 2
    xx = x + canvas.winfo_width() - 4
    yy = y + canvas.winfo_height() - 127

    image_counter += 1
    ImageGrab.grab(bbox=(x, y, xx, yy)).save(
        f"imgs/screenshots/screenshot_{image_counter}.png")


def show_frames(frames_canvas, cap, effects_manager):
    frame = cap.read()[1]

    frame_with_effect = cv2.cvtColor(
        effects_manager.apply_effect(frame), cv2.COLOR_BGR2RGBA)

    img = Image.fromarray(frame_with_effect)

    imgtk = ImageTk.PhotoImage(image=img)
    frames_canvas.imgtk = imgtk
    frame_id = frames_canvas.create_image(0, 0, image=imgtk, anchor=NW)
    frames_canvas.tag_lower(frame_id)
    frames_canvas.after(60, lambda: show_frames(
        frames_canvas, cap, effects_manager))

    return frames_canvas


def move(e, frames_canvas, image, i):
    global stickers_imgs

    def make_lambda(x):
        img = Image.open(
            f"imgs/stickers/{x}.png").resize((80, 80), Image.ANTIALIAS)
        return lambda e: move(e, frames_canvas, img, x)

    stickers_imgs[i] = ImageTk.PhotoImage(image)

    binds[i] = frames_canvas.create_image(
        e.x, e.y, image=stickers_imgs[i])

    frames_canvas.tag_bind(
        binds[i], '<B1-Motion>', make_lambda(i), add=f"+a{i}")


def main():
    root = Tk()

    # Video
    cap = cv2.VideoCapture(0)
    effects_manager = effects.EffectsManager()
    main_frame = Frame(root)
    main_frame.grid(row=0, column=1)

    frames_canvas = Canvas(main_frame, width=600, height=600)

    Button(main_frame, text="Take picture", bd=0,
           bg='#addedb', width=20, height=2, command=lambda: take_picture(root, frames_canvas)).pack(pady=10)

    frames_canvas.pack(expand=YES, fill=BOTH)
    frames_canvas = show_frames(frames_canvas, cap, effects_manager)

    # # Buttons
    width = 25
    height = 40

    arrow_left = ImageTk.PhotoImage(
        Image.open("imgs/icons/arrow_left.png").resize((width, height), Image.ANTIALIAS))

    arrow_right = ImageTk.PhotoImage(
        Image.open("imgs/icons/arrow_right.png").resize((width, height), Image.ANTIALIAS))

    Button(root, image=arrow_left, width=width + 25,
           height=height, borderwidth=0, command=effects_manager.previous_effect).grid(row=0, column=0)
    Button(root, image=arrow_right, width=width + 25,
           height=height, borderwidth=0, command=effects_manager.next_effect).grid(row=0, column=2)

    # Stickers
    for i in range(stickers_qty):
        def make_lambda(x):
            img = Image.open(
                f"imgs/stickers/{x}.png").resize((80, 80), Image.ANTIALIAS)
            return lambda e: move(e, frames_canvas, img, x)

        stickers_bar_imgs[i] = ImageTk.PhotoImage(
            Image.open(f"imgs/stickers/{sticker_paths[i]}").resize((80, 80), Image.ANTIALIAS))

        initial_binds[i] = frames_canvas.create_image(
            i*80, 500, image=stickers_bar_imgs[i], anchor=NW)

        frames_canvas.tag_bind(
            initial_binds[i], '<B1-Motion>', make_lambda(i+1), add=f"+a{i}")

    root.mainloop()


if __name__ == "__main__":
    main()
