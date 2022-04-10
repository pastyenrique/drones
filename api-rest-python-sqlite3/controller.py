from db import get_db


def insert_drone(serial_number, model, weight_limit, battery_capacity, state):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO drone(serial_number, model, weight_limit, battery_capacity, state) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(statement, [serial_number, model, weight_limit, battery_capacity, state])
    db.commit()
    return cursor.lastrowid

def load_medication(name, weight, code, image, drone_id):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO medication(name, weight, code, image, drone_id) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(statement, [name, weight, code, image, drone_id])
    db.commit()
    return True


def update_drone(id, serial_number, model, weight_limit, battery_capacity, state):
    db = get_db()
    cursor = db.cursor()
    statement = "UPDATE drone SET serial_number = ?, model = ?, weight_limit = ?, battery_capacity = ?, state = ? WHERE id = ?"
    cursor.execute(statement, [serial_number, model, weight_limit, battery_capacity, state, id])
    db.commit()
    return True

def update_drone_state(id, state):
    db = get_db()
    cursor = db.cursor()
    statement = "UPDATE drone SET state = ? WHERE id = ?"
    cursor.execute(statement, [state, id])
    db.commit()
    return True

def delete_drone(id):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM drone WHERE id = ?"
    cursor.execute(statement, [id])
    db.commit()
    return True

def get_by_id(id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, serial_number, model, weight_limit, battery_capacity, state FROM drone WHERE id = ?"
    cursor.execute(statement, [id])
    return cursor.fetchone()

def get_drone_state(state):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, serial_number, model, weight_limit, battery_capacity, state FROM drone WHERE state = ?"
    cursor.execute(statement, [state])
    return cursor.fetchall()

def medications_by_drone(id_drone):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, name, weight, code, drone_id FROM medication WHERE drone_id = ?"
    cursor.execute(statement, [id_drone])
    return cursor.fetchall()

def battery_level_by_drone(id_drone):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT battery_capacity FROM drone WHERE id = ?"
    cursor.execute(statement, [id_drone])
    return cursor.fetchone()

def weight_limit_by_drone(id_drone):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT weight_limit FROM drone WHERE id = ?"
    cursor.execute(statement, [id_drone])
    return cursor.fetchone()

def battery_level_all_drones():
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, battery_capacity FROM drone"
    cursor.execute(statement)
    return cursor.fetchall()

def get_drones():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM drone"
    cursor.execute(query)
    return cursor.fetchall()
