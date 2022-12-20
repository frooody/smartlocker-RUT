import face_recognition
import os
from notifiers import get_notifier
import time
from create import TOKEN
from main import chat_ids

FACES_DIR = 'database'


def compare(path):
    global name
    try:
        image1 = face_recognition.load_image_file(path)
        image1_encodings = face_recognition.face_encodings(image1)[0]
        members = []
        for filename in os.listdir(FACES_DIR):
            f = os.path.join(FACES_DIR, filename)
            if os.path.isfile(f):
                image2 = face_recognition.load_image_file(f)
                image2_encodings = face_recognition.face_encodings(image2)[0]
                result = face_recognition.compare_faces([image1_encodings], image2_encodings)
                if result[0]:
                    members.append(1)
                    name = str(filename)
            if 1 in  members:
                return 1
    except IndexError:
        print("Face not found")
        return -1
    
tg = get_notifier('telegram')
while True:
    if compare('camera/photo.jpg') == 1:
        tg.notify(token=TOKEN, chat_id=1133563229, message=name[:-4]+' вошёл в лабораторию.')
    elif compare('camera/photo.jpg') == -1:
        pass
    else:
        tg.notify(token=TOKEN, chat_id=1133563229, message='Посторонний пытается проникнуть в лабораторию!')
    time.sleep(5)
