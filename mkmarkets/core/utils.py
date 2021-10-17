from random import choice
from string import ascii_letters, punctuation



def get_random_string(length):
    raw_string = ascii_letters + punctuation
    return ''.join(choice(raw_string) for count in range(length))
