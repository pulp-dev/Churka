from KPMLScraper import Scraper
from config import BOT_TOKEN

import logging
from aiogram import Bot, Dispatcher, types
import asyncio
# import os
# from dotenv import load_dotenv

LAST_TABLE = "timetable02.03.pdf"
USERS_FILENAME = "users.txt"


def get_ids():
    with open("users.txt") as f:
        ids = set()
        lines = f.readlines()
        for line in lines:
            ids.add(line.strip())
    return ids


async def pipeline(scrapper, bot):
    while True:
        flag = scrapper.get_timetables_elements()
        if flag:
            global LAST_TABLE
            if flag != LAST_TABLE:
                LAST_TABLE = flag
                ids = get_ids()
                for user in ids:
                    await bot.send_message(str(user), "Чурка старался")
                    with open(f"TimeTables/{flag}", "rb") as doc:
                        await bot.send_document(user, document=doc)

        await asyncio.sleep(300)


async def main():
    # load_dotenv("config.env")
    # token = os.environ["TOKEN"]
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)
    scrapper = Scraper()

    # /start
    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):
        await message.answer('Здрасти, хозяин! Я буду отправлять вам хасписание. А пока держите последнее:')
        with open(f"TimeTables/{LAST_TABLE}", "rb") as doc:
            await message.answer_document(doc)
        msg_id = message.chat.id
        ids = get_ids()
        if msg_id not in ids:
            ids.add(str(message.chat.id))
            with open(USERS_FILENAME, "w") as f:
                for i in ids:
                    f.write(f"{str(i)}\n")

    await dp.skip_updates()
    task1 = asyncio.create_task(dp.start_polling())
    task2 = asyncio.create_task(pipeline(scrapper, bot))
    await task1
    await task2


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
