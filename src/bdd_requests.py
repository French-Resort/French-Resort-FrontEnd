import requests
import os

def book_room(id_guest, id_room, check_in_date, check_out_date):
    """
    Book a room for a guest.

    Parameters:
    - id_guest (int): Guest ID.
    - id_room (int): Room ID.
    - check_in_date (str): Check-in date in the format 'YYYY-MM-DD'.
    - check_out_date (str): Check-out date in the format 'YYYY-MM-DD'.

    Returns:
    - dict: A dictionary containing the success status and data/result.
    """
    url = f"{os.getenv('API_HOST_URL', default='http://localhost:5001')}/api/booking"
    headers = {"Content-Type": "application/json"}
    data = {
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "id_guest": id_guest,
        "id_room": id_room
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()

        result = response.json()
        return {"success": True, "data": result}

    except requests.exceptions.RequestException as err:
        print(f"Response content: {response.json()}")
        error_message = f"Error: {response.json()['error']}"
        return {"success": False, "error": error_message}

def cancel_room(id_booking):
    """
    Cancel a booked room.

    Parameters:
    - id_booking (int): Booking ID.

    Returns:
    - dict: A dictionary containing the success status and data/result.
    """
    url = f"{os.getenv('API_HOST_URL', default='http://localhost:5001')}/api/booking/{id_booking}"

    try:
        response = requests.delete(url)
        response.raise_for_status()

        result = response.json()
        return {"success": True, "data": result}

    except requests.exceptions.RequestException as err:
        print(f"Response content: {response.json()}")
        error_message = f"Error: {response.json()['error']}"
        return {"success": False, "error": error_message}

def sign_up(email, password, last_name, first_name, phone_number):
    """
    Sign up a new user.

    Parameters:
    - email (str): User's email address.
    - password (str): User's password.
    - last_name (str): User's last name.
    - first_name (str): User's first name.
    - phone_number (str): User's phone number.

    Returns:
    - dict: A dictionary containing the success status and data/result.
    """
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
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()

        result = response.json()
        return {"success": True, "data": result}

    except requests.exceptions.RequestException as err:
        print(f"Response content: {response.json()}")
        error_message = f"Error: {response.json()['error']}"
        return {"success": False, "error": error_message}


def log_in(email, password):
    """
    Log in a user.

    Parameters:
    - email (str): User's email address.
    - password (str): User's password.

    Returns:
    - dict: A dictionary containing the success status and data/result.
    """
    url = f"{os.getenv('API_HOST_URL', default='http://localhost:5001')}/api/login"
    headers = {"Content-Type": "application/json"}

    data = {
        "email": email,
        "password": password
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()

        result = response.json()
        return {"success": True, "data": result}

    except requests.exceptions.RequestException as err:
        print(f"Response content: {response.json()}")
        error_message = f"Error: {response.json()['error']}"
        return {"success": False, "error": error_message}

def get_bookings(id_guest):
    """
    Get bookings for a specific guest.

    Parameters:
    - id_guest (int): Guest ID.

    Returns:
    - dict: A dictionary containing the success status and data/result.
    """
    url = f"{os.getenv('API_HOST_URL', default='http://localhost:5001')}/api/bookings/{id_guest}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        result = response.json()
        return {"success": True, "data": result}

    except requests.exceptions.RequestException as err:
        error_message = f"Error: {err}"
        return {"success": False, "error": error_message}

def get_rooms():
    """
    Get a list of available rooms.

    Returns:
    - dict: A dictionary containing the success status and data/result.
    """
    url = f"{os.getenv('API_HOST_URL', default='http://localhost:5001')}/api/rooms"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        result = response.json()
        return {"success": True, "data": result}

    except requests.exceptions.RequestException as err:
        error_message = f"Error: {err}"
        return {"success": False, "error": error_message}
