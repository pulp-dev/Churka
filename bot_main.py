from KPMLScraper import Scraper

import logging
from aiogram import Bot, Dispatcher, executor, types

import os
import asyncio
from dotenv import load_dotenv
import json


def process(line):
    lst = line.split(' ')


async def main():
    scraper = Scraper()

    async def pipeline():
        while True:
            flag = scraper.get_timetables_elements()
            print(flag)
            if flag:
                print('dfdf')
                for user in ids:
                    await bot.send_message(str(user), "Я чурка")
            await asyncio.sleep(10)

    with open("users.txt") as f:
        ids = set()
        cock = f.readlines()
        for cum in cock:
            ids.add(cum.strip())

    # /start
    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):
        await message.answer('Hello')
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
