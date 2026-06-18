from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import BufferedInputFile, CallbackQuery

from datetime import datetime
import time
import random

import database

from ai_engine import generate_answer
from config import cute_words_universal



private_router = Router()
private_router.message.filter(F.chat.type == "private")
private_router.callback_query.filter(F.message.chat.type == "private")



@private_router.message(CommandStart())   # Старт бота
async def private(message: types.Message):
    await message.answer('''
    ˚₊‧꒰ა ☆ ໒꒱ ‧₊˚
    Привет, милашечка :З
    
    Я маленький ботик-помощничек ʕっ•ᴥ•ʔっ
    Я тихонечко сижу в беседе, ловлю практические задания от Александра Рузанова, решаю их и аккуратненько складываю в свою уютную базу решений 📚✨
    
    Чтобы посмотреть сохранённые задания, просто используй кнопочки внизу.
    Там всё заботливо разложено, чтобы тебе не пришлось копаться в беседе, страдать, плакать и искать “а где же был тот самый файл?” (ಥ﹏ಥ)
    
    Помни: ты не глупый/ая.
    У тебя просто лапки, дела поважнее и вообще жизнь непростая штука. 
    Пользуйся мной, не стесняйся, и знай -
    ты самый лучший/ая, самый умненький/ая и вообще солнышко группы ☀️
    
    Небольшое предупреждение для непосед! Ботик работает на бесплатных API у
    которых совсем не большие лимиты :(. Поэтому тех кто будет баловаться, я буду вынужден забанить нахуй.
    ''',
                         reply_markup=keyboard())


def keyboard():   # Функция создания кнопок внизу
    kb = [
        [types.KeyboardButton(text="📚 Доступные задания")],
        [types.KeyboardButton(text="🔄 Перегенерировать ответ")]   # Клавиатура в aiogram это список списков, где списки - строки, а их элементы - столбцы
    ]
    buttons = types.ReplyKeyboardMarkup(keyboard=kb,
                                        resize_keyboard=True,
                                        input_field_placeholder=f"{random.choice(cute_words_universal)} выбери опцию:")
    return buttons



@private_router.message(F.text == "📚 Доступные задания")
async def show_available_tasks(message: types.Message):   # Функция вывода заданий из БД
    dates = database.available_tasks()

    days_ru = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

    if not dates:
        await message.answer(f"{random.choice(cute_words_universal)} пока заданий нет")
        return

    builder = InlineKeyboardBuilder()   # ИнлайнБилдер для динамических элементов клавиатуры


    for date in dates:   # Циклом заполняем клаву
        date_obj = datetime.strptime(date[0], "%Y-%m-%d")
        day_name = days_ru[date_obj.weekday()]
        builder.button(text=f"{date[0]}, {day_name}, Количество заданий {date[1]}",
                       callback_data=f"date:{date[0]}"   # Колбек, флаг для удобности использования в боте
                       )

    builder.adjust(1)   # Метод задает столбцы кнопок
    buttons = builder.as_markup()   # Превращение инлайнбилдера в клаву

    await message.answer(f"{random.choice(cute_words_universal)} выбери дату", reply_markup=buttons)



@private_router.callback_query(F.data.startswith(f"date:"))
async def send_solutions(callback_query: CallbackQuery):

    await callback_query.answer()

    date = callback_query.data.split("date:")[1]

    solutions = database.get_solution_by_date(date)
    count=1
    for solution in solutions:
        await callback_query.message.answer_document(document=BufferedInputFile(solution[0].encode('utf-8'), filename=f'{count}_{solution[1].capitalize()}_{date}_{solution[2]}.md'))
        count+=1

    # my_bytes = ai_solutions.text.encode('utf-8')   # Превращаем текст в файле в байты и через специальный класс не сохраняя файл через озу скидываем ответ пользователю
    # await message.answer_document(document=BufferedInputFile(my_bytes, filename="solution.md"))



@private_router.message(F.text == "🔄 Перегенерировать ответ")
async def show_available_tasks_for_regenerate(message: types.Message):
    dates = database.available_tasks()

    days_ru = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

    if not dates:
        await message.answer(f"{random.choice(cute_words_universal)} пока заданий нет")
        return

    builder = InlineKeyboardBuilder()   # ИнлайнБилдер для динамических элементов клавиатуры

    for date in dates:   # Циклом заполняем клаву
        date_obj = datetime.strptime(date[0], "%Y-%m-%d")
        day_name = days_ru[date_obj.weekday()]
        builder.button(text=f"{date[0]}, {day_name}, Количество заданий {date[1]}",
                       callback_data=f"date_new_generate:{date[0]}"   # Колбек, флаг для удобности использования в боте
                       )

    builder.adjust(1)   # Метод задает столбцы кнопок
    buttons = builder.as_markup()   # Превращение инлайнбилдера в клаву

    await message.answer(f"{random.choice(cute_words_universal)} выбери дату", reply_markup=buttons)



@private_router.callback_query(F.data.startswith(f"date_new_generate:"))
async def choice_task(callback_query: CallbackQuery):

    await callback_query.answer()

    date = callback_query.data.split("date_new_generate:")[1]

    tasks = database.get_task_by_date(date)

    builder = InlineKeyboardBuilder()

    for task in tasks:
        builder.button(text=f"{task[2].capitalize()} {task[3]}",
                       callback_data=f"task_id:{task[0]}"
                       )

    builder.adjust(1)
    buttons = builder.as_markup()

    await callback_query.message.answer(f'{random.choice(cute_words_universal)} выбери задание', reply_markup=buttons)


user_last_click = {}

@private_router.callback_query(F.data.startswith(f"task_id:"))
async def regenerate_task(callback_query: CallbackQuery):

    await callback_query.answer()

    start_time = time.monotonic()
    user_id = callback_query.from_user.id

    if user_id in user_last_click and start_time - user_last_click[user_id] < 30:
        await callback_query.message.answer(f"{random.choice(cute_words_universal)} подожди {int(30-(start_time - user_last_click[user_id]))} секунд для повторного запроса")
        return

    user_last_click[user_id] = start_time

    task_id = callback_query.data.split("task_id:")[1]

    task = database.get_task_by_id(task_id)
    try:
        regen_solution = await generate_answer(task[0],task[1],regen = True)
    except Exception as e:
        print('Regeneration error:',e)
        await callback_query.message.answer(f"{random.choice(cute_words_universal)} регенерация не удалась, попробуй позже!")
        return


    my_bytes = regen_solution.encode('utf-8')   # Превращаем текст в файле в байты и через специальный класс не сохраняя файл через озу скидываем ответ пользователю
    await callback_query.message.answer_document(document=BufferedInputFile(my_bytes, filename=f"regenerate_{task[1].capitalize()}_{task[2]}.md"))




