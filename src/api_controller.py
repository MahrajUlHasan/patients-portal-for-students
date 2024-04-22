from flask import Flask, request, jsonify
from patient_db import PatientDB
from patient import Patient


class PatientAPIController:

    def __init__(self):
        self.app = Flask(__name__)
        self.patient_db = PatientDB()
        self.setup_routes()
        self.run()
    def setup_routes(self):
        """
        Sets up the routes for the API endpoints.
        """
        
        self.app.route("/patients", methods=["GET"])(self.get_patients)
        self.app.route("/patients/<patient_id>", methods=["GET"])(self.get_patient)
        self.app.route("/patients", methods=["POST"])(self.create_patient)
        self.app.route("/patient/<patient_id>", methods=["PUT"])(self.update_patient)
        self.app.route("/patient/<patient_id>", methods=["DELETE"])(self.delete_patient)

    def create_patient(self):
        """
        Creates a new patient record in the database.

        Returns:
            JSON: A JSON response with the created patient data or an error message.
        """
        try:

            data = request.get_json()
            if not data:
                return jsonify({"error": "Missing patient data in request body"}), 400

            patient_id = self.patient_db.insert_patient(data)
            if patient_id == None:
                return jsonify({"error": "Failed to create patient"}), 400

            new_patient = self.patient_db.fetch_patient_id_by_name(data["patient_name"])

            return jsonify(new_patient), 200

        except Exception as e:
            print(f"Error creating patient: {e}")
            return jsonify({"error": "Internal server error"}), 500

    # def get_patients(self):
    #     """
    #     Retrieves all patient records from the database.

    #     Returns:
    #         JSON: A JSON list of all patient records.
    #     """
    #     patients = self.patient_db.select_all_patients()
    #     if not patients:
    #         return jsonify({"message": "No patients found"}), 200
    #     return jsonify(patients), 200

    def get_patient(self, patient_id):
        """
        Retrieves a specific patient record based on the ID.

        Args:
            patient_id (str): The ID of the patient.

        Returns:
            JSON: A JSON object representing the patient record or an error message.
        """
        patient = self.patient_db.select_patient(patient_id)
        if not patient:
            return jsonify({"error": f"Patient with ID {patient_id} not found"}), 404
        return jsonify(patient), 200

    def update_patient(self, patient_id):
        """
        Updates an existing patient record in the database.

        Args:
            patient_id (str): The ID of the patient to update.

        Returns:
            JSON: A JSON response indicating success or failure.
        """
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Missing patient data in request body"}), 400

            affected_rows = self.patient_db.update_patient(patient_id, data)
            if affected_rows == 0:
                return jsonify({"error": f"Patient with ID {patient_id} not found"}), 404
            return jsonify({"message": "Patient updated successfully"}), 200

        except Exception as e:
            print(f"Error updating patient: {e}")
            return jsonify({"error": "Internal server error"}), 500
    def delete_patient(self, patient_id):
        
        try:
            affected_rows = self.patient_db.delete_patient(patient_id)
            print(affected_rows)
            if affected_rows is not None:
                return jsonify({"message": "Patient deleted successfully."}), 200
            else:
                return jsonify({"error": "Failed to delete patient."}), 400
        except Exception as e:
            return jsonify({"error":str(e)}), 400
        
    def run(self):
        """
        Runs the Flask application.
        """
        self.app.run()
    

    def get_patients(self):

        search_name = request.args.get("search_name") 
        if search_name == None:
            patients = self.patient_db.select_all_patients()
            if not patients:
                return jsonify({"message": "No patients found"}), 200
            return jsonify(patients), 200
        else:
            patient_ids = self.patient_db.fetch_patient_id_by_name(search_name)
            if not patient_ids:
                return jsonify({"message": "No patients found with that name"}), 200

            patients = []
            for patient_id in patient_ids:
                patient = self.patient_db.select_patient(patient_id["patient_id"])
                patients.append(patient)

            return jsonify(patients), 200



PatientAPIController()
