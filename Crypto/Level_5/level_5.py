import json
import base64
import requests
from colorama import Fore

# Global values
base_url = "http://crypto.praetorian.com/{}"
email = "almightysec@pm.me"
auth_token = None

def get_token(email):
    global auth_token
    if not auth_token:
        url = base_url.format("api-token-auth/")
        response = requests.post(url, data={"email": email})
        response.raise_for_status()
        auth_token = {"Authorization": "JWT " + response.json()['token']}
    return auth_token

def fetch_challenge(level):
    url = base_url.format(f"challenge/{level}/")
    response = requests.get(url, headers=get_token(email))
    response.raise_for_status()
    response_json = response.json()

    # Save the response to a file
    with open('server_response.json', 'w') as file:
        json.dump(response_json, file)

    return response_json

def solve_challenge(level, guess):
    url = base_url.format(f"challenge/{level}/")
    data = {"guess": guess}
    response = requests.post(url, headers=get_token(email), data=data)
    response.raise_for_status()
    return response.json()

def extract_and_save_audio(server_response_json_file):
    # Load the server response JSON from a file
    with open(server_response_json_file, 'r') as file:
        server_response_json = file.read()

    # Parse the JSON
    server_response = json.loads(server_response_json)
    
    # Extract the base64-encoded audio data from the response
    base64_audio_data = server_response['challenge'].split(",")[1]
    
    # Decode the base64 audio data to binary
    audio_data = base64.b64decode(base64_audio_data)
    
    # Define the path where the audio file will be saved
    audio_file_path = 'ctf_level_5_audio.wav'
    
    # Write the decoded audio data to a file
    with open(audio_file_path, 'wb') as audio_file:
        audio_file.write(audio_data)
    
    print(Fore.GREEN+f"Audio file saved successfully at: {audio_file_path}")

# Fetch the challenge and save the response to a file
fetch_challenge(5)

# Use the saved response file as input to the extract_and_save_audio function
server_response_json_file = 'server_response.json'
extract_and_save_audio(server_response_json_file)

def main():
    level = 5
    try:
        print(Fore.YELLOW+"Enter your guess after completing your analysis...")

        while True:  # This loop will continue asking for guesses until the correct answer is provided
            guess = input(Fore.RED+"Your guess: ")
            h = solve_challenge(level, guess)  # Attempt to solve
            if 'hash' in h:
                print(Fore.GREEN+f"Solved Level {level}! Hash: {h['hash']}")
                break  # Exit the loop if the challenge is solved
            else:
                print("Incorrect guess, please try again.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()