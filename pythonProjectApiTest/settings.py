import os
from dotenv import load_dotenv

my_pet_name = 'Doggy'
my_pet_type = '3D'
my_pet_age = 2
my_pet_photo = 'images\\dog.jpg'

new_name = 'Dog'
new_type = '4K'
new_age = 3

negative_age = -10

invalid_email = 'ya1@'
invalid_password = 'ya2'
invalid_auth_key = '00000148a1f19838e1c5d1413877f3691a3731380e733e1111111111'
invalid_pet_photo = 'images\\photo.txt'
load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')



