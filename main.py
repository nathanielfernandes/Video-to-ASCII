""" Webcam video to ASCII text viewer
    Author: Nathaniel Fernandes
"""
import cv2

# Reverse or unreverse this list depending on what background your terminal is
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", " "][::-1]


def scale_frame(frame, percent=7):
    """ Takes an OpenCV frame object and scales it properly for ASCII conversion.
        increasing percent drastically increases the final resolution of the converted
        when seen with ASCII characters. Lowering this value increases fps and keeps
        the text visible.
    """
    w = int((frame.shape[1] * percent / 100) * 1.75)
    h = int(frame.shape[0] * percent / 100)
    return cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)


def to_ascii(frame):
    """Takes a grayscale OpenCV frame object and returns a string of its ASCII form"""
    return "\n".join(["".join(ASCII_CHARS[i // 25] for i in slab) for slab in frame])


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    while True:
        # capture frame
        ret, frame = cap.read()

        # incase the webcam needs to warm up
        if ret:
            cv2.imshow("Webcam Video", frame)
            frame = scale_frame(frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            print(to_ascii(gray))

        # 1 ms of wait between frames, type q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

