# authenticator.py

import requests

auth_url = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'

#valid login details for testing purposes
email = 'tim@plymouth.ac.uk'
password = 'COMP2001!'




def Authenticate(email, password):
    credentials = {
        'email': email,
        'password': password
    }
 
    response = requests.post(auth_url, json=credentials)

    if response.status_code == 200:
        try:
            json_response = response.json()
            print("Authenticated successfully:", json_response)
            if json_response[1] == "True":
                return True
            else:
                return False
        except requests.JSONDecodeError:
            print("Response is not valid JSON. Raw response content:")
            print(response.text)
            return False
    else:
        print(f"Authentication failed with status code {response.status_code}")
        print("Response content:", response.text)
        return False