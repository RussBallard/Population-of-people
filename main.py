import os

from data_work import Apartment, json_file, work_with_db

apartment = Apartment()
# По условию задачи, при первом запуске программы,
# люди уже должны быть заселенны случайно
apartment.random_populate()
work_with_db(json_data=json_file())

while True:
    choice = input('\n1. Посмотреть список заселенных.\n'
                   '2. Заселить людей.\n'
                   '3. Выйти из приложения.\n'
                   'Выберите вариант действия: ')

    if choice == '1':
        choice = input('\n1. Показать свободные комнаты и кто там живет.\n'
                       '2. Показать занятые комнаты и кто там живет.\n'
                       '3. Показать все комнаты и кто там живет.\n'
                       'Выберите вариант действия: ')
        if choice == '1':
            select = '''SELECT rooms.id, room_name, number_of_free_places, 
                        is_the_room_full, name, sex, preferences 
                        FROM people FULL JOIN rooms ON rooms.id = people.room_id
                        WHERE is_the_room_full = False;'''
            print(work_with_db(select))

        elif choice == '2':
            select = '''SELECT rooms.id, room_name, number_of_free_places, 
                        is_the_room_full, name, sex, preferences 
                        FROM people FULL JOIN rooms ON rooms.id = people.room_id
                        WHERE is_the_room_full = True;'''
            print(work_with_db(select))

        elif choice == '3':
            select = '''SELECT rooms.id, room_name, number_of_free_places, 
                        is_the_room_full, name, sex, preferences 
                        FROM people FULL JOIN rooms ON rooms.id = people.room_id;'''
            print(work_with_db(select))

    elif choice == '2':
        os.remove('result.json')
        apartment.random_populate()

    elif choice == '3':
        print('До свидания!')
        break

    else:
        print('\nНет такого варианта.')
