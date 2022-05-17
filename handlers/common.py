import requests
from config import Utils
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from requests.auth import HTTPBasicAuth

CONFIG = Utils.load_env()


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")


def get_response(entity, data, method="GET"):
    if method == "GET":
        return requests.get(CONFIG["BD_SERVER"] + entity,
                            auth=HTTPBasicAuth(CONFIG["USER"], CONFIG["PASSWORD"]))
    elif method == "POST":
        return requests.post(CONFIG["BD_SERVER"] + entity,
                             auth=HTTPBasicAuth(CONFIG["USER"], CONFIG["PASSWORD"]),
                             json=data)
    elif method == "DELETE":
        return requests.delete(CONFIG["BD_SERVER"] + entity,
                               auth=HTTPBasicAuth(CONFIG["USER"], CONFIG["PASSWORD"]),
                               json=data)
    elif method == "PUT":
        return requests.put(CONFIG["BD_SERVER"] + entity,
                            auth=HTTPBasicAuth(CONFIG["USER"], CONFIG["PASSWORD"]),
                            json=data)
    elif method == "PATCH":
        return requests.patch(CONFIG["BD_SERVER"] + entity,
                              auth=HTTPBasicAuth(CONFIG["USER"], CONFIG["PASSWORD"]),
                              json=data)
    else:
        return None
