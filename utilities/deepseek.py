import os

from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI

from prompts import deepseek_translation_prompt

load_dotenv()

api_key = os.environ.get("DEEPSEEK_API_KEY")
base_url = os.environ.get("DEEPSEEK_BASE_URL")

client = OpenAI(api_key=api_key, base_url=base_url)
client_async = AsyncOpenAI(api_key=api_key, base_url=base_url)


def translate(source_text: str):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": source_text},
        ],
        stream=False,
    )

    return response.choices[0].message.content


async def translate_async(input_text: str):
    response = await client_async.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": deepseek_translation_prompt},
            {"role": "user", "content": input_text},
        ],
        stream=False,
    )

    return response.choices[0].message.content
