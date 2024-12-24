import string 
import random 



def code2fa():
    seed = 6#link randomizer #yoink not anymore more like a token generator LOL :D
    rz = '' 
    for i in range(seed):
        rz = rz + random.choice(string.ascii_letters)
    return rz
