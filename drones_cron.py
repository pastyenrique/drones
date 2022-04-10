import requests
import json

class DroneCron:

    def action_get_drones_battery_level(self):
        URL = "http://127.0.0.1:5000/battery/drones"
        response = requests.get(url=URL)
        file = "/home/pastor/Escritorio/Proyecto Musala/cron_log_batteries"
        with open(file, "w") as ff: 
            ff.write(str(response.json()))
        ff.close()

dr = DroneCron()

dr.action_get_drones_battery_level()