import random
from django.core.cache import cache

def code2fa():
    seed = 6
    otp = ''
    
    # Debugging: Print the OTP while generating
    for i in range(seed):
        otp += str(random.randint(0, 9))
    
    return otp


