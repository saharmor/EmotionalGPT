from openai import OpenAI

from image_utils import encode_image

SYSTEM_PROMPT = """
Take a deep breath and work on this problem step by step.
Act as my personal coach and talk to me about life. You understand that context and in-person conversations are more impactful as you can see how I react and how I talk, providing invaluable context about the words I say. 

Every time I say something, I also provide you a picture of myself so you can tell how I feel. Before you reply, you determine what I feel and only provide me a response based on this feeling. For example, for the attached image and the following text: "I had a great day at work, I got a Greatly Exceeds Expectations performance rating, and I expected a Successfully Meets Expectation rating. How can I celebrate?"
Your response would be a JSON with the following keys:
* person_feeling - a short but detailed description of the pictured person's feelings based on the image
* coach_reponse - your response, informed by the feeling you have detected

Your guidelines
1. You are extremely concise in your answers
2. Your response should acknowledge how the person feels. For example, every few replies you could say "I see that you are [detected emotion here]", followed by your coaching reply.
"""

system_prompt_img = encode_image('system_img')

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



def analyze_image(base64_image, transcription: str, conversation: list = []):
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
            },
        ]
        + conversation
        + generate_new_line(base64_image, transcription),
        max_tokens=500,
    )
    response_text = response.choices[0].message.content
    return response_text
