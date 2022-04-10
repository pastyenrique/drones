from crypt import methods
import imghdr
from pyexpat import model
from unittest import result
from flask import Flask, jsonify, request
import controller
import re
import base64
from db import create_tables

app = Flask(__name__)

@app.route('/')
def index():
    return "Drone Dispatch Controller"

#FUNCTION TO GET ALL DRONES AND SHOW
@app.route('/drones', methods=["GET"])
def get_all_drones():
    drones = controller.get_drones()
    return jsonify(drones)

#FUNCTION TO REGISTER DRONE ON DB
@app.route("/drone", methods=["POST"])
def insert_drone():
    drone_details = request.get_json()
    serial_number = drone_details["serial_number"]        
    model = drone_details["model"]
    weight_limit = drone_details["weight_limit"]
    battery_capacity = drone_details["battery_capacity"]
    state = drone_details["state"]
    if len(serial_number) <= 100 and model in ['Lightweight','Middleweight','Cruiserweight','Heavyweight'] and int(weight_limit) <= 500 and int(battery_capacity) <= 100 and state in ['IDLE','LOADING','DELIVERING', 'DELIVERED', 'RETURNING']:
        drone_id = controller.insert_drone(serial_number, model, weight_limit, battery_capacity, state)
    else:
        return jsonify({'message': 'Error registering drone: Review your entry data. Drone serial number must have at maximum 100 characters, model must get one of this values [Lightweight, Middleweight, Cruiserweight, Heavyweight], weight limit must have at max 500 grs, battery capacity cant be greater than 100 and state must be one of these values. [IDLE, LOADING, LOADED, DELIVERING, DELIVERED, RETURNING]'})
    if drone_id:
        return jsonify({'message': 'Drone created'})
    return jsonify({'message': 'Internal Error'})

#FUNCTION TO LOAD MEDICATIONS ON SPECIFIC DRONE
@app.route("/load/<drone_id>", methods=["POST"])
def load_medications_on_drone(drone_id):
    medication_details = request.get_json()
    my_drone = get_drone_by_id(drone_id)
    medication_list = medication_details["medications"]
    if my_drone and medication_list:
        weight_limit = my_drone.json[3]
        battery_capacity = my_drone.json[4]
        if battery_capacity >= 25:
            total_weight = sum(item['weight'] for item in medication_list)
            if total_weight <= weight_limit:
                medications_loaded = []
                for medication in medication_list:
                    name_verifing = re.findall("[-+ \w]", medication["name"])
                    if len(name_verifing) < len(medication["name"]):
                        return jsonify({'message': 'Error loading medication, medication name can only have numbers, letters and - or _'})
                    code_pattern = '[A-Z0-9_]'
                    result = re.match(code_pattern, medication["code"])
                    if not result:
                        return jsonify({'message': 'Error loading medication, medication code allowed only upper case letters, underscore and numbers'})
                    med_image = medication["image"]
                    with open(med_image, "rb") as f:
                        img = f.read()
                    if img:        
                        img_b64 = base64.b64encode(img).decode("utf8")
                    med = controller.load_medication(medication["name"], medication["weight"], medication["code"], img_b64, drone_id)
                    update_drone_state(drone_id)
                    medications_loaded.append(medication)
                if len(medications_loaded) == len(medication_list):
                    return jsonify({'message': 'All medications loaded'})
            else:
                return jsonify({'message': 'Error loading medication, total medication weight can not be greater than drone weight limit'})
        else:
            return jsonify({'message': 'Drone created without medication, drone battery level is under 25%'})
    else:
        return jsonify({'message': 'Error: Drone id not exist or you have not passed medications'})

#FUNCTION FOR UPDATE SPECIFIC DRONE STATE
def update_drone_state(drone_id):
    loading_state = "LOADED"
    result = controller.update_drone_state(drone_id, loading_state)
    if result:
        return jsonify({'message': 'Drone state updated'})
    return jsonify({'message': 'Internal Error'})


#FUNCTION FOR UPDATE ANY FIELD OF SPECIFIC DRONE
@app.route("/drone/<id>", methods=["PUT"])
def update_drone(id):
    drone_details = request.get_json()
    serial_number = drone_details["serial_number"]
    model = drone_details["model"]
    weight_limit = drone_details["weight_limit"]
    battery_capacity = drone_details["battery_capacity"]
    state = drone_details["state"]
    result = controller.update_drone(id, serial_number, model, weight_limit, battery_capacity, state)
    if result:
        return jsonify({'message': 'Drone updated'})
    return jsonify({'message': 'Internal Error'})

#DELETE DRONE FUNCTION
@app.route("/delete/<id>", methods=["DELETE"])
def delete_drone(id):
    result = controller.delete_drone(id)
    if result:
        return jsonify({'message': 'Drone deleted from the database'})
    return jsonify({'message': 'Internal Error'})


#FUNCTION FOR GETTING SPECIFIC DRONE BY ID
@app.route("/drone/<id>", methods=["GET"])
def get_drone_by_id(id):
    drone = controller.get_by_id(id)
    if drone:
        return jsonify(drone)
    return jsonify({'message': 'Drone does not exist'})


#FUNCTION FOR GET ALL DRONES FROM SPECIFIC STATE
@app.route("/state/<state>", methods=["GET"])
def get_drone_by_state(state):
    result = controller.get_drone_state(state)
    if result:
        return jsonify(result)
    return jsonify({'message': 'Were not found any drone with the state given on the url'})

#FUNCTION TO GET ALL MEDICATIONS FROM SPECIFIC DRONE
@app.route("/medications/<id_drone>", methods=["GET"])
def get_medications_by_drone(id_drone):
    result = controller.medications_by_drone(id_drone)
    if result:
        return jsonify(result)
    return jsonify({'message': 'Were not found any medication with the drone_id given on the url'})


#FUNCTION TO GET BATTERY LEVEL FROM SPECIFIC DRONE
@app.route("/battery/<id_drone>", methods=["GET"])
def get_battery_level_by_drone(id_drone):
    result = controller.battery_level_by_drone(id_drone)
    if result:
        return jsonify(result)
    return jsonify({'message': 'Were not found any drone with the id given on the url'})


#CRON FUNCTION TO SHOW IN LOG FILE ALL DRONES BATTERY LEVEL
@app.route("/battery/drones", methods=["GET"])
def get_all_drones_battery_level():
    result = controller.battery_level_all_drones()
    if result:
        return jsonify(result)
    return jsonify({'message': 'Internal error'})


if __name__ == "__main__":
    create_tables()
    """
    Here you can change debug and port
    Remember that, in order to make this API on production, you must set debug in False
    """
    #app.run(host='0.0.0.0', port=8000, debug=False)
    app.run(debug=True)