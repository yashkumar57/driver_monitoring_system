from storage import upload_screenshot

import os

image_path = os.path.join(
    os.getcwd(),
    "screenshots",
    "alert_20260519_181215.jpg"
)

print(image_path)

url = upload_screenshot(image_path)
print(url)