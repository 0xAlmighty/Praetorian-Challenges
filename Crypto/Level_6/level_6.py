import requests
import time
from datetime import datetime

# Global stuff
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
    print("Raw Response Object:", response)
    response.raise_for_status()
    try:
        json_response = response.json()
        print("Response JSON Content:", json_response)
    except ValueError as e:  # Handles cases where JSON decoding fails
        print("Error decoding JSON from response:", e)
        print("Response Text Content:", response.text)
    return json_response

def solve_challenge(level, guess):
    time.sleep(3) # Add simulated delay
    """Submit a guess for the challenge and measure response time with high precision using .perf_counter()"""
    url = base_url.format(f"challenge/{level}/")
    data = {"guess": guess}
    start_time = time.perf_counter()  # High-resolution start time
    print(start_time)
    response = requests.post(url, headers=get_token(email), json=data) # , proxies=proxies
    end_time = time.perf_counter()  # High-resolution end time
    print(end_time)
    response.raise_for_status()
    response_time = end_time - start_time  # Calculate duration in seconds
    print(f"Response time for guess '{guess}': {response_time:.6f} seconds")
    return response.json(), response_time

def timing_attack(level, starting_guess):
    """Refines the guess by measuring response times for different character additions,
    added options to switch between lowercase, uppercase letters, and numbers."""
    current_guess = starting_guess
    last_guess_correct = True

    def try_guesses(char_range):
        """Tries appending characters from char_range to current_guess, selects the best character based on a significance threshold."""
        nonlocal current_guess
        best_char = ''
        max_avg_time_diff = 0 # default 0
        significance_threshold = 0.05  # threshold: 10% longer than the average if using 0.1, set to 0.05, can tweak
        total_times = []
        attempts_per_char = 1

        # Collect average response times for each character
        for char in char_range:
            total_time = sum(solve_challenge(level, current_guess + char)[1] for _ in range(attempts_per_char))
            avg_time = total_time / attempts_per_char
            total_times.append((char, avg_time))

        # Calculate the overall average response time
        overall_avg_time = sum(time for _, time in total_times) / len(total_times)

        # Determine the best character based on the threshold
        for char, avg_time in total_times:
            if avg_time > overall_avg_time * (1 + significance_threshold) and avg_time > max_avg_time_diff:
                max_avg_time_diff = avg_time
                best_char = char

        return best_char

    def get_char_sequence(choice):
        """Returns the character sequence based on choice."""
        if choice == '1':
            return [chr(i) for i in range(ord('A'), ord('Z') + 1)]  # Uppercase letters
        elif choice == '2':
            return [str(i) for i in range(0, 10)]                   # Numbers
        else:
            return [chr(i) for i in range(ord('a'), ord('z') + 1)]  # Lowercase letters

    while True:
        print(f"Current best guess: {current_guess}")
        if not last_guess_correct:
            retry_choice = input("Retry last position? (y/n): ")
            if retry_choice.lower() == 'y':
                current_guess = current_guess[:-1]  # Remove the last character to retry
            last_guess_correct = True  # Reset flag

        choice = input("Continue with (0) lowercase, (1) uppercase letters, (2) numbers, or any other key to finish: ")
        if choice not in ['0', '1', '2']:
            print("Final guess:", current_guess)
            break

        char_sequence = get_char_sequence(choice)
        best_char = try_guesses(char_sequence)
        if best_char:
            current_guess += best_char
            print(f"Best guess so far: {current_guess}")
        else:
            print("No improvement found, try a different set or finish.")
            last_guess_correct = False  # Set flag indicating the last guess may not be correct
            continue  

# Authenticate first
get_token(email)

# Start
initChall = input("Do you want to reset the challenge?Enter 'y' for yes and 'n' for no: ")
if initChall == 'y':
    fetch_challenge(6)
level = 6
initChar = input("Enter the starting letter according to the response: ")
timing_attack(level, initChar)
