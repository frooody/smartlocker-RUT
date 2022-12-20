from create import bot, dp
import aiogram
import face_recognition 
import PIL
import os
import time

FACES_DIR = 'database'
chat_ids = []

@dp.message_handler()
async def echo(message: aiogram.types.Message):
    global chat_ids
    chat_ids.append(message.from_user.id)

@dp.message_handler(content_types=['photo'])
async def add_member_to_list_of_access(message: aiogram.types.Message):
    await message.photo[-1].download(message.caption + '.jpg')
    load = face_recognition.load_image_file(message.caption + '.jpg')
    # detect the faces from the images  
    locations = face_recognition.face_locations(load)
    load_encodings = face_recognition.face_encodings(load)[0]
    members = []
    # encode the 128-dimension face encoding for each face in the image 
    for filename in os.listdir(FACES_DIR):
        f = os.path.join(FACES_DIR, filename)
        if os.path.isfile(f):
            image2 = face_recognition.load_image_file(f)
            image2_encodings = face_recognition.face_encodings(image2)[0]
            result = face_recognition.compare_faces([load_encodings], image2_encodings)
            if result[0]:
                members.append(1)
    if 1 in members:    
        await message.reply('Пользователь уже занесен в базу данных')
    else:
        i = 0
        for location in locations:
            top, right, bottom, left = location
            face_img = load[top:bottom, left:right]
            pil_img = PIL.Image.fromarray(face_img)
            pil_img.save(f"database/{message.caption}.jpg")
            i += 1
        await message.reply(message.caption + ' успешно занесен(а) в базу данных!')
        print(chat_ids)
    os.remove(message.caption + '.jpg')

if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True)