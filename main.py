# Folder
import os
import time
import cv2
from playsound import playsound

from image_utils import TEMP_IMG_FOLDERS, encode_image, take_pic
from openai_utils import process_img, response_to_speech, transcribe_audio

IMG_CAPTURE_INTERVAL = 5

test_data = [
    {'img': 'frame_1.jpg', 'transcription': "Absolutely maddening day! Missed the bus twice, couldn't snag an Uber. Now, I've completely missed this crucial meeting! Just great!"},
    {'img': 'frame_2.jpg', 'transcription': "Seems like bad luck's my shadow, always trailing behind. Missed opportunities, constant mishaps - can't catch a break to save my life!"},
]

test_mode = True

def run_coach(video_cap):
    script = []
    curr_pos = 0

    print("✨ Let's start our emotional coaching session")
    while True:
        if test_mode:
            transcription = test_data[curr_pos]['transcription']
            test_img_path = os.path.join(TEMP_IMG_FOLDERS, test_data[curr_pos]['img'])
            endcoded_img = encode_image(test_img_path)
        else:
            transcription = transcribe_audio()
            endcoded_img = take_pic(video_cap)
        
        response = process_img(
            endcoded_img, transcription=transcription, conversation=script)
        curr_pos += 1

        print(f"Detected sentiment: {response['person_feeling']}")
        print(f"Coach: {response['coach_response']}\n\n")
        
        # generate TTS and play it
        output_file = response_to_speech(response['coach_response'])
        playsound(output_file)

        script = script + [{"role": "assistant", "content": response}]

        time.sleep(IMG_CAPTURE_INTERVAL)

if __name__ == "__main__":
    video_cap = cv2.VideoCapture(1)

    # Wait for the camera to initialize
    time.sleep(2)

    if not video_cap.isOpened():
        raise IOError("Cannot open webcam")

    run_coach(video_cap)

    video_cap.release()
    cv2.destroyAllWindows()
