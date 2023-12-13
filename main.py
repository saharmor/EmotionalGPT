# Folder
import time
import cv2

from image_utils import take_pic
from openai_utils import analyze_image

IMG_CAPTURE_INTERVAL = 5

fake_transcriptions = [
    # "I had a tough day at work "
]

def run_coach(video_cap):
    script = []

    while True:
        # analyze posture
        print("✨ Let's start our emotional coaching session")
        base64_image = take_pic(video_cap)
        analysis = analyze_image(base64_image, script=script)

        print("Coach:")
        print(analysis)

        # play_response

        script = script + [{"role": "assistant", "content": analysis}]

        # wait for 5 seconds
        time.sleep(IMG_CAPTURE_INTERVAL)


if __name__ == "__main__":
    # Initialize the webcam
    video_cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not video_cap.isOpened():
        raise IOError("Cannot open webcam")

    run_coach(video_cap)

    # Release the camera and close all windows
    video_cap.release()
    cv2.destroyAllWindows()
