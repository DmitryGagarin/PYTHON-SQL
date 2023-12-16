from database import database
from datetime import datetime
from utils import *

# function that starts the program and controls main flow
def app() -> None:
    # db_path = input("Insert db path: ") <-- you can uncomment this line if you have several databases, and you need certain path to the database
    global db
    db = database('hospital.db')  # if you want to have certain path - change 'hospital.db' to db_path
    while True:
        print_menu(menu)
        command = get_input(input('>>> '), 0, 13)
        if command in menu.keys():
            menu[command]['func']()


# CRUD principle - create, read, update, delete
# function that creates (adds) new employee to the database
def add_employee():
    print(OKGREEN + "*****ADD EMPLOYEE*****" + ENDC)
    name = input('Insert name ')
    surname = input('Insert surname ')
    phone = input('Insert phone ')
    passport = input('Insert passport information ')
    speciality = input('Insert speciality ')
    print(OKGREEN + "*****available clinics*****" + ENDC)
    show_clinics()
    print(OKGREEN + "**********" + ENDC)
    clinic_id = input('Insert clinic id ')

    # validation
    if (
            len(name) <= 2 or
            len(surname) == 0 or
            len(phone) == 0 or
            len(passport) == 0 or
            len(speciality) == 0 or
            len(clinic_id) == 0):
        print(FAIL + "You forgot to insert non-empty values" + ENDC)
    else:
        request = f'INSERT INTO employee VALUES (NULL, (SELECT id FROM clinic WHERE id = "{clinic_id}"), "{name}",  "{surname}",  "{phone}",  "{passport}",  "{speciality}");'
        response = db.raw(request)
        if not response:
            print(FAIL + "Input error of employee addition failed" + ENDC)
        print(OKGREEN + "*****EMPLOYEE WAS ADDED*****" + ENDC)


# function that reads all employees values
def show_employee():
    while True:
        desire_of_order = input("Do you want to show their names in order? 1 - yes; 2 - no ")
        if desire_of_order.isdigit():  # Check if the input is a digit
            desire_of_order = int(desire_of_order)
            if desire_of_order == 1 or desire_of_order == 2:
                print(OKGREEN + "*****READ ALL EMPLOYEES*****" + ENDC)
                if desire_of_order == 2:
                    show_employee_no_order()
                else:
                    show_employee_in_order()
                print(OKGREEN + "*****ALL EMPLOYEE READING ENDED*****" + ENDC)
                break  # This will break the loop and end the function
        else:
            print(FAIL + "Please enter a valid input (1 or 2)" + ENDC)
            break


# function that's called when we don't want to have order in showing employees
def show_employee_no_order():
    print(OKCYAN + UNDERLINE + "\t".join(formatted_employee_headers) + ENDC)
    request = show_employee_request
    response = db.raw(request)
    for row in response:
        formatted_row = [
            str(row["id"]).ljust(15),
            row["clinic_name"].ljust(15),
            row["name"].ljust(15),
            row["surname"].ljust(15),
            row["phone"].ljust(15),
            row["passport"].ljust(15),
            row["speciality"].ljust(15)
        ]
        print("\t".join(formatted_row))


# function that's called when we do want to have order in showing employees, and it gives types of sorting
def show_employee_in_order():
    while True:
        order = input("Choose sort order: (ASC (from a to z) / DESC (from z to a)) ")
        if order.lower() == "asc" or order.lower() == "desc":
            print(OKCYAN + UNDERLINE + "\t".join(formatted_employee_headers) + ENDC)
            request = (f'SELECT employee.id, '
                       f'employee.name, '
                       f'employee.surname, '
                       f'employee.phone, '
                       f'employee.passport, '
                       f'employee.speciality, '
                       f'clinic.name AS clinic_name '
                       f'FROM employee JOIN clinic ON clinic.id = employee.clinic_id ORDER BY employee.surname {order.upper()};')
            response = db.raw(request)
            for row in response:
                formatted_row = [
                    str(row["id"]).ljust(15),
                    row["clinic_name"].ljust(15),
                    row["name"].ljust(15),
                    row["surname"].ljust(15),
                    row["phone"].ljust(15),
                    row["passport"].ljust(15),
                    row["speciality"].ljust(15)
                ]
                print("\t".join(formatted_row))
            break  # This will break the loop and end the function
        else:
            print(FAIL + "Please enter either 'ASC' or 'DESC'" + ENDC)
            break


