import requests
import base64
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
    print("Image decoded and saved as 'challenge_image.png'.")

def examine_png_chunks(png_file_path):
    """Examine and print the type and size of each chunk in a PNG file."""
    # PNG file signature (magic number) to verify it's a PNG file
    png_signature = b'\x89PNG\r\n\x1a\n'
    
    with open(png_file_path, 'rb') as file:
        signature = file.read(8)
        if signature != png_signature:
            print(f"{png_file_path} is not a valid PNG file.")
            return
        
        print(f"Examining PNG chunks in {png_file_path}:")
        while True:
            # Each chunk has a length (4 bytes), type (4 bytes), data (variable length), and CRC (4 bytes)
            chunk_length_data = file.read(4)
            if len(chunk_length_data) == 0:  # End of file
                break
            
            # The length of the data portion of the chunk
            chunk_length = int.from_bytes(chunk_length_data, byteorder='big')
            
            # The type of the chunk (e.g., IHDR, IDAT, IEND)
            chunk_type = file.read(4).decode('ascii')
            
            # Skipping the data and CRC parts of the chunk
            file.seek(chunk_length + 4, 1)
            
            print(f"Chunk Type: {chunk_type}, Chunk Length: {chunk_length}")
        
        print("Finished examining PNG chunks.")

def extract_hckr_data(png_file_path):
    with open(png_file_path, 'rb') as file:
        # Skip the PNG signature
        file.read(8)
        
        while True:
            chunk_length_data = file.read(4)
            if len(chunk_length_data) == 0:
                break  # End of file
            
            chunk_length = int.from_bytes(chunk_length_data, byteorder='big')
            chunk_type = file.read(4).decode('ascii')
            
            if chunk_type == 'HCKR':
                print("Found HCKR chunk, extracting data...")
                hckr_data = file.read(chunk_length)
                print(Fore.YELLOW + f"HCKR Data:", hckr_data)

                file.seek(4, 1)
            else:
                # Skip this chunk's data and CRC
                file.seek(chunk_length + 4, 1)

def main():
    level = 2
    try:
        challenge_data = fetch_challenge(level)
        challenge_text = challenge_data['challenge']
        decode_base64_image(challenge_text)
        print("Please inspect 'challenge_image.png' for hidden data or clues.")
        png_file_path = "challenge_image.png"
        examine_png_chunks(png_file_path)
        extract_hckr_data("challenge_image.png")
        print(Fore.CYAN + "Enter your guess after completing your analysis...")
        guess = input(Fore.RED+"Your guess: ")
        
        # Attempt to solve the challenge with the guess
        h = solve_challenge(level, guess)
        if 'hash' in h:
            print(Fore.GREEN+f"Solved Level {level}! Hash: {h['hash']}")
        else:
            print("Failed to solve level.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
