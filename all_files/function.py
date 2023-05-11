import psycopg2
from config import HOST, PORT, USER, PASSWORD, DATABASENAME

conn = psycopg2.connect(database=DATABASENAME, user=USER, password=PASSWORD, host=HOST, port=PORT)


# Функция, создающая структуру БД (таблицы).
# def create_tables(conn):
#
#     with conn.cursor() as cursor:
#         # Попытка выполнение транзации
#
#         cursor.execute('create table username(id bigint generated always as identity primary key,'
#                        'name VARCHAR(50), surname varchar(50), email varchar(100))')
#         cursor.execute('create table phone(id bigint generated always as identity primary key,'
#                        'phone VARCHAR(20))')
#
#         cursor.execute('ALTER TABLE phone ADD user_id bigint references username(id)')
#         conn.commit()
# # create_tables(conn)
#
# Функция, позволяющая добавить нового клиента.
# def create_user(user_data: list, conn):
#     with conn.cursor() as cursor:
#         # Попытка выполнение транзации
#
#         cursor.execute( 'INSERT INTO username( name, surname, email) VALUES (%s,%s,%s)',(user_data[0],user_data[1],user_data[2]))
#
#         conn.commit()
#         print("Данные добавлены")
#
# create_user(['Варений','Mеладзе','@'],conn)
# # create_user(['Jack','London','@.GB'],conn)
#
#
# функция, позволяющая добавить телефон для существующего клиента
# def insert_phone(conn,phone,user_id):
#     with conn.cursor() as cursor:
#         cursor.execute(f"INSERT INTO phone(phone,user_id) VALUES ('{phone}','{user_id}')")
#
#         conn.commit()
#         print("Данные добавлены")
# insert_phone(conn,'89036888888',2)
# #
#
# функция, которая позволяет изменить данные о клиенте
# def change_user_name(conn, user_id,phone_id, name=None, surname=None, mail=None,phone=None ):
#     with conn.cursor() as cursor:
#         if name:
#            cursor.execute("UPDATE username SET name =%s where id =%s;",(name,user_id))
#
#         if surname:
#             cursor.execute("UPDATE username SET surname =%s where id =%s;",(surname,user_id))
#
#         if mail:
#             cursor.execute("UPDATE username SET mail =%s where id =%s;",(mail,user_id))
#
#         if phone:
#             cursor.execute("UPDATE phone SET phone =%s where id =%s;", (phone, phone_id))
#
#         conn.commit()
#         print("Данные добавлены")
#
#
#
#
# change_user_name(conn,'1','4',name='Pavel' )
#
#
# Функция, позволяющая удалить телефон для существующего клиента.
# def del_user_phone(conn,id_user):
#     with conn.cursor() as cursor:
#         cursor.execute(f"DELETE FROM phone where user_id = '{id_user}' ")
#         conn.commit()
# del_user_phone(conn, 1)

#
# Функция, позволяющая удалить существующего клиента
# def del_user(user_id):
#     with conn.cursor() as cursor:
#
#         cursor.execute(f"DELETE FROM phone WHERE (user_id = '{user_id}') ")
#         cursor.execute(f"DELETE FROM username where (id = '{user_id}') ")
#         conn.commit()
#     print("Данные удалены")
#
# del_user(1)
# #
#
# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def select_user(name=None,surname=None,email=None,phone=None):
    if name:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM username where name = '{name}' ")
        print(cursor.fetchall())
    if surname:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM username where surname = '{surname}' ")
        print(cursor.fetchall())
    if email:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM username where email = '{email}' ")
        print(cursor.fetchall())
    if phone:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM username LEFT JOIN phone on username.id = phone.user_id WHERE phone = '{phone}'")

        print(cursor.fetchall())
select_user(phone='89036888888')
