from openai import OpenAI
from enum import Enum

from typing import Any
from time import time, sleep
import json
import base64
from keys import OPENAI_API_KEY
from utils.cache import get_from_cache, update_cache


EXTENSION_TO_FILE_TYPE = {
    "jpg": "jpeg",
    "webp": "webp",
    "png": "png"
}

class Model(str):
    GPT_4 = "gpt-4"
    GPT_4_VISION = "gpt-4-vision-preview"

class OpenAIClient:
    def __init__(self, api_key: str) -> None:
        self.client = OpenAI(api_key=api_key)

    def ask_model(self, model: str, messages) -> str:
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": messages
                    }
                ],
                max_tokens=1000,
                temperature=0,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            pass
        return None

    def ask_model_with_retry(self, model: Model, messages: list[dict[str, Any]]) -> str:
        while (response := self.ask_model(model, messages)) is None:
            sleep(1)
            pass
        return response


    def get_response(self, messages: list[dict[str, Any]], model: Model=Model.GPT_4) -> str:
        prompt_key = str(messages)
        if cached_response := get_from_cache(prompt_key):

            return cached_response

        response = self.ask_model_with_retry(model, messages)

        update_cache(prompt_key, response)

        return response


    def encode_image(self, image_path: str) -> str:
        image_extension = image_path.split(".")[-1]

        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        file_type = EXTENSION_TO_FILE_TYPE.get(image_extension)

        if file_type is None:
            raise ValueError("Unsupported file type")

        return f"data:image/{file_type};base64,{base64_image}"



    def ask_about_image(self, prompt: str, image_path: str) -> str:
        image_data = self.encode_image(image_path=image_path) 
        messages = [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": image_data,
                    "detail": "high",
                }
            },
        ]

        return self.get_response(messages, Model.GPT_4_VISION)
    
    def get_image_details(self, prompt: str, image_path: str) -> dict[str, Any]:
        response = self.ask_about_image(prompt=prompt, image_path=image_path)
        if response.startswith("```json"):
            response = response.lstrip("```json").rstrip("```")

        dict_response = json.loads(response)
        return dict_response


client = OpenAIClient(api_key=OPENAI_API_KEY)