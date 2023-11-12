import requests
import time
import json
import subprocess 

def run_send_script():
    try:
        subprocess.run(['python', 'send.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running the send.py script: {e}")
def load_forbidden_from(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data.get('forbidden_from', '')
    except Exception as e:
        print(f"An error occurred while loading forbidden_from from file: {e}")
        return ''

def save_to_json(data, filename, amount=None, txid_details=None):
    try:
        data_to_save = {'forbidden_from': data}

        # Add amount and txid_details if provided
        if amount is not None:
            data_to_save['amount'] = amount
        if txid_details is not None:
            data_to_save['txid_details'] = txid_details

        with open(filename, 'w') as file:
            json.dump(data_to_save, file, indent=2)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving data to file: {e}")

def call_api(api_url):
    try:
        # Make a GET request to the API
        response = requests.get(api_url)
        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def check_api_response(response, expected_hash, forbidden_from):
    if response is not None:
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("API request successful")
            data_from_api = response.json()

            # Check if the hash value is in the data and matches the expected value
            if 'data' in data_from_api and data_from_api['data']:
                first_data_item = data_from_api['data'][0]
                if 'to' in first_data_item and first_data_item['to'] == expected_hash:
                    print(f"Received a response with the expected hash value: {expected_hash}")

                    # Check if the "from" value is not in the forbidden_from list
                    if 'hash' in first_data_item and first_data_item['hash'] != forbidden_from:
                        print(f"Received a response with 'from' value not matching the forbidden value: {forbidden_from}")

                        # Save the 'from' value, amount, and txid_details to a JSON file
                        save_to_json(first_data_item['hash'], 'forbidden_from.json', amount=first_data_item['amount'][:-6], txid_details=first_data_item['hash'])

                        return data_from_api
                    else:
                        print(f"'from' value matches the forbidden value. Printing 'from' value and retrying...\n")
                        print(f"'from' value: {forbidden_from}")
                        return None
                else:
                    print(f"Response does not match the expected hash value. Retrying...\n")
                    return None
            else:
                print("No data or empty data received. Retrying...\n")
                return None
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    else:
        print("No response received")
        return None

def call_api_until_valid(api_url, expected_hash, forbidden_from):
    max_attempts = 50000  # You can adjust the maximum number of attempts
    current_attempt = 1

    while current_attempt <= max_attempts:
        print(f"Attempt {current_attempt} to call the API")

        # Call the API
        api_response = call_api(api_url)

        # Check the API response
        data_from_api = check_api_response(api_response, expected_hash, forbidden_from)

        # If the response is valid, return it
        if data_from_api is not None:
            return data_from_api

        # Wait for a short time before the next attempt
        time.sleep(2)

        current_attempt += 1

    print("\033[91mMaximum attempts reached. Unable to obtain a valid response.\033[0m")
    return None

def print_specific_info(valid_response):
    if valid_response is not None:
        # Assuming valid_response structure, modify this according to the actual structure
        data = valid_response.get('data', [])

        # Check if there is at least one item in the 'data' list
        if data:
            # Assuming there is only one item in the 'data' list
            first_data_item = data[0]

            # Extract and print specific information
            amount = first_data_item.get('amount', 'N/A')
            txid_details = first_data_item.get('hash', 'N/A')
            sliced_amount = amount[:-6]

            print(f"\033[92mAmount: {sliced_amount}\033[0m")
            print(f"\033[92mTxid_details: {txid_details}\033[0m")
            subprocess.run(["python", "send.py"])
        else:
            print("No data available in the response.")
    else:
        print("Valid response is None, no specific information to print.")

# Example usage
api_url = 'https://apilist.tronscanapi.com/api/transfer/trc20?address=TWmZhdHVqbjKEEJVThJttZ9e2PkZFf3Jfb&trc20Id=TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t&start=0&limit=1&direction=0&reverse=true&db_version=1&start_timestamp=&end_timestamp='
expected_hash = 'TWmZhdHVqbjKEEJVThJttZ9e2PkZFf3Jfb'

# Load forbidden_from from a JSON file
forbidden_from = load_forbidden_from('forbidden_from.json')

valid_response = call_api_until_valid(api_url, expected_hash, forbidden_from)

if valid_response is not None:
    print_specific_info(valid_response)
    