# function that deletes employee depends on its id
def delete_employee():
    print(OKGREEN + "*****LIST OF EMPLOYEES*****" + ENDC)
    show_employee_no_order()
    print(OKGREEN + "*****LIST OF EMPLOYEES ENDED*****" + ENDC)
    employee_id = int(input("Insert employee id to delete "))
    request = f'DELETE FROM employee WHERE id = {employee_id};'
    response = db.raw(request)
    if response:
        print(WARNING + "Employee was fired" + ENDC)
    else:
        print(FAIL + "Error occurred, impossible to fire employee" + ENDC)
    print(OKGREEN + "*****EMPLOYEE DELETING ENDED*****" + ENDC)


# function that updates some employee values
def change_employee_data():
    while True:
        print(OKGREEN + "*****CHANGE EMPLOYEE DATA*****" + ENDC)
        print(OKGREEN + "*****LIST OF EMPLOYEES*****" + ENDC)
        show_employee_no_order()
        print(OKGREEN + "*****LIST OF EMPLOYEES ENDED*****" + ENDC)
        try:  # here starts the validation of the user input
            employee_id = int(input("Insert employee id you want to change information "))
        except ValueError:
            print("Invalid input. Please enter a valid employee id.")
            continue
        print_menu(menu_change_employee)
        command = get_input(input('>>> '), 1, 6)
        if command is None:
            print(FAIL + "You haven't chosen anything to change" + ENDC)
            continue
        if command in menu_change_employee.keys():
            field: str = menu_change_employee[command]['field']
            value = input(f'Insert {field}: ')
            request = f'UPDATE employee SET {field} = "{value}" WHERE id = {employee_id};'
            response = db.raw(request)
            if response:
                print(f'You have changed {field}')
            else:
                print(FAIL + f'Impossible to change {field}' + ENDC)
        print(OKGREEN + "*****EMPLOYEE DATA CHANGING ENDED*****" + ENDC)
        break


# function that reads all appointments
def select_appointment():
    appointment_header = ['ID', 'Employee_id', 'Patient_id', 'Service_id', 'Date',
                          'Time']  # headers for showing appointments
    formatted_appointment_headers = [header.ljust(15) for header in
                                     appointment_header]  # creating spaces between headers
    print(OKGREEN + "*****SELECT APPOINTMENT*****" + ENDC)
    limit = int(input('How many lines you want to output? '))
    request = f'SELECT * FROM appointment LIMIT {limit}'
    response = db.raw(request)
    print(OKCYAN + UNDERLINE + "\t".join(formatted_appointment_headers) + ENDC)
    for row in response:
        formatted_row = [
            str(row["id"]).ljust(15),
            str(row["employee_id"]).ljust(15),
            str(row["patient_id"]).ljust(15),
            str(row["service_id"]).ljust(15),
            row["date"].ljust(15),
            row["time"].ljust(15)
        ]
        print("\t".join(formatted_row))
    print(OKGREEN + "*****APPOINTMENT SELECTION ENDED*****" + ENDC)


# function that creates new service
def create_service():
    print(OKGREEN + "*****ADD SERVICE*****" + ENDC)
    name = input('Insert name ')
    cost = input('Insert cost ')
    description = input('Insert description ')
    # validation
    if (
            len(name) == 0 or
            len(cost) == 0 or
            len(description) == 0):
        print("You forgot to insert non-empty values")
    else:
        request = f'INSERT INTO service VALUES (NULL, "{name}",  "{cost}",  "{description}");'
        response = db.raw(request)
        if not response:
            print(FAIL + "Input error. Service addition failed" + ENDC)
    print(OKGREEN + "*****SERVICE WAS ADDED*****" + ENDC)


