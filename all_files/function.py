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


# Функция, позволяющая удалить телефон для существующего клиента.
def del_user_phone(conn,phone_id):
    with conn.cursor() as cursor:
        cursor.execute(f"DELETE FROM username_phone where phone_id = '{phone_id}' ")
        cursor.execute(f"DELETE FROM phone where id = '{phone_id}' ")
        conn.commit()
del_user_phone(conn, 14)


# Функция, позволяющая удалить существующего клиента
def del_user(user_id):
    with conn.cursor() as cursor:

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


# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def select_user(name=None,surname=None, email=None, phone=None):
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
        cursor.execute(f"SELECT * FROM username LEFT JOIN username_phone on username_phone.user_id = username.id WHERE phone_id IN(SELECT id FROM phone where phone = '{phone}')")

        print(cursor.fetchall())
print(select_user(phone='8800555'))
