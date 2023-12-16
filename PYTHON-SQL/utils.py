# COLORS THAT ARE USED TO COLOR THE OUTPUT
HEADER = '\033[95m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# VARIABLES AND CONSTANTS THAT ARE IN SHOW EMPLOYEE FUNCTION
show_employee_request = (f'SELECT employee.id, '  # default select request
                         f'employee.name, '
                         f'employee.surname, '
                         f'employee.phone, '
                         f'employee.passport, '
                         f'employee.speciality, '
                         f'clinic.name AS clinic_name '
                         f'FROM employee JOIN clinic ON clinic.id = employee.clinic_id;')

employee_headers = ['ID', 'Clinic', 'Name', 'Surname', 'Phone', 'Passport',
                    'Speciality']  # headers that are used for beauty
formatted_employee_headers = [header.ljust(15) for header in
                              employee_headers]  # we make spaces between headers to have space for values


# function that analyzes user's input
def get_input(value: str, min_value: int, max_value: int) -> int or None:
    if value.isdigit():
        num = int(value)
        if min_value <= num <= max_value:
            return num
        else:
            print(
                FAIL + f"The input value {num} is out of range. Please enter a number between {min_value} and {max_value}." + ENDC)
    else:
        print(FAIL + "You have input a string, but you need to input an integer." + ENDC)
    return None


# function that prints different menus depending on the attribute
def print_menu(functions_list: dict):
    for variant in functions_list:
        print(f'{variant} - {functions_list[variant]["desc"]}')



# function that's called when we want to leave / stop the program
def close() -> None:
    exit()

