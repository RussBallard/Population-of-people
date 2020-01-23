import json
from random import shuffle

import psycopg2
from prettytable import from_db_cursor


# Чтобы не было повторений, была создана функция, которая
# выполняет все требуемые виды работ с 'result.json'
# Функция без аргумента возвращает данные с файла
def json_file(save_data=None):
    if save_data is not None:
        with open('result.json', encoding='utf-8', mode='w') as save:
            json.dump(save_data, save, indent=4, ensure_ascii=False)
            return
    with open('result.json', encoding='utf-8') as people_file:
        data = json.load(people_file)
        return data


def random_everything_in_file():
    with open('data.json', encoding='utf-8') as people_file:
        data = json.load(people_file)
        for key, value in data.items():
            shuffle(value)

    # Мной было решено не трогать оригинальный файл с данными, и
    # вносить все измнения во второй. Он и будет импортирован в БД.
    json_file(data)


def work_with_db(select=None, json_data=None):
    with psycopg2.connect(dbname="postgres", user="postgres", password="1040602010a", host="127.0.0.1",
                          port="5432") as connection:
        with connection.cursor() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS rooms
                              (id SERIAL,
                              room_name TEXT NOT NULL,
                              number_of_free_places INT NOT NULL,
                              is_the_room_full BOOLEAN NOT NULL);''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS people
                              (id SERIAL PRIMARY KEY,
                              room_id INT NOT NULL, 
                              name TEXT NOT NULL UNIQUE,
                              sex TEXT NOT NULL,
                              preferences TEXT NOT NULL,
                              FOREIGN KEY (room_id) REFERENCES rooms (id) ON DELETE CASCADE);''')
            # cursor.execute('''TRUNCATE people, rooms''')
            if json_data is not None:
                for num, room in enumerate(json_data['rooms'], start=1):
                    is_the_room_full = False
                    if len(room) > next(iter(room.values())):
                        is_the_room_full = True
                    cursor.execute(
                        "INSERT INTO rooms(room_name, number_of_free_places, is_the_room_full) VALUES (%s, %s, %s)",
                        (next(iter(room)), next(iter(room.values())), is_the_room_full))
                    for k, v in room.items():
                        if k.startswith('person'):
                            cursor.execute(
                                "INSERT INTO people(room_id, name, sex, preferences) VALUES (%s, %s, %s, %s)",
                                (num, v['name'], v['sex'], v['preferences']))
                return

            cursor.execute(select)
            x = from_db_cursor(cursor)
            x.sortby = 'id'
            return x


class Person:
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.sex = kwargs['sex']
        self.preferences = kwargs['preferences']


class Apartment:
    def populate_a_person(self, person, room):
        # Ложим все данные людей, находящиеся в комнате, в переменную
        temporary_variable = {k: v for k, v in room.items() if k.startswith('person')}
        every_values_in_room = []
        for k, v in temporary_variable.items():
            for k1, v1 in v.items():
                every_values_in_room.append(v1)

        if len(room) == 1:
            room['person ' + str(len(room))] = person
            return True

        # Если в комнате кто-то есть, то идет проверка на пол,
        # а потом на предпочтения
        elif person['sex'] in every_values_in_room:
            if (person['preferences'] == 'Гей' and
                    'Нетолерантный натурал' not in every_values_in_room):
                room['person ' + str(len(room))] = person
                return True

            if (person['preferences'] == 'Лесби' and
                    'Нетолерантный натурал' not in every_values_in_room):
                room['person ' + str(len(room))] = person
                return True

            if (person['preferences'] == 'Нетолерантный натурал' and
                    'Гей' not in every_values_in_room and
                    'Лесби' not in every_values_in_room):
                room['person ' + str(len(room))] = person
                return True

            if person['preferences'] == 'Толерантный натурал':
                room['person ' + str(len(room))] = person
                return True

            else:
                return

        else:
            return

    def room_fullness_check(self, room_needs_to_check):
        # Первый ключ словаря с названием комнаты
        # имеет значение количества комнат
        if len(room_needs_to_check) > next(iter(room_needs_to_check.values())):
            return True

    def random_populate(self):
        random_everything_in_file()
        data = json_file()
        count_in_room, count_in_people = 0, 0
        while count_in_people < len(data['people']):
            # Людей больше чем комнат, и этот блок кода обнуляет комнаты
            # до первой свободной
            if count_in_room == len(data['rooms']):
                count_in_room = 0
                while True:
                    if len(data['rooms'][count_in_room]) > next(iter(data['rooms'][count_in_room].values())):
                        count_in_room += 1

                    else:
                        break
            # Смена комнаты происходит в случае ее заполнения
            # или невозможности заполнения
            if self.populate_a_person(data['people'][count_in_people], data['rooms'][count_in_room]):
                count_in_people += 1
                if self.room_fullness_check(data['rooms'][count_in_room]):
                    count_in_room += 1

            else:
                count_in_room += 1

        json_file(data)
