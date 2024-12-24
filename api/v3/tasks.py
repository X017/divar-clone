
from __future__ import absolute_import , unicode_literals
from celery import shared_task
from .utils import code2fa


@shared_task()
def start_otp(note):
    note = code2fa()
    return note
    
