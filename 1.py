import requests
from bs4 import BeautifulSoup
import json
import subprocess 

# Function to perform the entire flow from login to buka
def complete_flow(login_api_url, deposit_api_url, deposit_now_api_url, email_value, password_value, json_file_path):
    try:
        # Step 1: Get _token and cookies from login API
        token_value, cookies, session = get_token_and_cookies(login_api_url)

        if token_value and cookies and session:
            print("Value of '_token':", token_value)

            # Step 2: Make a POST request to login
            session = post_data(login_api_url, token_value, email_value, password_value, session)

            # Step 3: Use recent cookies for the new API call to deposit
            html_response, token_value_deposit = get_html_deposit(deposit_api_url, session)

            if html_response and token_value_deposit:
                print("HTML Response from deposit API:")
                # print(html_response)

                # Step 4: Read amount and txid_details from JSON file
                amount, txid_details = read_input_data(json_file_path)

                if amount and txid_details:
                    # Step 5: Make a new POST request with additional data to deposit/now
                    gateway_code = "usdt"
                    session = post_new_data(deposit_now_api_url, token_value_deposit, gateway_code, amount, txid_details, session)

                    # Step 6: Perform additional action (e.g., calling 'buka') after successful execution
                    buka()
                else:
                    print("Error reading input data from the JSON file.")
            else:
                print("No HTML response or an error occurred.")
        else:
            print("No token value or cookies found or an error occurred.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Function to read amount and txid_details from a JSON file
def read_input_data(json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            amount = data.get('amount')
            txid_details = data.get('txid_details')
            return amount, txid_details
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file_path}' not found.")
        return None, None
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON file '{json_file_path}'.")
        return None, None

# Function to get _token and cookies from login API
def get_token_and_cookies(api_url, session=None):
    try:
        # Create a session or use the existing one
        session = session or requests.Session()

        # Make a GET request to obtain the token and cookies
        response = session.get(api_url)
        response.raise_for_status()  # Check if the request was successful (status code 200)

        # Extract cookies from the response
        cookies = response.cookies

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the input tag with the specified name
        input_tag = soup.find('input', {'name': '_token'})

        # Extract the value attribute
        if input_tag:
            token_value = input_tag.get('value')
            return token_value, cookies, session
        else:
            return None, cookies, session  # Return None if no input tag with name '_token' is found

    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return None, None, None  # Return None if an error occurs during the request

# Function to make a POST request with the token value and cookies
def post_data(api_url, token_value, email, password, session=None):
    try:
        # Create a session or use the existing one
        session = session or requests.Session()

        # Set up the POST data with the token value, email, and password
        data = {
            '_token': token_value,
            'email': email,
            'password': password
        }

        # Make the POST request with form-urlencoded data and include cookies
        response = session.post(api_url, data=data)
        response.raise_for_status()  # Check if the request was successful (status code 200)

        # Process the response as needed
        print("POST Request Response:")
        # print(response.text)

        # Return the session for subsequent requests
        return session

    except requests.exceptions.RequestException as err:
        print(f"An error occurred during the POST request: {err}")
        return None

# Function to make a GET request to a new API with recent cookies
def get_html_deposit(api_url, session=None):
    try:
        # Create a session or use the existing one
        session = session or requests.Session()

        # Make the GET request with cookies if available
        response = session.get(api_url)
        response.raise_for_status()  # Check if the request was successful (status code 200)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the input tag with the specified name
        input_tag = soup.find('input', {'name': '_token'})

        # Extract the value attribute
        if input_tag:
            token_value = input_tag.get('value')
            print("Value of '_token' in get_html_deposit:", token_value)
        else:
            print("No input tag with name '_token' found in the HTML response.")

        # Return the HTML response
        return response.text, token_value

    except requests.exceptions.RequestException as err:
        print(f"An error occurred during the GET request: {err}")
        return None, None

# Function to make a POST request to a new API with specific payload
def post_new_data(api_url, token_value, gateway_code, amount, txid_details, session=None):
    try:
        # Create a session or use the existing one
        session = session or requests.Session()

        # Set up the POST data with the token value and specific payload
        data = {
            '_token': token_value,
            'gateway_code': gateway_code,
            'amount': amount,
            'manual_data[Enter your TXID Details]': txid_details
        }

        # Make the POST request with form data and include cookies
        response = session.post(api_url, data=data)
        response.raise_for_status()  # Check if the request was successful (status code 200)

        # Process the response as needed
        print("New POST Request Response:")
        # print(response.text)

        # Return the session for subsequent requests
        return session

    except requests.exceptions.RequestException as err:
        print(f"An error occurred during the new POST request: {err}")
        return None

# Function to perform additional action after successful execution
def buka():
    print("Buka function called! Add your logic here.")
    print("\033[92mSUKSESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.\033[0m")
    subprocess.run(["python", "2.py"])

# Example usage:
login_api_url = "https://h5-international.loc-investment.com/login"  # Replace with your actual login API URL
deposit_api_url = "https://h5-international.loc-investment.com/user/deposit"  # Replace with your actual deposit API URL
deposit_now_api_url = "https://h5-international.loc-investment.com/user/deposit/now"  # Replace with your actual deposit/now API URL

email_value = "11111111"
password_value = "11111111"
json_file_path = "forbidden_from.json"  # Replace with the actual path to your JSON file

# Call the function to perform the entire flow
complete_flow(login_api_url, deposit_api_url, deposit_now_api_url, email_value, password_value, json_file_path)
