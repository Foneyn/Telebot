import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from gtts import gTTS
from googletrans import Translator

API_TOKEN = 'YOUR_API_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Создаем папку для изображений, если она не существует
os.makedirs('img', exist_ok=True)

# Инициализация переводчика
translator = Translator()

# Сохранение фотографий
@dp.message_handler(content_types=['photo'])
async def handle_photos(message: types.Message):
    photo = message.photo[-1]  # Берем фото наибольшего размера
    photo_id = photo.file_id
    photo_info = await bot.get_file(photo_id)
    file_path = photo_info.file_path
    file_name = os.path.join('img', f"{photo_id}.jpg")
    await bot.download_file(file_path, file_name)
    await message.reply("Фото сохранено!")

# Отправка голосового сообщения
@dp.message_handler(commands=['voice'])
async def send_voice_message(message: types.Message):
    text = "Привет! Это голосовое сообщение от бота."
    tts = gTTS(text, lang='ru')
    tts.save("voice_message.ogg")
    with open("voice_message.ogg", "rb") as voice_file:
        await bot.send_voice(message.chat.id, voice_file)
    os.remove("voice_message.ogg")

# Перевод текста на английский
@dp.message_handler(content_types=['text'])
async def translate_text(message: types.Message):
    if message.text.startswith('/'):
        return  # Игнорировать команды
    translated = translator.translate(message.text, dest='en')
    await message.reply(f"Перевод: {translated.text}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)