# function that reads all services
def select_service():
    service_header = ['Id', 'Name', 'Cost', 'Description']  # headers for showing services
    formatted_service_headers = [header.ljust(15) for header in service_header]  # creating spaces between headers
    print(OKGREEN + "*****SELECT SERVICE*****" + ENDC)
    request = f'SELECT * FROM service'
    response = db.raw(request)
    print(OKCYAN + UNDERLINE + "\t".join(formatted_service_headers) + ENDC)
    for row in response:
        formatted_row = [
            str(row["id"]).ljust(15),
            row["name"].ljust(15),
            str(row["cost"]).ljust(15),
            row["description"].ljust(15)
        ]
        print("\t".join(formatted_row))
    print(OKGREEN + "*****SERVICE SELECTION ENDED*****" + ENDC)


# function that shows list of clinics with their ids and names
def show_clinics():
    request = 'SELECT * FROM clinic'
    response = db.raw(request)
    for clinic in response:
        print(clinic['id'], clinic['name'])


# function that gives all workers who work in the certain clinic
def show_employee_by_clinic():
    print(OKGREEN + "*****CLINICS LISTED*****" + ENDC)
    show_clinics()
    print(OKGREEN + "*****CLINICS LISTING ENDED*****" + ENDC)
    clinic_id = input("Enter the clinic id in which you want to see employees: ")
    print(OKGREEN + "*****EMPLOYEES LISTING*****" + ENDC)
    print(OKCYAN + UNDERLINE + "\t".join(formatted_employee_headers) + ENDC)

    employee_request = f'SELECT * FROM employee WHERE clinic_id = {clinic_id}'
    employees = db.raw(employee_request)

    for row in employees:
        formatted_row = [
            str(row["id"]).ljust(15),
            str(row["clinic_id"]).ljust(15),
            row["name"].ljust(15),
            row["surname"].ljust(15),
            row["phone"].ljust(15),
            row["passport"].ljust(15),
            row["speciality"].ljust(15)
        ]
        print("\t".join(formatted_row))

    print(OKGREEN + "*****EMPLOYEES LISTING ENDED*****" + ENDC)


