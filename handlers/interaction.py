from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import Utils
import aiogram.utils.markdown as fmt
from handlers.users import CurrentUser
from handlers.company import *
from handlers.texts import *
from handlers.marketing import *

CONFIG = Utils.load_env()


class StatesNewUser(StatesGroup):
    get_phone = State()


class StatesExistUser(StatesGroup):
    selection_menu = State()


# Этапы прохождения по ветки "Позвоните мне"
class StatesChangeUserName(StatesGroup):
    save_name = State()


# Функция, которая вызывается по команде /start
async def bot_start(message: types.Message, state: FSMContext):
    if message.chat.username is None:
        username = ''
    else:
        username = message.chat.username
    # записываем информацию о пользователе
    user_info = {
        "id_telegram": message.chat.id,
        "mention": message.chat.mention,
        "full_name": message.chat.full_name,
        "user_name": username,
        "phone": "",
        "company": CONFIG["ID_COMPANY"],
        "activity": True,
        "approval": False,
    }
    user = CurrentUser(id_telegram=message.chat.id, id_company=CONFIG["ID_COMPANY"])

    # Ищем пользователя в БД (если его нет, то он создасться)
    if not user.find_user():
        # создаем
        if not user.create_user(user_info):
            await message.answer(get_text_server_error())
            return

    # Проверяем соглашение на использование персональных данных с пользователем
    if user.phone == "" or not user.approval:
        await show_offer(message, state)
    else:
        await message.delete()
        await message.answer(get_text_menu_selection(), reply_markup=get_keyboard_main_menu(), parse_mode=types.ParseMode.HTML)


