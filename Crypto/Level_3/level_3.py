import requests
import base64
from PIL import Image
from colorama import Fore

# Global values
base_url = "http://crypto.praetorian.com/{}"
email = "almightysec@pm.me"
auth_token = None

# Proxy
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

def get_token(email):
    global auth_token
    if not auth_token:
        url = base_url.format("api-token-auth/")
        response = requests.post(url, data={"email": email}, proxies=proxies)
        response.raise_for_status()
        auth_token = {"Authorization": "JWT " + response.json()['token']}
    return auth_token

def fetch_challenge(level):
    url = base_url.format(f"challenge/{level}/")
    response = requests.get(url, headers=get_token(email), proxies=proxies)
    response.raise_for_status()
    return response.json()

def solve_challenge(level, guess):
    url = base_url.format(f"challenge/{level}/")
    data = {"guess": guess}
    response = requests.post(url, headers=get_token(email), data=data, proxies=proxies)
    response.raise_for_status()
    return response.json()

def decode_base64_image(base64_data):
    """Decode base64 image data and save as a PNG file."""
    image_data = base64_data.split(",")[1]
    with open("challenge_image.png", "wb") as image_file:
        image_file.write(base64.b64decode(image_data))
    print(Fore.YELLOW+"Image decoded and saved as 'challenge_image.png'.")

def convert_to_ppm(image_path):
    # Load the image
    png_image = Image.open(image_path)
    
    png_image.save('output_image.ppm')

def read_ppm_file_including_text(file_path):
    """
    Reads and prints the content of a PPM file in binary mode,
    including binary data and any human-readable text.

    Args:
    - file_path: The path to the .ppm file.

    This function handle P6 format .ppm files
    but will attempt to decode and print human-readable ASCII text
    found in the file.
    """
    try:
        with open(file_path, 'rb') as file:
            content = file.read()

            try:
                # Attempt to decode the entire content as ASCII
                print(content.decode('ascii'))
            except UnicodeDecodeError:
                # If decoding fails, print the binary data as is,
                # then attempt to find and print the ASCII text at the end
                print(Fore.YELLOW+"Binary image data (not displayed)")
                # Find the last newline, which might precede human-readable text
                last_newline = content.rfind(b'\n')
                if last_newline != -1 and last_newline < len(content) - 1:
                    # Attempt to decode and print any text after the last newline
                    text_end = content[last_newline + 1:].decode('ascii', errors='ignore')
                    print(Fore.YELLOW+"Detected ASCII text at the end of the file:")
                    print(Fore.CYAN+text_end)

    except FileNotFoundError:
        print(f"No file found at {file_path}. Please check the path and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    level = 3
    try:
        challenge_data = fetch_challenge(level)
        challenge_text = challenge_data['challenge']
        decode_base64_image(challenge_text)
        print(Fore.YELLOW+"Inspecting 'challenge_image.png' for hidden data or clues...")
        convert_to_ppm('challenge_image.png')
        read_ppm_file_including_text('output_image.ppm')
        print("Enter your guess after completing your analysis:")

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