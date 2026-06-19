from google import genai
from mistralai.client import Mistral
from config import GEMINI_KEY,MISTRAL_KEY

import json
import random

from prompts import *

client_g = genai.Client(api_key=GEMINI_KEY)
client_m = Mistral(api_key=MISTRAL_KEY)



async def analyze_task(text):   # Функция-фильтр определяющая является ли файл препода заданием
    try:
        answer = await client_g.aio.models.generate_content(  # Запрос в ии
            model="gemini-3.5-flash",
            contents=ANALYZE_PROMPT + text
        )
        answer = answer.text.strip()
    except Exception as e:
        print("Gemini filter failed: ",e)
        answer = await client_m.chat.complete_async(
            model="mistral-small-2506",
            messages=[
                {
                    "role": "user",
                    "content": ANALYZE_PROMPT + text
                }
            ]
        )
        answer = answer.choices[0].message.content.strip()

    answer = json.loads(answer)

    return answer


def random_style(language):
    reprompt = REPROMPT_DICT.get(language, REPROMPT_DICT["unknown"])
    style =  STYLE_DICT[random.randint(1,4)]
    reprompt =  reprompt.replace('{style}', style)
    return reprompt


async def generate_answer(task_text, language = "unknown", regen = False):   # Функция генерации ответа для задания от ИИ
    language = language.strip().lower()

    prompt = PROMPT_DICT.get(language, PROMPT_DICT["unknown"])
    if regen:
        reprompt = random_style(language)
        try:
            answer = await client_g.aio.models.generate_content(
                model="gemini-3.5-flash",
                contents= reprompt + task_text,
                config = genai.types.GenerateContentConfig(
                    temperature=1.4
                )
            )
            return answer.text
        except Exception as e:
            print("Gemini regeneration failed: ",e)
            answer = await client_m.chat.complete_async(
                model="codestral-2508",
                messages=[
                    {
                        "role": "user",
                        "content": reprompt + task_text
                    }
                ],
                temperature=1.4
            )
            return answer.choices[0].message.content
    try:
        answer = await client_g.aio.models.generate_content(
            model="gemini-3.5-flash",
            contents= prompt + task_text
        )
        return answer.text
    except Exception as e:
        print("Gemini generation failed: ",e)
        answer = await client_m.chat.complete_async(
            model="codestral-2508",
            messages=[
                {
                    "role": "user",
                    "content": prompt + task_text
                }
            ]
        )
        return answer.choices[0].message.content



