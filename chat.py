from dotenv import load_dotenv
from openai import OpenAI
import os
import json
load_dotenv()

class Chat:
    def __init__(self, prompt) -> None:
        self.client = OpenAI(api_key=os.environ.get("OPENAI_KEY",""))
        self.messages = [
            {"role": "system", "content": prompt},
        ]

    def send_message_json(self,msg):
        self.messages.append({"role": "user", "content": msg})
        completion = self.client.chat.completions.create(
            model = "gpt-3.5-turbo-1106",
            response_format = {"type": "json_object"},
            messages=self.messages,
        )
        self.messages.append(completion.choices[0].message)
        response = json.loads(completion.choices[0].message.content)
        return response