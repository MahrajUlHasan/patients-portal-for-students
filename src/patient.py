from datetime import datetime
import uuid
import requests
import random

from config import GENDERS, WARD_NUMBERS, ROOM_NUMBERS , API_CONTROLLER_URL
from patient_db_config import PATIENTS_TABLE
from patient_db import PatientDB


class Patient:
    """
    Patient model representing a patient in the hospital system.

    Attributes:
        patient_id (str): Unique identifier for the patient (generated using UUID).
        patient_name (str): Name of the patient.
        patient_age (int): Age of the patient.
        patient_gender (str): Gender of the patient (must be in `config.GENDERS`).
        patient_checkin (str): Date and time of patient check-in (automatically set).
        patient_checkout (str): Date and time of patient check-out (initially None).
        patient_ward (int): Ward number where the patient is located (must be in `config.WARD_NUMBERS`).
        patient_room (str): Room number within the ward where the patient is located (must be a valid room based on `config.ROOM_NUMBERS`).
    """

    def __init__(self, name,gender,age):
        """
        Initializes a new Patient instance.

        Args:
            name (str): Name of the patient.
            age (int): Age of the patient.
            gender (str): Gender of the patient.

        Raises:
            ValueError: If gender is invalid or age is not a positive integer.
        """

        self.patient_id = str(uuid.uuid4())
        self.patient_name = name
        self.patient_age = self._validate_age(age)
        self.patient_gender = self._validate_gender(gender)
        self.patient_checkin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_checkout = None
        self.patient_ward = None
        self.patient_room = None
    def get_id(self):
        return self.patient_id
    def get_name(self):
        return self.patient_name
    def get_age(self):
        return self.patient_age
    def get_gender(self):
        return self.patient_gender
    def get_room(self):
        return self.patient_room
    def get_ward(self):
        return self.patient_ward
        

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
        if room_number not in ROOM_NUMBERS:
            raise ValueError(f"Invalid room number: {room_number} for ward {self.patient_ward}. Valid options are: {', '.join(ROOM_NUMBERS)}")
        self.patient_room = room_number

    def set_ward(self, ward_number):
        if ward_number not in WARD_NUMBERS:
            raise ValueError(f"Invalid ward number: {ward_number}. Valid options are: {', '.join(WARD_NUMBERS)}")
        self.patient_ward = ward_number
    

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

        url = f"{API_CONTROLLER_URL}/patients"
        try:
            response = requests.post(url, json=patient_data)
            response.raise_for_status() 

            print(f"Patient data successfully committed. Response: {response.text}")
        except (requests.exceptions.RequestException, ConnectionError) as e:
            print(f"Error committing patient data to API controller: {e}")

        
       
