import requests
from requests.auth import HTTPBasicAuth
from config import Utils
from handlers.common import *

CONFIG = Utils.load_env()


class CurrentUser:
    server = CONFIG['BD_SERVER']

    def __init__(self, id_telegram, id_company):
        self.id_db = None
        self.id_telegram = id_telegram
        self.mention = ""
        self.full_name = ""
        self.user_name = ""
        self.phone = ""
        self.company = id_company
        self.activity = True
        self.approval = False

    def find_user(self):
        entity = CONFIG["USERS_API_LIST"]
        method = "POST"
        data = {
            "id_telegram": self.id_telegram,
            "id_company": self.company,
        }
        response = get_response(entity, data, method)

        if response.status_code == 200:
            json_r = response.json().get('result')
            if not json_r: #данные не обнаружены
                return False
            else: #данные найдены
                return self.process_new_data(json_r[0])
        else:
            return False
        pass

    def create_user(self, user_info: dict):
        self.process_new_data(user_info)
        entity = CONFIG["USERS_API_CREATE"]
        method = "POST"
        data = {
            "id_telegram": self.id_telegram,
            "mention": self.mention,
            "full_name": self.full_name,
            "user_name": self.user_name,
            "phone": self.phone,
            "company": self.company,
            "activity": self.activity,
            "approval": self.approval
        }
        response = get_response(entity, data, method)
        if response.status_code == 201:
            json_r = response.json()
            return self.process_new_data(json_r)
        else:
            return False

    def delete_user(self):
        pass

    def update_user(self):
        entity = CONFIG["USERS_API_UPDATE"] + str(self.id_db) + "/"
        method = "PATCH"
        data = {
            "id_telegram": self.id_telegram,
            "mention": self.mention,
            "full_name": self.full_name,
            "user_name": self.user_name,
            "phone": self.phone,
            "company": self.company,
            "activity": self.activity,
            "approval": self.approval,
        }
        response = get_response(entity, data, method)
        if response.status_code == 200:
            return True
        else:
            return False

    def process_new_data(self, user_info):
        if user_info.get("id"):
            self.id_db = user_info.get("id")
        self.id_telegram = user_info.get("id_telegram")
        self.mention = user_info.get("mention")
        self.full_name = user_info.get("full_name")
        self.user_name = user_info.get("user_name")
        self.phone = user_info.get("phone")
        self.company = user_info.get("company")
        self.activity = user_info.get("activity")
        self.approval = user_info.get("approval")
        return True


    @staticmethod
    def get_all_users(id_company):
        pass

