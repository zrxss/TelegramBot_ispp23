# Telegram Bot для архивации заданий

Бот для учебной группы, который автоматически сохраняет задания от преподавателя, генерирует решения через LLM и позволяет получать их в личном чате.

## Возможности

- Отслеживание файлов от конкретного преподавателя в групповом чате
- Поддержка `.docx` и `.txt`
- Анализ файла через LLM: является ли файл заданием
- Генерация решения
- Сохранение заданий и решений в БД
- Просмотр доступных заданий по датам
- Перегенерация решения для выбранного задания

## Технологии

- Python
- aiogram 3.x
- SQLite
- Gemini API
- Mistral API
- Mammoth для чтения `.docx`


## Установка

1. Клонировать репозиторий:

```
git clone git@github.com:zrxss/TelegramBot_ispp23.git
cd TelegramBot_ispp23
``` 
2. Создать виртуальное окружение:
```
python -m venv .venv
source .venv/Scripts/activate
```
3. Установить зависимости:
```
pip install -r requirements.txt
```
## Настройка

Создать файл `config.py` по примеру `config.example.py`:
```
TOKEN = "your_bot_token_here"
GEMINI_KEY = "your_gemini_key_here"
MISTRAL_KEY = "your_mistral_key_here"
TEACHER_ID = 123456789
```
## Запуск
```
python run.py
```
## Структура проекта
```
run.py                  # запуск бота
database.py             # работа с SQLite
ai_engine.py            # запросы к LLM
prompts.py              # промпты для анализа и генерации
handlers/group_parser.py # обработка файлов в группе
handlers/private_chat.py # личное меню пользователя
config.example.py       # пример конфигурации
```

## Ограничения 

- Бот рассчитан на учебное использование
- Используются бесплатные API с лимитами
- Нет системы ролей и whitelist пользователей
- SQLite используется синхронно