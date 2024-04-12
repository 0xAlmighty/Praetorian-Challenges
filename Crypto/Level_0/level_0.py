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
    return response.json()

def solve_challenge(level, guess):
    url = base_url.format(f"challenge/{level}/")
    data = {"guess": guess}
    response = requests.post(url, headers=get_token(email), data=data)
    response.raise_for_status()
    return response.json()

def caesar_cipher(text, shift):
    """Decode a Caesar cipher with the given shift."""
    decoded = ''
    for char in text:
        if char.isalpha():  # Check if the character is an alphabet
            shifted = ord(char) - shift  # Shift the character backwards
            if char.islower():
                if shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted < ord('A'):
                    shifted += 26
            decoded += chr(shifted)
        else:
            decoded += char
    return decoded

def find_correct_shift(challenge):
    for shift in range(26):
        decoded_message = caesar_cipher(challenge, shift)
        print(f"Shift {shift}: {decoded_message}")

challenge_text = "AfpzilprobPvpqbjZlkcifzq"
hint = "Praetorian... that sounds Roman..."

# Find the correct shift
find_correct_shift(challenge_text)

def main():
    level = 0
    hashes = {}
    try:
        data = fetch_challenge(level)
        guess = data['challenge']
        h = solve_challenge(level, guess)
        if 'hash' in h:
            hashes[level] = h['hash']
            print(Fore.GREEN + f"Solved Level {level}!: {h['hash']}")
        else:
            print("Failed to solve level {}.".format(level))
    except Exception as e:
        print("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()