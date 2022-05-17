import requests
from requests.auth import HTTPBasicAuth
from config import Utils
from handlers.common import *

CONFIG = Utils.load_env()


class Promotions:
    server = CONFIG['BD_SERVER']

    def __init__(self):
        self.data = {"result": []}
        self.company = None

    def get_data(self):
        entity = CONFIG["PROMOTIONS_API_LIST"]
        method = "POST"
        data = {
            "id_company": self.company,
        }
        response = get_response(entity, data, method)

        if response.status_code == 200:
            json_r = response.json().get('result')
            if not json_r:
                return False
            else:
                return self.process_new_data(json_r)
        else:
            return False
        pass

    def process_new_data(self, data_info):
        for prom in data_info:
            data = {"id": prom.get("id"),
                    "date_start": prom.get("date_start"),
                    "date_end": prom.get("date_end"),
                    "description": prom.get("description"),
                    "activity": prom.get("activity"),
                    "image_url": prom.get("image_url"),
                    "data_sync": prom.get("data_sync"),
                    "guid_one_c": prom.get("guid_one_c")
                    }
            self.data["result"].append(data)
        return True



class Bonus:
    server = CONFIG['BD_SERVER']

    def __init__(self):
        self.quantity = None
        self.user = None
        self.data_sync = None

    def get_balance(self):
        entity = CONFIG["BONUSES_API_LIST"]
        method = "POST"
        data = {
            "id_user": self.user,
        }
        response = get_response(entity, data, method)

        if response.status_code == 200:
            json_r = response.json().get('result')
            if not json_r:  # данные не обнаружены
                return False
            else:  # данные найдены
                return self.process_new_data(json_r[0])
        else:
            return False
        pass

    def process_new_data(self, bonuses_info):
        if bonuses_info.get("user"):
            self.quantity = bonuses_info.get("quantity")
            self.user = bonuses_info.get("user")
            self.data_sync = bonuses_info.get("data_sync")
        return True
