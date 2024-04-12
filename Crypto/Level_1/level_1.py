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
    """Decode Caesar cipher with the given shift."""
    decoded = ''
    for char in text:
        if char.isalpha():
            shifted = ord(char) - shift
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

def auto_solve_caesar(challenge_text):
    """Automatically find and return the correct Caesar cipher by trying all shifts."""
    for shift in range(26):
        decoded_message = caesar_cipher(challenge_text, shift)
        print(f"Shift {shift}: {decoded_message}")
    correct_shift = int(input(Fore.CYAN+"Enter the correct shift based on output: "))
    return caesar_cipher(challenge_text, correct_shift)

def main():
    level = 1
    try:
        data = fetch_challenge(level)
        challenge_text = data['challenge']
        print(f"Challenge Text: {challenge_text}")
        decoded_message = auto_solve_caesar(challenge_text)
        if decoded_message:
            print(Fore.YELLOW + f"Decoded Message: {decoded_message}")
            h = solve_challenge(level, decoded_message)
            if 'hash' in h:
                print(Fore.GREEN + f"Solved Level {level}!: {h['hash']}")
            else:
                print("Failed to solve level.")
        else:
            print("Failed to decode message. No valid English text found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()