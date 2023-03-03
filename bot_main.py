from KPMLScraper import Scraper

import logging
from aiogram import Bot, Dispatcher, executor, types

import os
import asyncio
from dotenv import load_dotenv


LAST_TABLE = "timetable02.03.pdf"


async def main():
    scraper = Scraper()

    def get_ids():
        with open("users.txt") as f:
            ids = set()
            cock = f.readlines()
            for cum in cock:
                ids.add(cum.strip())
        return ids

    async def pipeline():
        while True:
            flag = scraper.get_timetables_elements()
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

    # /start
    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):
        await message.answer('Здрасти, хозяин! Я буду отправлять вам хасписание. А пока держите последнее:')
        with open(f"TimeTables/{LAST_TABLE}", "rb") as doc:
            await message.answer_document(doc)
        ids = get_ids()
        ids.add(message.chat.id)
        with open("users.txt", "w") as f:
            for i in ids:
                f.write(f"{str(i)}\n")

    #await dp.skip_updates()
    task1 = asyncio.create_task(dp.start_polling())
    task2 = asyncio.create_task(pipeline())
    await task1
    await task2

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_dotenv("config.env")
    token = os.environ["TOKEN"]
    bot = Bot(token=token)
    dp = Dispatcher(bot)
    asyncio.run(main())
