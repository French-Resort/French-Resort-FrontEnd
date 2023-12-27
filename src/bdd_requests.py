import requests

def bdd_init():
    url = "http://localhost:5001/api/db_init"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        result = response.json()
        print(result)

    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        
def check_rooms_available():
    url = "http://localhost:5001/api/rooms/available"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        result = response.json()
        print(result)
        return True

    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        return False
        
def book_room(id_guest, id_room, check_in_date, check_out_date):
    url = "http://localhost:5001/api/booking"
    headers = {"Content-Type": "application/json"}
    print(check_in_date)
    data = {
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "id_guest": id_guest,
        "id_room": id_room
    }

    try:
        response = requests.post(url, json=data, headers=headers)  # Use json parameter for JSON data
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        result = response.json()
        return result

    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        # Print additional details about the error if available
        print(f"Response content: {response.content}")
        
def sign_up(email, password, last_name, first_name, phone_number):
    url = "http://localhost:5001/api/signup"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "email": email,
        "password": password,
        "last_name": last_name,
        "first_name": first_name,
        "phone_number": phone_number
    }

    try:
        response = requests.post(url, json=data, headers=headers)  # Use json parameter for JSON data
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        result = response.json()
        print(result)

    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        # Print additional details about the error if available
        print(f"Response content: {response.content}")
        
def log_in(email, password):
    url = "http://localhost:5001/api/login"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "email": email,
        "password": password
    }

    try:
        response = requests.post(url, json=data, headers=headers)  # Use json parameter for JSON data
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        result = response.json()
        print(result)

    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        # Print additional details about the error if available
        print(f"Response content: {response.content}")
        
        