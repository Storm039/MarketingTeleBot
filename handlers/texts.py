import aiogram.utils.markdown as fmt


def get_text_save_phone_answer(success=True):
    if success:
        return "".join(
            ["Спасибо, теперь вы можете пользоваться другими пунктами меню. \n ",
             "Для продолжения, вы можете вызвать команду /start"]
        )
    else:
        return "".join([
            "На стороне сервера произошла ошибка, попробуйте повторить операцию позже!",
        ])


def get_text_menu_selection():
    return "".join(
        ["Выберите желаемый пункт меню 👇",
         "\n",
         ])


def get_text_change_user_name(full_name):
    return "".join([
        f"{full_name} на клавиатуре введите имя, на которое будет изменено ваше текущее имя \n",
    ])


def get_text_command_cancel():
    return "".join([
        f"Выполните одну из команд:\n",
        f"- /start для возвращения в главное меню\n ",
        f"- /cancel для отмены текущего действия",
    ])


def get_text_handler_save_name(full_name, success):
    if success:
        return ''.join([
            f'{full_name} введенное имя должно быть не менее 4 символов!\n',
            f'Повторите ввод имени или выполнитеследующую операцию: \n',
            f'- отмена: /cancel\n',
            f'- вернуться на главное меню: /start\n',
        ])
    else:
        return "".join([
            f"Ваше имя успешно изменено\n",
            f"Для возврата в главное меню нажимте: ",
            f"/start или /cancel для прекращения работы",
        ])


def get_text_server_error():
    return ''.join([
        f'На стороне сервера произошла ошибка, попробуйте повторить операцию позже!',
    ])


def get_text_consent_processing_of_personal_data(offer):
    return "".join(
        [
            f"{fmt.hide_link(offer)}Продолжая пользоваться ботом, ",
            f"Вы принимаете условия по обработке персональных данных \n",
        ])


def get_text_no_data_on_bonuses(full_name):
    return "".join([
        f"{full_name}, к сожалению, информация о бонусных 💰 баллах отсутсвует 📉.",
    ])


def get_text_on_amount_bonuses(full_name, amount):
    return "".join([
        f"{full_name}, у вас имеется 📈:\n",
        f"💰 <b>{str(amount)}</b> 💰 бонусных баллов."
    ])


def get_text_no_promotions(full_name):
    return "".join([
        f"{full_name}, на данный момент нет действующих акций в компании 🚫"
    ])


def get_text_for_promotions(full_name, promotions):
    set_texts = [f"<b>{full_name} далее представлен список действующих акций:</b>\n{'*'*15}\n"]
    for prom in promotions:
        # date_start = prom.get("date_start")
        # date_end = prom.get("date_end")
        description = prom.get("description")
        image_url = prom.get("image_url")

        if description:
            set_texts.append(f"{description}\n")
            if image_url:
                set_texts.append(f"Ссылка 💻:\n")
                set_texts.append(f"{image_url}\n")
            set_texts.append(f"{'*'*15}\n")
    return "".join(set_texts)