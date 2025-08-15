import asyncio
import os
import subprocess
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram import F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile 
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile, Video
from aiogram.enums import ContentType
from aiogram.filters.command import Command
#я мог добавить и лишние либы т.к. мне похуй

bot = Bot("TOKEN")
dp = Dispatcher()

START = '''
Просто отправь или перешли мне видео, и я сразу сконвертирую его в кружок и пришлю обратно.
(бот сделан @UN2222NATE, по вопросам обращаться к нему)
'''

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(f"Привет, <b>{message.from_user.full_name}</b>! Я бот, который конвертирует видео в ТГ кружочки. \n{START}", parse_mode="HTML")

@dp.message(F.content_type == ContentType.VIDEO)
async def handle_video(message: types.Message):
    video: Video = message.video
    file = await bot.get_file(video.file_id)
    file_path = file.file_path
    input_filename = f"video_{message.chat.id}.mp4"
    output_filename = f"circle_{message.chat.id}.mp4"

    await bot.download_file(file_path, input_filename)
  
    subprocess.run([
        "ffmpeg", "-y",
        "-i", input_filename,
        "-vf", "crop='min(in_w, in_h)':'min(in_w, in_h)',scale=240:240", 
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-t", "180",
        output_filename
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.exists(output_filename):
        video_note = FSInputFile(output_filename)
        await message.answer("Вот твой кружок:")
        await message.answer_video_note(video_note)
    else:
        await message.answer("Ошибка при создании кружка...")

    for f in [input_filename, output_filename]:
        if os.path.exists(f):
            os.remove(f)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
