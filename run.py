import  asyncio
from aiogram import Bot, Dispatcher, types
from config import TOKEN
from aiogram.filters import CommandStart

bot = Bot(token=TOKEN)

dp=Dispatcher()

@dp.message(CommandStart())
async def answer(message: types.Message):
    await message.answer('Привет! Я живой!')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())