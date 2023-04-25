import psycopg2

from config import HOST, PORT, USER,PASSWORD, DATABASENAME

conn = psycopg2.connect(database =DATABASENAME, user = USER, password = PASSWORD,host = HOST, port = PORT)
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

