import os

from dotenv import load_dotenv
from volcenginesdkarkruntime._exceptions import ArkAPIError
from volcenginesdkarkruntime import AsyncArk

from prompts import chinese_prompt

load_dotenv()

api_key = os.environ.get("ARK_API_KEY")
endpoint_id = os.environ.get("ARK_ENDPOINT_ID")

client = AsyncArk(api_key=api_key)


async def translate_async(input_text: str):
    try:
        response = await client.chat.completions.create(
            model=endpoint_id,
            messages=[
                {"role": "system", "content": chinese_prompt},
                {"role": "user", "content": input_text},
            ],
        )

        return response.choices[0].message.content
    except ArkAPIError as e:
        raise e
