from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = 'YOUR_API_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Задание 1
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Привет", "Пока"]
    keyboard.add(*buttons)
    await message.answer("Выберите опцию:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ["Привет", "Пока"])
async def handle_greeting(message: types.Message):
    if message.text == "Привет":
        await message.answer(f"Привет, {message.from_user.first_name}!")
    elif message.text == "Пока":
        await message.answer(f"До свидания, {message.from_user.first_name}!")

# Задание 2
@dp.message_handler(commands=['links'])
async def send_links(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text="Новости", url="https://news.ycombinator.com/"),
        InlineKeyboardButton(text="Музыка", url="https://www.spotify.com/"),
        InlineKeyboardButton(text="Видео", url="https://www.youtube.com/")
    ]
    keyboard.add(*buttons)
    await message.answer("Выберите ссылку:", reply_markup=keyboard)

# Задание 3
@dp.message_handler(commands=['dynamic'])
async def send_dynamic(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Показать больше", callback_data="show_more")
    keyboard.add(button)
    await message.answer("Нажмите кнопку ниже:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'show_more')
async def process_callback_show_more(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text="Опция 1", callback_data="option_1"),
        InlineKeyboardButton(text="Опция 2", callback_data="option_2")
    ]
    keyboard.add(*buttons)
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in ['option_1', 'option_2'])
async def process_callback_options(callback_query: types.CallbackQuery):
    option = "Опция 1" if callback_query.data == 'option_1' else "Опция 2"
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, f"Вы выбрали {option}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)