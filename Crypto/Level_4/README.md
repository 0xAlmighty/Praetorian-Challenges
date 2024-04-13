# Crypto Challenge Level 4 :closed_lock_with_key:

This level focuses on hash generation and comparison, utilizing a customized approach to tackle the challenge effectively.

## Challenge Description :scroll:

For Level 4, I adapted a tailored wordlist from `lang-english.txt` provided by SecLists. The process involved capitalizing the first letter of each word and filtering out any words shorter than three characters and anything useless like words with `'`. The new list was also built from answers gained in Level 1 using a simple fetch_challenge script and saving the output in a new list.

## Script Overview :computer:

The core of this solution is the `generate_hashes.py` script. Here's what it does:

- **Wordlist Preparation**: Starts by reading the modified wordlist, which is structured for optimal hashing.
- **Hash Generation**: Utilizes `hint4.py`—a script returned by the server—to generate hashes for each word in our wordlist.
- **Output Saving**: All generated hashes are saved to `final_hash_output.txt`.

Upon running the `level_4.py` script, it performs the following:

- **Hash Querying**: Queries the hash associated with the challenge.
- **Comparison and Identification**: Compares this hash against those in `final_hash_output.txt`.
- **Result Display**: If a matching hash is found, the corresponding word is displayed on screen. This is the solution to enter on the challenge portal to proceed.
