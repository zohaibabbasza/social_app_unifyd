from django.core.mail import send_mail
from django.conf import settings
from django.core.files import File
import math, random,uuid
from pyfcm import FCMNotification
from PIL import Image
from io import BytesIO

def send_custom_email(subject,message,recipient):
    subject = subject
    message = message
    send_mail(subject, message,
                settings.DEFAULT_FROM_EMAIL, [recipient])

def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'media/' + filename

def send_push_notification(ids,message_title,message_body):
    push_service = FCMNotification(api_key=settings.FCM_API_KEY)
    result = push_service.notify_multiple_devices(registration_ids=ids, message_title=message_title, message_body=message_body)
    print(result)


def compress_image(image):
        im = Image.open(image)
        im_io = BytesIO() 
        im = im.resize([800,800])
        im = im.convert("RGB")
        im = im.save(im_io,'JPEG', quality=70) 
        new_image = File(im_io, name=image.name)
        return new_image