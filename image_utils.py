import base64
import os
import re
import time
from PIL import Image
import cv2
import numpy as np
import errno

TEMP_IMG_FOLDERS = "frames"

def encode_image(image_path):
    while True:
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except IOError as e:
            if e.errno != errno.EACCES:
                # Not a "file in use" error, re-raise
                raise
            # File is being written to, wait a bit and retry
            time.sleep(0.1)
            
def take_pic(video_cap):
    # Create the frames folder if it doesn't exist
    frames_dir = os.path.join(os.getcwd(), TEMP_IMG_FOLDERS)
    os.makedirs(frames_dir, exist_ok=True)

    ret, frame = video_cap.read()
    if ret:
        # Convert the frame to a PIL image
        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Resize the image
        max_size = 250
        ratio = max_size / max(pil_img.size)
        new_size = tuple([int(x*ratio) for x in pil_img.size])
        resized_img = pil_img.resize(new_size, Image.LANCZOS)

        # Convert the PIL image back to an OpenCV image
        frame = cv2.cvtColor(np.array(resized_img), cv2.COLOR_RGB2BGR)

        # Determine the next frame number
        frame_files = [f for f in os.listdir(TEMP_IMG_FOLDERS) if re.match(r'frame_\d+\.jpg', f)]
        frame_numbers = [int(re.search(r'\d+', f).group()) for f in frame_files]
        next_frame_number = max(frame_numbers, default=0) + 1

        # Save the frame as an image file
        # frame_filename = f'frame_{next_frame_number:02}.jpg'
        frame_filename = f'frame_{next_frame_number}.jpg'
        path = os.path.join(TEMP_IMG_FOLDERS, frame_filename)
        cv2.imwrite(path, frame)
    else:
        print("Failed to capture image")

    # path to your image
    image_path = os.path.join(os.getcwd(), path)

    # getting the base64 encoding
    return encode_image(image_path)