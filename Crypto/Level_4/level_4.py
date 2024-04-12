import requests
import base64
from PIL import Image
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
    data = response.json()
    return data['challenge'].split(' = ')[1]  # Return the hash

def solve_challenge(level, guess):
    url = base_url.format(f"challenge/{level}/")
    data = {"guess": guess}
    response = requests.post(url, headers=get_token(email), data=data)
    response.raise_for_status()
    return response.json()

def searching_for_hash(hash_input):
    try:
        with open("final_hash_output.txt", "r") as f:
            for line in f:
                word, hash_value = line.strip().split(": ")
                if hash_input == hash_value:
                    return line
    except IOError:
        print("Error opening file")
    return None

def main():
    level = 4
    while True:
        try:
            hash_input = fetch_challenge(level)  # Get the hash from the server response
            print(Fore.YELLOW+"Searching for the matching: "+hash_input+" from the final_hash_output.txt file...")
            matching_line = searching_for_hash(hash_input)
            if matching_line:
                print(Fore.GREEN + "Match found: " + matching_line)
                break  # Exit the loop if a match is found
            else:
                print(Fore.RED + "No match found. Fetching the challenge again...")
        except Exception as e:
            print(Fore.RED + "An error occurred: " + str(e))

    while True:
        try:
            guess = input(Fore.CYAN+"Your guess: ")
            h = solve_challenge(level, guess)
            if 'hash' in h:
                print(Fore.GREEN+f"Solved Level {level}! Hash: {h['hash']}")
                break 
            else:
                print("Incorrect guess, please try again.")
        except Exception as e:
            print(Fore.RED + "An error occurred: " + str(e))

if __name__ == "__main__":
    main()