import cv2 as c
import os
from datetime import datetime

def save_screenshot(frame):

    # create screenshots folder if missing
    if not os.path.exists("../screenshots"):
        os.makedirs("../screenshots")

    # unique filename using time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"../screenshots/alert_{timestamp}.jpg"

    # save image
    c.imwrite(filename, frame)

    print(f"Screenshot saved: {filename}")

    return filename