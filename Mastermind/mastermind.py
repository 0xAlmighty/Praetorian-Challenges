import requests
from itertools import permutations
from typing import Tuple, Generator
from colorama import Fore, Style
#import traceback

base_url = "https://mastermind.praetorian.com/{}"
email = "almightysec@pm.com"
auth_token = None

def get_token(email):
    global auth_token
    if not auth_token:
        url = base_url.format("api-auth-token/")
        response = requests.post(url, json={"email": email})
        response.raise_for_status()  
        auth_token = {"Auth-Token": response.json()['Auth-Token']}
        print(Fore.YELLOW + "Auth token received: " + str(auth_token) + Style.RESET_ALL)
    return auth_token

def fetch_challenge(level):
    url = base_url.format(f"level/{level}/")
    response = requests.get(url, headers=get_token(email))
    response.raise_for_status() 
    return response.json()

def solve_challenge(level, guess):
    url = base_url.format(f"level/{level}/")
    data = {"guess": guess}
    response = requests.post(url, headers=get_token(email), json=data)
    response.raise_for_status()
    return response.json()

def reset_challenge():
    url = base_url.format("reset/")
    response = requests.post(url, headers=get_token(email))
    response.raise_for_status()
    return response.json()

Guess = Tuple[int, ...]
Score = Tuple[int, int]

def generate_guesses(gladiators: int, weapons: int) -> Generator[Guess, None, None]:
    return permutations(range(weapons), gladiators)

def calculate_score(guess: Guess, code: Guess) -> Score:
    w = b = 0
    for i, n in enumerate(guess):
        if n in code:
            w += 1
        if n == code[i]:
            b += 1
    return w, b

def remove_unwanted(guesses: Generator[Guess, None, None], guess: Guess, score: Score) -> Generator[Guess, None, None]:
    return (s for s in guesses if calculate_score(s, guess) == score)

def next_guess(guesses: Generator[Guess, None, None]) -> Guess:
    return next(guesses)

def main():
    level = 1
    while True:
        print(Fore.CYAN + "Mastermind initialized. The game is now reset and ready to play." + Style.RESET_ALL)
        if level == 1:
            reset_challenge()
        for level in range(level, 7):
            print(Fore.MAGENTA + f"Starting level {level}" + Style.RESET_ALL)
            try:
                data = fetch_challenge(level)
                gladiators = data['numGladiators']
                weapons = data['numWeapons']
                guesses = generate_guesses(gladiators, weapons)

                while True:
                    if not guesses:
                        print(Fore.RED + "No more guesses left. Something went wrong." + Style.RESET_ALL)
                        break
                    guess = next_guess(guesses)
                    print(Fore.YELLOW + f"Guess: {guess}" + Style.RESET_ALL)
                    response = solve_challenge(level, list(guess))
                    score_value = tuple(response.get('response', []))
                    print(Fore.BLUE + f"Score for guess {guess}: {score_value}" + "\n" + Style.RESET_ALL)
                    if level == 6 and 'hash' in response:
                        print(Fore.GREEN + f"Hash for level 6: {response['hash']}" + Style.RESET_ALL)
                        return
                    elif 'message' in response:
                        print(Fore.GREEN + response['message'] + " Good job!\n" + Style.RESET_ALL)
                        break
                    guesses = remove_unwanted(guesses, guess, score_value)
            except Exception as e:
                print(Fore.RED + f"An error occurred at level {level}: {e}\n" + Style.RESET_ALL)
                #traceback.print_exc()
                break
        else:
            break

if __name__ == "__main__":
    main()