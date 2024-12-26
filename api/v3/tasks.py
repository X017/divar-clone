
from __future__ import absolute_import , unicode_literals
from celery import shared_task
import requests



@shared_task()
def start_otp(note,receiver_number):
    final = "DRF Activation CODE: " + note
    url = f"http://sms.segalnet.net/send_via_get/send_sms.php?note={final}&username=bonit_ad&password=&receiver_number={receiver_number}&sender_number=9890008750"
    requests.get(url)
    
    return note
    
