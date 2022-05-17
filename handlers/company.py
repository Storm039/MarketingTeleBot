import requests
from requests.auth import HTTPBasicAuth
from config import Utils

CONFIG = Utils.load_env()


class CurrentCompany:
    def __init__(self):
        self.id = CONFIG["ID_COMPANY"]
        self.activity = False

    def check_activity(self):
        entity = CONFIG["COMPANY_API_ACTIVITY"]
        response = requests.get(CONFIG["BD_SERVER"] + entity + str(self.id),
                                auth=HTTPBasicAuth(CONFIG["USER"], CONFIG["PASSWORD"]))
        if response.status_code == 200:
            json_r = response.json()
            if json_r.get("activity") is None:
                return self.activity
            else:
                self.activity = json_r.get("activity")
                return self.activity


class ConfigData:
    def __init__(self):
        self.params = {}

    def get_params(self):
        entity = CONFIG["DATA_CONFIG_API_LIST"]
        data = {
            "id_company": CONFIG["ID_COMPANY"]
        }
        response = requests.post(CONFIG["BD_SERVER"] + entity,
                                 json=data,
                                 auth=HTTPBasicAuth(CONFIG["USER"], CONFIG["PASSWORD"]))
        if response.status_code == 200:
            json_r = response.json().get("result")
            if not json_r:  # данные не обнаружены
                return self.params
            params_dict = {}
            for param in json_r:
                params_dict[param["param_key"]] = param["param_val"]
            self.params = params_dict
        return self.params



