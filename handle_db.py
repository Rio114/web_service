import sqlite3
from contextlib import closing


def db_save_image(rect_data):
    db_name = 'database.db'

    with closing(sqlite3.connect(db_name)) as conn:
        c = conn.cursor()
        create_table = '''CREATE TABLE IF NOT EXISTS images (id integer primary key, file_name varchar(64), x_pos int, y_pos int, width int, hight int)'''
        c.execute(create_table)
        insert_sql = 'INSERT INTO images (file_name, x_pos, y_pos, width, hight) values (?, ?, ?, ?, ?)'
        c.executemany(insert_sql, rect_data)
        conn.commit()

        # select_sql = 'SELECT * FROM images'
        # for row in c.execute(select_sql):
        #     print(row)


# with closing(sqlite3.connect(db_name)) as conn:
#     c = conn.cursor()

#     create_table = '''CREATE TABLE IF NOT EXISTS images (id integer primary key, file_name varchar(64), x_pos int, y_pos int, width int, hight int)'''
#     c.execute(create_table)

#     sql = 'INSERT INTO images (file_name, x_pos, y_pos, width, hight) values (?, ?, ?, ?, ?)'
#     file_name = ('test.jpg', 200, 100, 50, 50)
#     c.execute(sql, file_name)

#     insert_sql = 'INSERT INTO images (file_name, x_pos, y_pos, width, hight) values (?, ?, ?, ?, ?)'
#     file_names = [
#         ('test1.jpg', 200, 100, 50, 50),
#         ('test2.jpg', 100, 120, 100, 50),
#         ('test3.jpg', 300, 140, 140, 45),
#         ('test4.jpg', 400, 110, 50, 50)
#     ]

#     c.executemany(insert_sql, file_names)

#     conn.commit()

#     select_sql = 'SELECT * FROM images'
#     for row in c.execute(select_sql):
#         print(row)