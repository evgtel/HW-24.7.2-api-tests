import os.path
from api import PetFriends
from settings import *  # or valid_email, valid_password
# from settings import my_pet_name
pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Получение api_key для зарегистрированного пользователя"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Получение списка всех питомцев"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_success_add_new_pet_with_photo(name= my_pet_name, animal_type= my_pet_type,
                                     age= my_pet_age, pet_photo= my_pet_photo):
    """ Добавление питомца с фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_success_delete_my_pet():
    """ Удаление питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0: # если нет своих питомцев, то для проверки удаления создаем питомца
        pet_photo = os.path.join(os.path.dirname(__file__), my_pet_photo)
        pf.add_new_pet(auth_key, my_pet_name, my_pet_type, my_pet_age, pet_photo)

        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_success_add_new_pet_simple(name= my_pet_name, animal_type= my_pet_type, age= my_pet_age):
    """ Добавление питомца без фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_success_update_my_pet(name= new_name, animal_type= new_type, age= new_age):
    """Проверка возможности обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Нет моих питомцев")



def test_success_add_pet_photo(pet_photo = my_pet_photo):
    """ Добавление фото питомцу"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Формируем список питомцев без фото
    pets_id_no_photo = []
    for pet in my_pets['pets']:
        if not pet['pet_photo']:
            pets_id_no_photo.append(pet['id'])

    # Если список не пустой, добавляем фото первому питомцу
    if len(pets_id_no_photo) > 0:
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        status, result = pf.add_pet_photo(auth_key, pets_id_no_photo[0], pet_photo)
        assert status == 200
        assert result['pet_photo'] != ""

    else:
        raise Exception("Нет питомцев без фото")

# 10 tests

def test_1_unsuccess_get_api_key_for_invalid_email(email= invalid_email, password=valid_password):
    """ Невозможно получить api_key указав неправильный логин и правильный пароль"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_2_unsuccess_get_api_key_for_invalid_password(email= valid_email, password=invalid_password):
    """ Невозможно получить api_key указав правильный логин и неправильный пароль"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_3_unsuccess_get_api_key_for_no_login_no_password(email= "", password= ""):
    """ Невозможно получить api_key не указав логин и пароль"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_4_unsuccess_get_all_pets_with_invalid_key(filter=''):
    """ Невозможно запросить информацию используя невалидный api_key"""
    auth_key= {}
    auth_key['key'] = invalid_auth_key
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

def test_5_unsuccess_get_all_pets_without_key(filter=''):
    """ Невозможно запросить информацию без api_key"""
    auth_key= {}
    auth_key['key'] = ""
    status, result = pf.get_list_of_pets_without_api_key(filter)
    assert status == 403

def test_6_unsuccess_get_all_pets_with_invalid_filter(filter='all_pets'):
    """ Невозможно запросить информацию о питомцах с некорректным параметром 'filter' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status != 200
    assert 'Filter value is incorrect' in result

def test_7_unsuccess_add_new_pet_simple_without_name(animal_type= my_pet_type, age= my_pet_age):
    """ Невозможно добавить питомца не передав параметр 'name' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple_without_name(auth_key, animal_type, age)
    assert status == 400

def test_8_unsuccess_add_new_pet_simple_with_invalid_age(name= my_pet_name, animal_type= my_pet_type, age= 'bad'):
    """ Невозможно добавить питомца передав символы в параметре 'age' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 400

def test_9_unsuccess_add_new_pet_simple_with_negative_age(name= my_pet_name, animal_type= my_pet_type, age= negative_age):
    """ Невозможно добавить питомца передав отрицательное число в параметре 'age' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 400

def test_10_unsuccess_add_invalid_pet_photo_mime(pet_photo = invalid_pet_photo):
    """ Невозможно добавить фото питомца некорректного типа """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pets_id_no_photo = []
    for pet in my_pets['pets']:
        if not pet['pet_photo']:
            pets_id_no_photo.append(pet['id'])

    if len(pets_id_no_photo) > 0:
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        status, result = pf.add_pet_photo(auth_key, pets_id_no_photo[0], pet_photo)
        assert status != 200

    else:
        raise Exception("Нет питомцев без фото")