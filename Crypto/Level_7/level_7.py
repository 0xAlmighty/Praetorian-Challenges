import time
import random
import hmac
import hashlib
import urllib.parse
import requests
from colorama import Fore, Style

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
    print("Challenge Response:", response.json())
    server_time = response.headers['Date']
    print("Server Time:", server_time)
    return server_time

def solve_challenge(level, hmac_md5):
    url = base_url.format(f"challenge/{level}/")
    data = {"guess": f"757365726e616d653d61646d696e:{hmac_md5}"}
    encoded_data = urllib.parse.urlencode(data, safe=':')
    headers = get_token(email)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    response = requests.post(url, headers=headers, data=encoded_data)
    response.raise_for_status()
    response_data = response.json()
    print("Sent Data:", encoded_data)
    print("Response Data:", response_data)
    if 'hash' in response_data:
        print(Fore.GREEN + f"Solved Level {level}! Hash: {response_data['hash']}" + Style.RESET_ALL)
        return True
    else:
        print(Fore.RED + "Incorrect guess, please try again." + Style.RESET_ALL)
        return False

def generate_key(seed):
    random.seed(seed)
    key = random.getrandbits(256)
    print(f"Generated key for seed {seed}: {key}")
    return key

def create_hmac_md5(message, key):
    key_bytes = key.to_bytes(32, 'big')
    hmac_obj = hmac.new(key_bytes, message.encode(), hashlib.md5)
    return hmac_obj.hexdigest()

def main():
    level = 7
    if not get_token(email):
        print(Fore.RED + "Exiting due to authentication failure." + Style.RESET_ALL)
        return
    
    if not fetch_challenge(level):
        print(Fore.RED + "Exiting due to failure in fetching challenge." + Style.RESET_ALL)
        return

    message = "username=admin"

    current_time = int(time.time() * 256)
    for offset in range(-10, 10):
        seed = current_time + offset
        key = generate_key(seed)
        hmac_md5 = create_hmac_md5(message, key)
        print(f"Trying HMAC MD5 with seed {seed}: {hmac_md5}")
        if solve_challenge(level, hmac_md5):
            print(Fore.GREEN + f"Success! Seed found: {seed}" + Style.RESET_ALL)
            break
    else:
        print(Fore.RED + "Failed to find the correct seed within the given range.")

if __name__ == "__main__":
    main()