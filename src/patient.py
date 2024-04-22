from datetime import datetime
import uuid
import requests
from itertools import chain
from config import GENDERS, WARD_NUMBERS, ROOM_NUMBERS ,API_CONTROLLER_URL


class Patient:
    def __init__(self, name,gender,age):
        self.patient_id = str(uuid.uuid4())
        self.patient_name = name
        self.patient_age = self._validate_age(age)
        self.patient_gender = self._validate_gender(gender)
        self.patient_checkin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_checkout = None
        self.patient_ward = None
        self.patient_room = None
    def get_id(self):
        return str(self.patient_id)
    def get_name(self):
        return str(self.patient_name)
    def get_age(self):
        return str(self.patient_age)
    def get_gender(self):
        return str(self.patient_gender)
    def get_room(self):
        return str(self.patient_room)
    def get_ward(self):
        return str(self.patient_ward)
        

    def _validate_gender(self, gender):
        if gender not in GENDERS:
            raise ValueError(f"Invalid gender: {gender}. Valid options are: {', '.join(GENDERS)}")
        return gender

    def _validate_age(self, age):
        if not isinstance(age, int) or age <= 0:
            raise ValueError(f"Invalid age: {age}. Age must be a positive integer.")
        else:
            return age

    def set_room(self, room_number):
        rooms = list(ROOM_NUMBERS.values())
        flatten = list(chain.from_iterable(rooms))
        if not flatten.__contains__(str(room_number)):
            raise ValueError(f"Invalid room number: {room_number}")
        else:
            self.patient_room = str(room_number)
        
            

    def set_ward(self, ward_number):
        if not WARD_NUMBERS.__contains__(ward_number):
            raise ValueError(f"Invalid ward number: {ward_number}")
        else :
            self.patient_ward = str(ward_number)
    
    def _get_patient_by_id(uri, id):
        uri = f"{API_CONTROLLER_URL}/patients/{id}"
        response = requests.get(uri)
        return response.json()

    def commit(self):
        patient_data = {
            "patient_id": self.patient_id,
            "patient_name": self.patient_name,
            "patient_age": self.patient_age,
            "patient_gender": self.patient_gender,
            "patient_checkin": self.patient_checkin,
            "patient_checkout": self.patient_checkout,
            "patient_ward": self.patient_ward,
            "patient_room": self.patient_room,
        }
        
        get = f"{API_CONTROLLER_URL}/patients"
        put = f"{API_CONTROLLER_URL}/patient/{self.patient_id}"
        response = requests.get(get).json()
        ids = [patient['patient_id'] for patient in response if patient['patient_id'] == self.patient_id]
        
        if self.patient_id in ids:
            response = requests.put(put, json=patient_data)
            if response.status_code == 200:
                print("patient commited to database")
            else:
                print("patient was not commited")

        else:
            response = requests.post(get, json=patient_data)
            if response.status_code == 200:
                print("patient commited to databasel")
            else:
                print("patient was not commited")
        
       
