from operator import mul, xor
from functools import reduce
from struct import unpack
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time

def hash(d):
    j = unpack
    y = bytes
    e = mul
    w = bytearray
    n = xor
    i = reduce
    f = map
    l = b'\x3e\x68\x68\x69'
    q = w(b'\x0a'*4)
    r = len
    d = w(d)
    h = b'\x00\x0b\x01\x01\x00\x14\x2a\x2d'
    h = i(e, j(l, h))
    l = b'\x3e\x49'
    k = w(b'\xc0\xf4\xb0\xb4')
    c = h ^ (h & 0x0)
    q = i(e, j(l, y(w(f(n, k, q)))))
    k = r(d)
    y, j = h ^ c, h
    while (y >> (c ^ 3735928571)) < k:
        j = (j ^ (((2**(4*1<<2)-1) * (y % (c ^ 3736977135) > 0)) & ((d[y >> (c ^ 3735928571)] * q) ^ (0xface * (y >> (c ^ 3735928571))))) & (2**(4*1<<2)-1))
        y += (h ^ (h - 0xf + 0x2 * 7))
    return format(j, 'x')

def hash_word(word):
    return word, hash(word.encode())

def main(file_path, output_file, workers=10):
    start_time = time.time()
    try:
        with open(file_path, 'r') as file:
            words = [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Failed to read file: {e}")
        return

    try:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(hash_word, word): word for word in words}
            with open(output_file, 'w') as outfile:
                for future in as_completed(futures):
                    word = futures[future]
                    try:
                        word, hashed_word = future.result()
                        last_four = hashed_word[-4:]  # Extract the last four characters
                        outfile.write(f"{word}: {last_four}\n")  # Write both the word and the last four characters to the file
                        print(f"Word: {word}, Hash: {hashed_word}")
                    except Exception as e:
                        print(f"Error processing {word}: {e}")
    except Exception as e:
        print(f"Error setting up ThreadPoolExecutor: {e}")

    elapsed_time = time.time() - start_time
    print(f"Processing completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    words_file_path = 'wordlist.txt' # File containing words to hash
    output_file_path = 'final_hash_output.txt' # Output file to store the hashes
    main(words_file_path, output_file_path)