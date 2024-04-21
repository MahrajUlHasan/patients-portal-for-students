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

    def __init__(self, name, age, gender):
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
        self.patient_ward = random.choice(WARD_NUMBERS)
        self.patient_room = random.choice(ROOM_NUMBERS[self.patient_ward])
      
        

    def _validate_gender(self, gender):
        """
        Validates the provided gender against the available options in `config.GENDERS`.

        Args:
            gender (str): The gender to validate.

        Returns:
            str: The validated gender if valid, otherwise raises a ValueError.

        Raises:
            ValueError: If the provided gender is not in `config.GENDERS`.
        """

        if gender not in GENDERS:
            raise ValueError(f"Invalid gender: {gender}. Valid options are: {', '.join(GENDERS)}")
        return gender

    def _validate_age(self, age):
        """
        Validates the provided age to be a positive integer.

        Args:
            age (int): The age to validate.

        Raises:
            ValueError: If the provided age is not a positive integer.
        """
        if not isinstance(age, int) or age <= 0:
            raise ValueError(f"Invalid age: {age}. Age must be a positive integer.")

    def update_room_and_ward(self, ward_number, room_number):
        """
        Updates the patient's ward and room number, performing validation.

        Args:
            ward_number (int): The new ward number for the patient.
            room_number (str): The new room number for the patient.

        Raises:
            ValueError: If the ward number is invalid or the room number is not valid for the chosen ward.
        """

        if ward_number not in WARD_NUMBERS:
            raise ValueError(f"Invalid ward number: {ward_number}. Valid options are: {', '.join(map(str, WARD_NUMBERS))}")

        if room_number not in ROOM_NUMBERS[ward_number]:
            raise ValueError(f"Invalid room number: {room_number} for ward {ward_number}. Valid options are: {', '.join(ROOM_NUMBERS[ward_number])}")

        self.patient_ward = ward_number
        self.patient_room = room_number

    

def commit_to_database(self, api_controller_url):
    """
    Commits the patient information to the database using the provided API controller URL.

    This method sends a POST request to the API controller endpoint (assumed to be "/patients") with the patient data as JSON.

    Args:
        api_controller_url (str): The base URL of the API controller.

    Raises:
        ConnectionError: If there's an issue connecting to the API controller.
        RequestException: If there's an error during the request.
    """

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

    endpoint = f"{api_controller_url}/patients"
    try:
        response = requests.post(endpoint, json=patient_data)
        response.raise_for_status() 

        print(f"Patient data successfully committed. Response: {response.text}")
    except (requests.exceptions.RequestException, ConnectionError) as e:
        print(f"Error committing patient data to API controller: {e}")

        
       