# here we start the same thing as it was with employees. We have to add, read, update and delete patients
# function that creates new patient (this function is huge because we need to create appointment according to patient info)
def add_patient():
    # user input of patient data
    print(OKGREEN + "*****ADD PATIENT*****" + ENDC)
    show_clinics()
    clinic_id = input('Insert clinic id: ')
    select_service()
    service_id = input('Insert service id: ')
    name = input('Insert name: ')
    surname = input('Insert surname: ')
    phone = input('Insert phone: ')
    birthday = input('Insert birthday (YYYY-MM-DD): ')

    # Validation
    if (
            len(clinic_id) == 0 or
            len(service_id) == 0 or
            len(name) == 0 or
            len(surname) == 0 or
            len(phone) == 0 or
            len(birthday) == 0):
        print("You forgot to insert non-empty values")
    else:
        # connecting patient with the certain clinic
        clinic_request = f'SELECT id FROM clinic WHERE id = "{clinic_id}"'
        clinic_result = db.raw(clinic_request)

        if clinic_result:  # Check if result is not empty
            clinic_id = clinic_result[0]['id']

            # giving patient his appointment number by taking the id of the last appointment
            appointment_id_request = 'SELECT MAX(id) AS last_id FROM appointment'
            appointment_id_result = db.raw(appointment_id_request)

            if appointment_id_result:
                appointment_id = appointment_id_result[0]['last_id']
                appointment_id_final = appointment_id + 1
            else:
                appointment_id_final = 0

            # Insert new patient
            request = f'INSERT INTO patient VALUES (NULL, {clinic_id}, {service_id}, "{name}", "{surname}", "{phone}", "{birthday}", {appointment_id_final})'
            response = db.raw(request)

            if not response:
                print("Input error of patient addition")
            else:
                # Get the newly inserted patient's ID
                new_patient_request = f'SELECT id FROM patient WHERE name = "{name}" AND surname = "{surname}"'
                new_patient_result = db.raw(new_patient_request)
                if new_patient_result:
                    new_patient_id = new_patient_result[0]['id']

                    # Display a list of employees working in the chosen clinic
                    employee_request = f'SELECT id, name FROM employee WHERE clinic_id = {clinic_id}'
                    employee_result = db.raw(employee_request)
                    if employee_result:
                        print("Available Employees:")
                        for employee in employee_result:
                            print(f"{employee['id']}: {employee['name']}")

                        employee_id = input("Choose an employee ID: ")

                        # Create a new appointment for the patient with the selected employee
                        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        appointment_request = f'INSERT INTO appointment (employee_id, patient_id, service_id, date, time) VALUES ({employee_id}, {new_patient_id}, {service_id}, "{current_datetime}", "{current_datetime}")'
                        appointment_response = db.raw(appointment_request)

                        if not appointment_response:
                            print("Failed to create an appointment.")
                        else:
                            print("*****PATIENT AND APPOINTMENT WERE ADDED*****")
                    else:
                        print("No employees found in the chosen clinic.")
                else:
                    print("Failed to retrieve the newly added patient.")
        else:
            print("Clinic not found")


# function that shows all patient (without any order)
def show_patient():
    patient_headers = ['ID', 'Clinic', 'Service', 'Name', 'Surname', 'Phone',
                       'Birthday']  # headers for showing patients
    formatted_patient_headers = [header.ljust(15) for header in
                                 patient_headers]  # creating spaces between headers
    print(OKCYAN + UNDERLINE + "\t".join(formatted_patient_headers) + ENDC)
    request = (
        f'SELECT patient.id, clinic.name AS clinic_name, service.name AS service_name, '
        f'patient.name, patient.surname, patient.phone, patient.birthday '
        f'FROM patient '
        f'LEFT JOIN clinic ON clinic.id = patient.clinic_id '
        f'LEFT JOIN service ON service.id = patient.service_id'
    )
    # response = db.raw(request)
    response = db.raw(request)

    if not isinstance(response, bool):  # Check if response is not a boolean
        print(OKGREEN + "*****LIST OF PATIENTS*****" + ENDC)
        for row in response:
            formatted_row = [
                str(row["id"]).ljust(15),
                str(row["clinic_name"]).ljust(15),
                str(row["service_name"]).ljust(15),
                row["name"].ljust(15),
                row["surname"].ljust(15),
                row["phone"].ljust(15),
                row["birthday"].ljust(15)
            ]
            print("\t".join(formatted_row))
    else:
        print(FAIL + "No patient data found." + ENDC)

    print(OKGREEN + "*****LIST OF PATIENTS ENDED*****" + ENDC)


# function that deletes patient
def delete_patient():
    print(OKGREEN + "*****LIST OF PATIENTS*****" + ENDC)
    show_patient()
    patient_id = int(input("Insert patient id to delete "))
    request = f'DELETE FROM patient WHERE id = {patient_id};'
    response = db.raw(request)
    if not response:
        print(FAIL + "Error occurred, impossible to delete patient" + ENDC)
    print(OKGREEN + "*****PATIENT DELETING ENDED*****" + ENDC)


