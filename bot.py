from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
from handlers.company import *
from handlers.common import *
from config import Utils
import handlers.interaction as interaction
import asyncio


# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Старт"),
        BotCommand(command="/cancel", description="Отмена")
    ]
    await bot.set_my_commands(commands)


async def main():
    # # Парсинг файла конфигурации
    config = Utils.load_env()

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config['TELEGRAM_TOKEN'])
    dp = Dispatcher(bot, storage=MemoryStorage())

    # проверим статус компании
    current_company = CurrentCompany()
    if not current_company.check_activity():
        return
    # Регистрация хэндлеров
    register_handlers_common(dp)
    # register_handlers_drinks(dp)
    interaction.register_handlers(dp)
    # Установка команд бота
    await set_commands(bot)
    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
