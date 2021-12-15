import cv2
import numpy as np


def maybe_add_alpha_channel(frame):
    try:
        frame.shape[3]
    except IndexError:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    return frame


def color_overlay(frame,
                  intensity=0.2,
                  blue=0,
                  green=0,
                  red=0):
    frame = maybe_add_alpha_channel(frame)
    frame_h, frame_w, frame_c = frame.shape
    color_bgra = (blue, green, red, 1)
    overlay = np.full((frame_h, frame_w, 4), color_bgra, dtype='uint8')
    cv2.addWeighted(overlay, intensity, frame, 1.0, 0, frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    return frame


def alpha_blend(frame_1, frame_2, mask):
    alpha = mask/255.0
    blended = cv2.convertScaleAbs(frame_1*(1-alpha) + frame_2*alpha)
    return blended


def invert(frame):
    return cv2.bitwise_not(frame)


def sepia(frame, intensity=0.5):
    blue = 20
    green = 66
    red = 112
    frame = color_overlay(frame,
                          intensity=intensity,
                          blue=blue, green=green, red=red)
    return frame


def circle_focus_blur(frame, intensity=0.2):
    frame = maybe_add_alpha_channel(frame)
    frame_h, frame_w, frame_c = frame.shape
    y = int(frame_h/2)
    x = int(frame_w/2)
    radius = int(x/2)
    center = (x, y)
    mask = np.zeros((frame_h, frame_w, 4), dtype='uint8')
    cv2.circle(mask, center, radius, (255, 255, 255), -1, cv2.LINE_AA)
    mask = cv2.GaussianBlur(mask, (21, 21), 11)
    blured = cv2.GaussianBlur(frame, (21, 21), 11)
    blended = alpha_blend(frame, blured, 255-mask)
    frame = cv2.cvtColor(blended, cv2.COLOR_BGRA2BGR)
    return frame


def portrait_mode(frame):
    frame = maybe_add_alpha_channel(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
    blured = cv2.GaussianBlur(frame, (21, 21), 11)
    blended = alpha_blend(frame, blured, mask)
    frame = cv2.cvtColor(blended, cv2.COLOR_BGRA2BGR)
    return frame


def main():
    cap = cv2.VideoCapture(3)

    if not cap.isOpened():
        print("Could not open video device")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    ret, frame = cap.read()
    result = frame.copy()

    available_opts = ['b', 'n', 'p', 's']

    selected_key = 'n'

    while(True):
        ret, frame = cap.read()

        cv2.imshow("original", frame)
        cv2.imshow("filtro", result)

        key = cv2.waitKey(1)

        if key != -1 and chr(key) in available_opts:
            key = chr(key)
        else:
            key = selected_key

        if key == '\x1b':
            break
        elif key == 'n':
            result = invert(frame)
        elif key == 'b':
            result = circle_focus_blur(frame)
        elif key == 'p':
            result = portrait_mode(frame)
        elif key == 's':
            result = sepia(frame)

        selected_key = key

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.waitKey()


if __name__ == '__main__':
    main()
