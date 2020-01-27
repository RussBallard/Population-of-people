import psycopg2
from prettytable import from_db_cursor

from apartment import Apartment, Person


def new_start():
    new_apartment = Apartment()
    cursor.execute('TRUNCATE apartment RESTART IDENTITY CASCADE;;')
    return new_apartment


with psycopg2.connect(dbname='postgres', user='admin', password='admin', host='localhost') as connection:
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS apartment(id SERIAL, number_of_rooms SMALLINT NOT NULL, persons JSON,'
            'is_fullness BOOLEAN NOT NULL);')

        # При первом запуске уже должны быть данные
        apartment = new_start().random_populate(cursor)

        while True:
            choice = input('\n1. Посмотреть список заселенных.\n'
                           '2. Заселить людей.\n'
                           '3. Заселить нового человека.\n'
                           '4. Выйти из приложения.\n'
                           'Выберите вариант действия: ')

            if choice == '1':
                db_select = {'1': 'SELECT * FROM apartment WHERE is_fullness = False;',
                             '2': 'SELECT * FROM apartment WHERE is_fullness = True;',
                             '3': 'SELECT * FROM apartment;'}

                choice = input('\n1. Показать свободные комнаты и кто там живет.\n'
                               '2. Показать занятые комнаты и кто там живет.\n'
                               '3. Показать все комнаты и кто там живет.\n'
                               'Выберите вариант действия: ')

                select = db_select.get(choice, '')
                if select:
                    cursor.execute(select)
                    print(from_db_cursor(cursor))
                else:
                    print('\nНет такого варианта.')
                    continue

            elif choice == '2':
                apartment = new_start().random_populate(cursor)

            elif choice == '3':
                # Дополнил изначальную задачу и создал возможность добавлять новых людей в апартаменты
                while True:
                    valid_preferences = ('Гей', 'Лесби', 'Нетолерантный натурал', 'Толерантный натурал')
                    valid_sex = ('Мужской', 'Женский')

                    name = input('Введите имя заселяемого: ')
                    sex = input('Введите пол заселяемого (Мужской или Женский): ').capitalize()
                    preferences = input('Введите сексуальную ориентацию заселяемого (Гей, Лесби, Нетолерантный натурал '
                                        'или Толерантный натурал): ').capitalize()

                    if preferences not in valid_preferences or sex not in valid_sex:
                        print('Заполните анкету корректно!')
                        continue

                    apartment = new_start()
                    apartment.peoples.append(vars(Person(name=name, sex=sex, preferences=preferences)))
                    apartment.random_populate(cursor)
                    break

            elif choice == '4':
                print('До свидания!')
                break

            else:
                print('\nНет такого варианта.')
