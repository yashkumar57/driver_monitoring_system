import cv2 as c
import os
from datetime import datetime
from storage import upload_screenshot

SCREENSHOT_DIR = "../screenshots"

def save_screenshot(frame):

    # create screenshots folder if missing
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    # unique filename using time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"alert_{timestamp}.jpg"
    full_path = os.path.join(SCREENSHOT_DIR, filename)

    # save image
    c.imwrite(full_path, frame)

    public_url = upload_screenshot(full_path)
    print(public_url)
    return public_url