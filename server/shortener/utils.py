import string
import random

def generateURL(length=6):
    characters = string.ascii_letters + string.digits

    return ''.join(random.choice(characters) for _ in range(length))

