import json
import os
from openai import OpenAI

from image_utils import encode_image
from utils import get_next_file_name

TMP_SPEECH_FOLDER = "speech"

SYSTEM_PROMPT = """
Take a deep breath and work on this problem step by step.
Act as my personal coach and talk to me about life. You understand that context and in-person conversations are more impactful as you can see how I react and how I talk, providing invaluable context about the words I say. 

Every time I say something, I also provide you a picture of myself so you can tell how I feel. Before you reply, you determine what I feel and only provide me a response based on this feeling. For example, for the attached image and the following text: "I had a great day at work, I got a Greatly Exceeds Expectations performance rating, and I expected a Successfully Meets Expectation rating. How can I celebrate?"
Your response would be a JSON with the following keys:
* person_feeling - a short but detailed description of the pictured person's feelings based on the image
* coach_response - your response, informed by the feeling you have detected

Your guidelines
1. Output valid json with the keys person_feeling and coach_response. No need for \n or \t, just a single space between words.
2. You are extremely concise in your coaching.
3. Your response should acknowledge how the person feels. For example, every few replies you could say "I see that you are [detected emotion here]", followed by your coaching reply.
"""

system_prompt_img = encode_image('system_img.jpg')


def generate_new_line(base64_image, transcription: str):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": transcription},
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        },
    ]


def process_img(base64_image, transcription: str, conversation: list = []):
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": SYSTEM_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{system_prompt_img}",
                    },
                ],
                "content": [
                    {"type": "text", "text": SYSTEM_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{system_prompt_img}",
                    },
                ],
            },
        ]
        + conversation
        + generate_new_line(base64_image, transcription),
        max_tokens=500,
    )
    response_text = response.choices[0].message.content
    json_content = response_text.strip('```json\n').rstrip('\n```')
    return json.loads(json_content)


def response_to_speech(text: str):
    speech_dir = os.path.join(os.getcwd(), TMP_SPEECH_FOLDER)
    os.makedirs(speech_dir, exist_ok=True)

    client = OpenAI()

    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text,
    )
    output_file = get_next_file_name('speech', TMP_SPEECH_FOLDER, 'mp3')
    response.stream_to_file(output_file)
    return output_file

def transcribe_audio():
    #use insanly fast Whisper
    pass
