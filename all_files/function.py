import psycopg2
from config import HOST, PORT, USER,PASSWORD, DATABASENAME

# Функция, создающая структуру БД (таблицы).
def create_tables(conn):

    with conn.cursor() as cursor:
        # Попытка выполнение транзации

        cursor.execute('create table username(id bigint generated always as identity primary key,'
                       'name VARCHAR(50), surname varchar(50), email varchar(100))')
        cursor.execute('create table phone(id bigint generated always as identity primary key,'
                       'phone VARCHAR(20))')
        cursor.execute('create table username_phone(user_id bigint references username(id),'
                       'phone_id bigint references phone(id))')

# Функция, позволяющая добавить нового клиента.
def create_user(user_data: list, conn):
    with conn.cursor() as cursor:
        # Попытка выполнение транзации

        cursor.execute( 'INSERT INTO username( name, surname, email) VALUES (%s,%s,%s)',(user_data[0],user_data[1],user_data[2]))

        # cursor.execute(f"INSERT INTO phone(phone) VALUES ('{user_data[3]}')")

        conn.commit()
        print("Данные добавлены")

create_user(['Варений','Mеладзе','@','123321'],conn)


# функция, позволяющая добавить телефон для существующего клиента
def insert_phone(conn,phone,user_id):
    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO phone(phone) VALUES ('{phone}')")
        '''вставляем телефон'''
        cursor.execute(f"select id from phone where phone = '{phone}'")
        cursor.execute('INSERT INTO username_phone(user_id,phone_id) values (%s,%s)',(user_id, cursor.fetchall()[0][0]))
        '''нашли id телефона из phone'''
        conn.commit()
        print("Данные добавлены")
insert_phone(conn,'799090909','7')




# функция, которая позволяет изменить данные о клиенте

def change_user_name(conn, name, surname, mail, phone, user_id, phone_id):
    with conn.cursor() as cursor:
        cursor.execute("UPDATE username SET name =%s, surname = %s, email = %s where id = %s;",
                       (name, surname, mail, user_id))
        cursor.execute("UPDATE phone SET phone =%s where id =%s", (phone, phone_id))


        conn.commit()
        print("Данные добавлены")
change_user_name(conn,'Alfred','Waune','@blist','8800555','10','17')


'''Функция, позволяющая удалить телефон для существующего клиента.'''
def del_user_phone(conn,phone_id):
    with conn.cursor() as cursor:
        cursor.execute(f"DELETE FROM username_phone where phone_id = '{phone_id}' ")
        cursor.execute(f"DELETE FROM phone where id = '{phone_id}' ")
        conn.commit()
del_user_phone(conn, 14)

'''Функция, позволяющая удалить существующего клиента.'''
def del_user(user_id):
    with conn.cursor() as cursor:
        # cursor.execute(f"DELETE FROM username_phone where user_id = '{user_id}' ")
        '''удалили связь между таблицами'''
        cursor.execute("ALTER TABLE username_phone  DROP CONSTRAINT username_phone_user_id_fkey")
        cursor.execute("ALTER TABLE username_phone  DROP CONSTRAINT username_phone_phone_id_fkey")


        '''выполнили каскадное удаление из user_phone до phone'''
        cursor.execute(f"DELETE FROM phone WHERE id IN (SELECT phone_id FROM username_phone where user_id = '{user_id}') ")
        cursor.execute(f"DELETE FROM username where id = '{user_id}' ")
        cursor.execute(f"DELETE FROM username_phone where user_id = '{user_id}' ")
        '''восстановили связь между таблицами'''
        cursor.execute(
            "ALTER TABLE username_phone ADD CONSTRAINT username_phone_user_id_fkey FOREIGN KEY (user_id) "
        "REFERENCES username(id)")
        cursor.execute(
            "ALTER TABLE username_phone ADD CONSTRAINT username_phone_phone_id_fkey FOREIGN KEY (phone_id) "
            "REFERENCES phone(id)"
        )
        conn.commit()
    print("Данные удалены")

del_user(9)



'''Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.'''
def select_user(user_data):
    with conn.cursor() as cursor:
        (f"SELECT name, surname, email FROM username where name ='{name}', surname = '{surname}', email ='{email}'")
        ("SELECT (name, surname, email) FROM username where name,surname,email = (%s,%s,%s)", (user_data[0], user_data[1], user_data[2]))

        ('INSERT INTO username( name, surname, email) VALUES (%s,%s,%s)', (user_data[0], user_data[1], user_data[2]))
        conn.commit()
# (f"select id from phone where phone = '{phone}'")







#     "sql - запросы"
#
# request = input('Введите номер операции\n'
#                '1.Функция, создающая структуру БД: Введите create_tables(таблицы)\n'
#                '2.Функция, позволяющая добавить нового клиента\n')
#
#
# conn = psycopg2.connect(database=DATABASENAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
#
# # Pattern matching -> Python 3.10
# match request.split():
#     # Unpacking
#     case "create_tables", :
#         create_tables(conn)
#     case "create_user", *data:
#         create_user(data,conn)
#     case _:
#         print("Ошибка ввода")
#
# # "create_user Pavel Ivanov aa@gmail.com +88005553535"