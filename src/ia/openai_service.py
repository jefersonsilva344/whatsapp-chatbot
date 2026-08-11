from openai import OpenAI
from dotenv import load_dotenv

from ia.prompt import SYSTEM_PROMPT

import os

load_dotenv()


class OpenAIService:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )


    def responder(self, mensagem, historico):

        messages = [

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }

        ]

        messages.extend(historico)

        messages.append(
            {
                "role": "user",
                "content": mensagem
            }
        )

        resposta = self.client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=messages,

            temperature=0.5,

            max_tokens=150

        )

        return resposta.choices[0].message.content.strip()