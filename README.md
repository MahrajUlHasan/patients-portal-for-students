# Patients Portal

## Introduction

Patient Portal is a basic Patient management system, where the user (i.e., receptionist) can perform the following tasks:
- **List Patients**
- **List Patients with a given name**
- **Read a Patient with a certain ID**
- **Create a Patient**
- **Update the data of a Patient**
- **Delete a Patient**

## Prerequisites

- Install **Python** (recommended version >= 3.10)
- Install **Gitbash** (Optional)

## Installation Steps

Follow these steps to install the repository requirements:

1. **Fork this Repository**
Click on the Fork button
Then, rename the repo name to *patients-portal* and click Create Fork.

2. **Clone the Repository from your list of repositories:**

```bash
git clone https://github.com/<your-username>/patients-portal.git
```

3. **Navigate to the Repository:**
```bash
cd patients-portal
```

4. **Create a virtual environment**
```bash
python -m venv venv
```

5. **Activate the virtual environment**

*In Linux (Gitbash)*

```bash
source venv/bin/activate
```

*In Windows*
```bash
.\\venv\Scripts\activate.bat
```

6. **Install Python packages to run the application**
```bash
python -m pip install -r requirements.txt
```

## Testing the APIs
You can use Git Bash to execute these shell commands if you don't have Linux or WSL.

In Terminal:

First, run the Flask server by running the API_CONTROLLER (`src/api_controller.py`) directly or using the Linux command:
```bash
python src/api_controller.py
```
Once the Flask server is running, open a new terminal and keep the server running in the first one.

Then,
```bash
cd tests
```

Then,
```bash
bash create_patient.sh
```

If it returns the patient_id in the response, it means that the patient has been created successfully and added to the database.

Then, for listing the created patients,
```bash
bash list_patients.sh
```

Then, for listing the created patients with *name* as a parameter,
```bash
bash list_patient_by_name.sh
```

Then, for getting patient details with a certain ID,
```bash
bash get_certain_patient.sh
```

Then, to update the patient,
```bash
bash update_patient.sh
```

Finally, to delete the created patient,
```bash
bash delete_patient.sh
```

## Testing the Final Application
This is an E2E test case, which is going to test the functionality of the patient portal:

It creates the patient object from the Patient class and commits the patient to the database using the client request.

Test 1 (basic):
Simple test case for creating the patient object and committing it.

Test 2 (validation of room and ward):
It is invoked after Test 1 for the same patient. Therefore, you need to think of the business logic for the commit method in `patient.py` that when the first patient is created, it cannot be created again; therefore, it has to be updated using a (PUT) request.

```bash
python src/test_application.py
```

## References:

- Flask Documentation: https://flask.palletsprojects.com/en/3.0.x/quickstart/#routing
- Flask Cheatsheet: https://s3.us-east-2.amazonaws.com/prettyprinted/flask_cheatsheet.pdf
- Swagger Editor (Playground): https://editor.swagger.io/
- Python OOP: https://docs.python.org/3/tutorial/classes.html