def get_keyboard_main_menu():
    buttons = [
        types.InlineKeyboardButton(text="💸 Сколько бонусов 💸", callback_data="bonuses"),
        types.InlineKeyboardButton(text="💎 Текущии акции 💎", callback_data="promotions"),
        types.InlineKeyboardButton(text="📇 Сменить имя 📇", callback_data="change_name"),
        types.InlineKeyboardButton(text="🔌 Отмена 🔌", callback_data="cancel")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


async def show_offer(message: types.Message, state: FSMContext):
    """
    Показываем соглашение на обработку персональных данных пользователю
    """
    # загружаем конфигурационные данные по компании
    company_params = ConfigData().get_params()
    # в полученных параметрах получаем по ключу ссылку на соглашение
    offer = company_params.get('offer')
    if not offer:
        await message.delete()
        await message.answer(get_text_server_error())
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        # В данном случае описываем только 2 команды (обработчик команд - get_phone())
        for name in ["Принимаю", "Не принимаю"]:
            keyboard.add(name)
        text = get_text_consent_processing_of_personal_data(offer)
        await message.answer(text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        await StatesNewUser.get_phone.set()


# Обработка ответа
async def get_phone(message: types.Message, state: FSMContext):
    if message.text == "Принимаю":
        selection_options = ["Разрешение на получение номера"]
        keyboard_type = 'request_contact'
        keyboard = create_keyboard(selection_options, keyboard_type=keyboard_type)
        await message.delete()
        await message.answer("Оставьте свой номер телефона", reply_markup=keyboard)
        await state.finish()
    elif message.text == "Не принимаю":
        await message.delete()
        await message.answer("Работа с ботом прекращена", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()


async def save_phone(message: types.Message, state: FSMContext):
    user = CurrentUser(id_telegram=message.contact.user_id, id_company=CONFIG["ID_COMPANY"])
    if not user.find_user():
        text = get_text_server_error()
    else:
        user.phone = message.contact.phone_number
        user.approval = True
        if user.update_user():
            text = get_text_save_phone_answer(True)
        else:
            text = get_text_save_phone_answer(False)
    await message.delete()
    await message.answer(text, reply_markup=types.ReplyKeyboardRemove())


# функция создания клавиатуры для вывода на экран
def create_keyboard(values, keyboard_type=None):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if keyboard_type == 'request_location':
        return keyboard.add(types.KeyboardButton(text="Поделиться геолокацией 🗺️", request_location=True))
    elif keyboard_type == 'request_contact':
        return keyboard.add(types.KeyboardButton(text="Поделиться контактом ☎", request_contact=True))
    elif keyboard_type == 'request_poll':
        return keyboard.add(types.KeyboardButton(text="Создать викторину",
                                                 request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
    else:
        for val in values:
            keyboard.add(val)
        return keyboard


# функция правильно расставляет кнопки в ряд
def location_buttons_in_row(values, keyboard: types.ReplyKeyboardMarkup):
    conf = {
        "max_val_in_row": 6,  # максимальное кол-во значений в строке
        'fill_empty': True  # добавлять ли пустые кнопки для полноты сетки
    }
    # считаем кол-во строк вывода дат
    if len(values) % conf['max_val_in_row'] == 0:
        num_rows = len(values) // conf['max_val_in_row']
    else:
        num_rows = len(values) // conf['max_val_in_row'] + 1

    # считаем,сколько всего кнопок нужно расставить
    if conf['fill_empty']:
        num_total_buttons = num_rows * conf['max_val_in_row']
    else:
        num_total_buttons = len(values)

    stop_process = False
    buttons = []
    current_num_button = 1
    current_col = 1

    # начинаем расстановку кнопок
    while current_num_button <= num_total_buttons:
        # проверим необходимость добавления пустых кнопок для полноты списка
        if current_num_button > len(values):
            buttons.append(types.KeyboardButton(' '))
        else:
            buttons.append(types.KeyboardButton(values[current_num_button - 1]))

        # проверить возможность расстановки в одной строке
        if current_col == conf['max_val_in_row'] or (not conf['fill_empty'] and current_num_button == len(values)):
            keyboard.row(*buttons)
            buttons = []
            current_col = 1
        else:
            current_col += 1

        current_num_button += 1

    f = 0
    return keyboard


async def inline_interceptor(callback: types.CallbackQuery, state: FSMContext):
    user = CurrentUser(id_telegram=callback.from_user.id, id_company=CONFIG["ID_COMPANY"])
    if not user.find_user():
        await callback.message.edit_text(get_text_server_error(), reply_markup=None)
        await callback.answer()
        return
    full_name_db = str(user.full_name)
    command_name = callback.values['data'].lower()
    if command_name == "bonuses":
        message_text = get_bonuses_info(user)
    elif command_name == "promotions":
        message_text = get_promotions_info(user)
    elif command_name == "change_name":
        message_text = get_text_change_user_name(full_name_db)
        await state.update_data(current_user=user)
        await StatesChangeUserName.save_name.set()
        await callback.message.edit_text("-"*10, reply_markup=None)
        await callback.message.answer(message_text)
        await callback.answer(message_text)
        return
    elif command_name == "cancel":
        await callback.message.edit_text("-"*10, reply_markup=None)
        await callback.message.answer(get_text_command_cancel())
        await callback.answer()
        return
    else:
        message_text = "-Получена неизвестная команда-"
    await callback.message.answer(message_text, parse_mode=types.ParseMode.HTML)
    await callback.answer()


def get_bonuses_info(user):
    bonus_info = Bonus()
    bonus_info.user = user.id_db
    if not bonus_info.get_balance():
        return  get_text_no_data_on_bonuses(user.full_name)

    amount = bonus_info.quantity
    if not amount:
        return get_text_no_data_on_bonuses(user.full_name)

    else:
        return get_text_on_amount_bonuses(user.full_name, amount)


def get_promotions_info(user):
    promotions = Promotions()
    promotions.company = user.company
    if not promotions.get_data():
        return get_text_no_promotions(user.full_name)
    else:
        if promotions.data:
            return get_text_for_promotions(user.full_name, promotions.data['result'])
        else:
            return get_text_no_promotions(user.full_name)


async def save_user_name(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user = user_data.get("current_user")
    if user:
        if len(message.text) < 4:
            message_text = get_text_handler_save_name(full_name=user.full_name, success=True)
            await message.answer(message_text)
            await StatesChangeUserName.save_name.set()
            return
        user.full_name = message.text
        if user.update_user():
            message_text = get_text_handler_save_name(full_name=user.full_name, success=False)
            await message.answer(message_text)
        else:
            await message.answer("Не удалось изменить имя, попробуйте позднее")
        await state.finish()
    else:
        await message.answer(get_text_server_error())
        await state.finish()


# Регистрация обработчиков
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands="start", state="*")
    dp.register_message_handler(get_phone, state=StatesNewUser.get_phone)
    dp.register_message_handler(save_user_name, state=StatesChangeUserName.save_name)
    dp.register_message_handler(save_phone, content_types=types.ContentType.CONTACT)
    dp.register_callback_query_handler(inline_interceptor)