# function that changes some patient data
def change_patient_data():
    while True:
        print(OKGREEN + "*****CHANGE PATIENT DATA*****" + ENDC)
        print(OKGREEN + "*****LIST OF PATIENT*****" + ENDC)
        show_patient()
        try:  # here starts the validation of the user input
            patient_id = int(input("Insert patient id you want to change information "))
        except ValueError:
            print(FAIL + "Invalid input. Please enter a valid employee id." + ENDC)
            continue
        print_menu(menu_change_patient)
        command = get_input(input('>>> '), 1, 6)
        if command is None:
            print(FAIL + "You haven't chosen anything to change" + ENDC)
            continue
        if command in menu_change_patient.keys():
            field: str = menu_change_patient[command]['field']
            value = input(f'Insert {field}: ')
            request = f'UPDATE patient SET {field} = "{value}" WHERE id = {patient_id};'
            response = db.raw(request)
            if response:
                print(f'You have changed {field}')
            else:
                print(FAIL + f'Impossible to change {field}' + ENDC)
        print(OKGREEN + "*****PATIENT DATA CHANGING ENDED*****" + ENDC)
        break


def show_clinics_data():
    clinic_header = ['Id', 'Name', 'Address']  # headers for showing clinics
    formatted_clinic_headers = [header.ljust(15) for header in clinic_header]  # creating spaces between headers
    request = 'SELECT * FROM clinic'
    response = db.raw(request)
    print(OKGREEN + "*****LIST OF CLINICS*****" + ENDC)
    print(OKCYAN + UNDERLINE + "\t".join(formatted_clinic_headers) + ENDC)
    for row in response:
        formatted_row = [
            str(row["id"]).ljust(15),
            row["name"].ljust(15),
            row["address"].ljust(15)
        ]
        print("\t".join(formatted_row))
    print(OKGREEN + "*****LIST OF CLINICS ENDED*****" + ENDC)


# function that's called when we want to leave / stop the program
def close() -> None:
    exit()


# dictionary that compares user input with the text and functions
menu: dict = {
    1: {'func': add_employee, 'desc': 'add employee'},
    2: {'func': show_employee, 'desc': 'show employee'},
    3: {'func': delete_employee, 'desc': 'delete employee'},
    4: {'func': change_employee_data, 'desc': 'change employee data'},
    5: {'func': select_appointment, 'desc': 'show appointment'},
    6: {'func': create_service, 'desc': 'create service'},
    7: {'func': select_service, 'desc': 'show services'},
    8: {'func': show_employee_by_clinic, 'desc': 'show clinic employees'},
    9: {'func': add_patient, 'desc': 'add patient'},
    10: {'func': show_patient, 'desc': 'show patient'},
    11: {'func': delete_patient, 'desc': 'delete patient'},
    12: {'func': change_patient_data, 'desc': 'change patient'},
    13: {'func': show_clinics_data, 'desc': 'show clinics data'},
    0: {'func': close, 'desc': 'exit'}
}

# dictionary that compares user input with the text and functions in change_employee_data() function
menu_change_employee: dict = {
    1: {'desc': "change employee's clinic", 'field': 'clinic_id'},
    2: {'desc': 'change name', 'field': 'name'},
    3: {'desc': 'change surname', 'field': 'surname'},
    4: {'desc': 'change phone', 'field': 'phone'},
    5: {'desc': 'change passport data', 'field': 'passport'},
    6: {'desc': 'change speciality', 'field': 'speciality'}
}

# dictionary that compares user input with the text and functions in change_patient_data() function
menu_change_patient: dict = {
    1: {'desc': "change patient's clinic", 'field': 'clinic_id'},
    2: {'desc': "change patient's service", 'field': 'service_id'},
    3: {'desc': 'change name', 'field': 'name'},
    4: {'desc': 'change surname', 'field': 'surname'},
    5: {'desc': 'change phone', 'field': 'phone'},
    6: {'desc': 'change birthday', 'field': 'birthday'},
}


# function that prints different menus depending on the attribute
def print_menu(functions_list: dict):
    for variant in functions_list:
        print(f'{variant} - {functions_list[variant]["desc"]}')


# a condition that starts main flow
if __name__ == '__main__':
    app()
