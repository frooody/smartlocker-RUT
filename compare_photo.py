import face_recognition 
import PIL
import os
from create import bot
import numpy as np
import time
from main import chat_ids

FACES_DIR = 'database'
CAMERA_DIR = 'camera'

def compare(path):
    try:
        image1 = face_recognition.load_image_file(path)
        image1_encodings = face_recognition.face_encodings(image1)[0]
    except IndexError:
        print("Face not found")
        exit()
    members = []
    for filename in os.listdir(FACES_DIR):
        f = os.path.join(FACES_DIR, filename)
        if os.path.isfile(f):
            image2 = face_recognition.load_image_file(f)
            image2_encodings = face_recognition.face_encodings(image2)[0]
            result = face_recognition.compare_faces([image1_encodings], image2_encodings)
            if result[0]:
                members.append(1)
    if not 1 in  members: 
        return 1
while True:
    for chat_id in chat_ids:
        compare('camera/photo.jpg', chat_id)
    time.sleep(4)
bot.send_message(chat_id=chat_id, text='dsa')
    
