import requests
import os

def book_room(id_guest, id_room, check_in_date, check_out_date):
    url = f"{os.getenv('API_HOST_URL', default='http://localhost:5001')}/api/booking"
    headers = {"Content-Type": "application/json"}
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
        return {"success": True, "data": result}

    except requests.exceptions.RequestException as err:
        # Print additional details about the error if available
        print(f"Response content: {response.json()}")
        error_message = f"Error: {response.json()['error']}"
        return {"success": False, "error": error_message}
    
def cancel_room(id_booking):
    url = f"{os.getenv('API_HOST_URL', default='http://localhost:5001')}/api/booking/{id_booking}"

    try:
        response = requests.delete(url)  # Use json parameter for JSON data
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        result = response.json()
        return {"success": True, "data": result}

    except:
        # Print additional details about the error if available
        print(f"Response content: {response.json()}")
        error_message = f"Error: {response.json()['error']}"
        return {"success": False, "error": error_message}
        
def sign_up(email, password, last_name, first_name, phone_number):
    url = f"{os.getenv('API_HOST_URL', default='http://localhost:5001')}/api/signup"
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
        return {"success": True, "data": result}

    except:
        print(f"Response content: {response.json()}")
        error_message = f"Error: {response.json()['error']}"
        return {"success": False, "error": error_message}
        
def log_in(email, password):
    url = f"{os.getenv('API_HOST_URL', default='http://localhost:5001')}/api/login"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "email": email,
        "password": password
    }

    try:
        response = requests.post(url, json=data, headers=headers)  # Use json parameter for JSON data
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        result = response.json()
        return {"success": True, "data": result}

    except:
        print(f"Response content: {response.json()}")
        error_message = f"Error: {response.json()['error']}"
        return {"success": False, "error": error_message}
        
def get_bookings(id_guest):
    url = f"{os.getenv('API_HOST_URL', default='http://localhost:5001')}/api/bookings/{id_guest}"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)  # Use json parameter for JSON data
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        result = response.json()
        return {"success": True, "data": result}

    except requests.exceptions.RequestException as err:
        # Print additional details about the error if available
        # print(f"Response content: {response.content}")
        error_message = f"Error: {err}"
        return {"success": False, "error": error_message}
            
def get_rooms():
    url = f"{os.getenv('API_HOST_URL', default='http://localhost:5001')}/api/rooms"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)  # Use json parameter for JSON data
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        result = response.json()
        return {"success": True, "data": result}

    except requests.exceptions.RequestException as err:
        # Print additional details about the error if available
        # print(f"Response content: {response.content}")
        error_message = f"Error: {err}"
        return {"success": False, "error": error_message}