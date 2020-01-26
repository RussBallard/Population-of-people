import json
from random import shuffle

from psycopg2.extras import Json


class Person:
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.sex = kwargs['sex']
        self.preferences = kwargs['preferences']


class Apartment:
    def __init__(self, file='data.json'):
        with open(file, encoding='utf-8') as people_file:
            data = json.load(people_file)
            self.peoples = data['people']
            self.rooms = data['rooms']

    def populate_a_person(self, person_index, room_index):
        # Заносим в переменную все данные о людях проживающих в квартире, итерируя
        # через массив persons внутри передаваемого словаря
        every_values_in_room = [v for persons in self.rooms[room_index]['persons'] for v in persons.values()]

        if not self.rooms[room_index]['persons']:
            self.rooms[room_index]['persons'].append(self.peoples[person_index])
            return True

        elif self.peoples[person_index]['sex'] in every_values_in_room:
            if (self.peoples[person_index]['preferences'] == 'Гей' and
                    'Нетолерантный натурал' not in every_values_in_room):
                self.rooms[room_index]['persons'].append(self.peoples[person_index])
                return True

            if (self.peoples[person_index]['preferences'] == 'Лесби' and
                    'Нетолерантный натурал' not in every_values_in_room):
                self.rooms[room_index]['persons'].append(self.peoples[person_index])
                return True

            if (self.peoples[person_index]['preferences'] == 'Нетолерантный натурал' and
                    'Гей' not in every_values_in_room and
                    'Лесби' not in every_values_in_room):
                self.rooms[room_index]['persons'].append(self.peoples[person_index])
                return True

            if self.peoples[person_index]['preferences'] == 'Толерантный натурал':
                self.rooms[room_index]['persons'].append(self.peoples[person_index])
                return True

            else:
                return

        else:
            return

    def random_populate(self, cur):
        # При каждом запуске заселения необходимо перетасовать людей и комнаты рандомно
        [shuffle(var) for var in [self.peoples, self.rooms]]
        count_in_room, count_in_people = 0, 0

        while count_in_people < len(self.peoples):
            # Проверка на случай, когда будет нужно пройтись заново по свободным апартаментам
            if count_in_room == len(self.rooms):
                count_in_room = 0
                while True:
                    if self.rooms[count_in_room]['is_fullness']:
                        count_in_room += 1
                    else:
                        break

            if self.populate_a_person(count_in_people, count_in_room):
                count_in_people += 1
                if self.rooms[count_in_room]['number_of_rooms'] == len(self.rooms[count_in_room]['persons']):
                    self.rooms[count_in_room]['is_fullness'] = True
                    count_in_room += 1

            else:
                count_in_room += 1

        for room in self.rooms:
            cur.execute(
                'INSERT INTO apartment(number_of_rooms, persons, is_fullness) VALUES (%s, %s, %s);',
                (room['number_of_rooms'], Json(room['persons']), room['is_fullness']))
