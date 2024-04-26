import hlextend
import requests
import urllib.parse
from colorama import Fore, Style, init

# Initialize Colorama
init()

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
    headers = get_token(email)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    challenge_response = response.json()
    print(Fore.YELLOW + "Challenge Response:" + Fore.CYAN, challenge_response, Style.RESET_ALL)
    
    # Extracting MAC from challenge response
    try:
        mac = challenge_response['challenge'].split('"')[-2].split(':')[-1]
        if len(mac) != 40:
            raise ValueError("Extracted MAC is not of correct length.")
    except (IndexError, KeyError, ValueError) as e:
        print(Fore.RED + "Failed to extract MAC from challenge response: " + str(e) + Style.RESET_ALL)
        return None
    return mac

def solve_challenge(level, data_to_append, original_data, original_hash):
    sha = hlextend.new('sha1')  # Create a new SHA1 hash object
    
    for key_length in range(31, 33):  # Adjust range as needed
        new_data = sha.extend(data_to_append, original_data, key_length, original_hash)
        extended_hash = sha.hexdigest()
        new_data_hex = new_data.hex()  # Convert the new data to a hexadecimal string
        
        print(Fore.YELLOW + f"Key length {key_length}: {extended_hash}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"New data: {new_data_hex}" + Style.RESET_ALL)
        
        url = base_url.format(f"challenge/{level}/")
        data = {"guess": f"{new_data_hex}:{extended_hash}"}
        encoded_data = urllib.parse.urlencode(data, safe=':')
        
        headers = get_token(email)
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        
        response = requests.post(url, headers=headers, data=encoded_data)
        response.raise_for_status()
        response_data = response.json()
        
        print(Fore.MAGENTA + "Sent Data:" + Fore.LIGHTWHITE_EX, encoded_data, Style.RESET_ALL)
        print(Fore.MAGENTA + "Response Data:" + Fore.LIGHTWHITE_EX, response_data, Style.RESET_ALL)
        
        if 'hash' in response_data:
            print(Fore.GREEN + f"Solved Level {level}! Hash: {response_data['hash']}" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Incorrect guess, please try again." + Style.RESET_ALL)

def main():
    level = 8
    if not get_token(email):
        print(Fore.RED + "Exiting due to authentication failure." + Style.RESET_ALL)
        return
    
    mac = fetch_challenge(level)
    if not mac:
        print(Fore.RED + "Exiting due to failure in fetching challenge." + Style.RESET_ALL)
        return
    
    data_to_append = b'&admin=true'
    original_data = b'username=user00000'
    solve_challenge(level, data_to_append, original_data, mac)

if __name__ == "__main__":
    main()

