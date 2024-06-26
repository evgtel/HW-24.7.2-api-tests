import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    def __init__(self):
        self.base_url= 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email, password):
        """ GET запрос получения api_key"""
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers = headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        """ Получение списка всех питомцев, если 'filter' не задан,
        и только своих, если 'filter'='my_pets' """
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key, name, animal_type, age, pet_photo):
        """POST запрос добавления питомца с указанными именем, типом, возрастом и фото,
                возвращает статус запроса и JSON с добавленными данными питомца"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': str(age),
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()

        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """POST запрос на удаление питомца по указанному ID """

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        # except json.decoder.JSONDecodeError:
        except:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """POST запрос обновления данных питомца c указанным ID,
        возвращает статус запроса и JSON с обновлёнными данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet_simple(self, auth_key, name, animal_type, age):
        """POST запрос добавления питомца с указанными именем, типом, возрастом и без фото,
                        возвращает статус запроса и JSON с добавленными данными питомца"""
        data = {
                'name': name,
                'animal_type': animal_type,
                'age': age
            }
        headers = {'auth_key': auth_key['key']}
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()

        except:
            result = res.text
        return status, result

    def add_pet_photo(self, auth_key: json, pet_id: str, pet_photo):
        """POST запрос добавления фото питомца с указанными ID,
        возвращает статус запроса и JSON с обновлёнными данными питомца"""
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + f'/api/pets/set_photo/{pet_id}', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    # Addition methods for testing

    def get_list_of_pets_without_api_key(self, filter):
        """ Попытка получения списка питомцев без api_key """
        headers = {}
        filter = {'filter': filter}
        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet_simple_without_name(self, auth_key, animal_type, age):
        """ Попытка добавления питомца без параметра 'name' """
        data = {
                'animal_type': animal_type,
                'age': age
            }
        headers = {'auth_key': auth_key['key']}
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()

        except:
            result = res.text
        return status, result
