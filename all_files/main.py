import psycopg2

from config import HOST, PORT, USER, PASSWORD, DATABASENAME

conn = psycopg2.connect(database=DATABASENAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
with conn.cursor() as cursor:
    # Попытка выполнение транзации
    try:
        cursor.execute('create table username(id bigint generated always as identity primary key,'
                       'name VARCHAR(50), surname varchar(50), email varchar(100))')
        cursor.execute('create table phone(id bigint generated always as identity primary key,'
                       'phone VARCHAR(20))')
        cursor.execute('create table username_phone(user_id bigint references username(id),'
                       'phone_id bigint references phone(id))')





    # При возникновении ошибки
    except Exception as error:
        # Отмена последней транзакции
        conn.rollback()
        print(str(error))

    # Если транзакция была выполнена успешно
    else:
        # Сохранение транзации
        conn.commit()
        # save result of transaction
        print("Successful transaction")


def insert_phone(conn, phone, user_id):
    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO phone(phone) VALUES ('{phone}')")
        '''вставляем телефон'''
        cursor.execute(f"select id from phone where phone = '{phone}'")
        cursor.execute('INSERT INTO username_phone(user_id,phone_id) values (%s,%s)',
                       (user_id, cursor.fetchall()[0][0]))
        '''нашли id телефона из phone'''
        conn.commit()
        print("Данные добавлены")


insert_phone(conn, '799090909', '1')


#

def change_user_name(conn, name=None, surname=None, mail=None, phone=None, user_id, phone_id):
    with conn.cursor() as cursor:


cursor.execute("UPDATE username SET name =%s, surname = %s, email = %s where id = %s;",
               (name, surname, mail, user_id))
cursor.execute("UPDATE phone SET phone =%s where id =%s", (phone, phone_id))

conn.commit()
print("Данные добавлены")


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