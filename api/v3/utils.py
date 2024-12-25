import random
from django.core.cache import cache

def code2fa():
    seed = 6
    otp = ''
    
    # Debugging: Print the OTP while generating
    print("Generating OTP...")
    
    for i in range(seed):
        otp += str(random.randint(0, 9))
    
    # Debugging: Print the OTP after it has been generated
    print(f"Generated OTP: {otp}")
    
    # Store OTP in cache with a 5-minute timeout
    cache.set('otp', otp, timeout=300)
    
    # Debugging: Verify OTP is stored in cache
    cached_otp = cache.get('otp')
    print(f"OTP stored in cache: {cached_otp}")
    
    return otp


