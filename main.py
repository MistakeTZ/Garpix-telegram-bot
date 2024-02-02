import asyncio, logging
import sys, os
import json
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode

from user import User
import handler
import language


dp = Dispatcher()
load_dotenv()


async def main() -> None:
    global texts, bot

    with open("config.json") as f:
        config = json.load(f)

    """
    with open("data.json", encoding="utf8") as f:
        data = json.load(f)
    kb.cells = data["cells"]
    level.monster_types = data["monsters"]
    """

    language.start(config["DEFAULT_LANG"])

    bot = Bot(os.getenv("TG_TOKEN"), parse_mode=ParseMode.HTML)

    dp.include_router(handler.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())