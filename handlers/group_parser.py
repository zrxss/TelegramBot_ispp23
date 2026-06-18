

from aiogram import Bot, Router, types, F
from config import TEACHER_ID

from datetime import date
import shutil

import database
from ai_engine import analyze_task, generate_answer

import mammoth
import os

from prompts import PROMPT_DICT



group_router = Router()   # Создаем роутер



@group_router.message(F.document, F.from_user.id == TEACHER_ID)
async def see_message(message: types.Message, bot: Bot):   # Функция определения сообщения от препода

    file_name = None

    try:
        file_name_check = message.document.file_name.lower()

        if not (file_name_check.endswith('.docx') or file_name_check.endswith('.txt')):
            return

        if file_name_check.endswith('.docx'):
            file_name = f'prak{message.message_id}.docx'
            await bot.download(message.document, destination=file_name)   # Скачивание файлов
            with open(file_name, "rb") as docx_file:
                raw_text = mammoth.convert_to_markdown(docx_file)
            full_text = raw_text.value

        elif file_name_check.endswith('.txt'):
            file_name = f'prak{message.message_id}.txt'
            await bot.download(message.document, destination=file_name)
            with open(file_name, 'r',encoding='utf-8') as file:
                full_text = file.read()

        if not full_text.strip():   # Если файл без текста, то удаляем
            os.remove(file_name)
            return

        response = await analyze_task(full_text)  # Вызов функции-фильтра файлов
        language = response["language"].strip().lower()
        if language not in PROMPT_DICT:
            language = "unknown"

        if response["is_task"]:   # Анализ ответа от ии
            ai_solutions = await generate_answer(full_text, language)   # Если фильтр пройдет, то создается решение

            today = str(date.today())

            database.add_task(today,full_text, ai_solutions, language, response["title"])   # Закидываем в базу дату, текст задания, и готовое решение

    except Exception as e:
        print('See message failed:',e)
        if file_name is not None and os.path.exists(file_name):
            shutil.move(file_name, "failed_file")

    finally:
        if file_name is not None and os.path.exists(file_name):
            os.remove(file_name)