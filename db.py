
import mysql.connector as sql

def createUsers():
    try:
        c = sql.connect(
            host='sql',
            user='user',
            password='user1234',
            database='practice',
            port='3306'
        )

        cur = c.cursor()

        cur.execute('CREATE TABLE users (id INT PRIMARY KEY AUTO_INCREMENT, user VARCHAR(255))')

        c.commit()
        c.close()

        print('таблица users создана')
        return
    except:
        print('не удалось создать таблицу users')
        return


def createStats():
    try:
        c = sql.connect(
            host='sql',
            user='user',
            password='user1234',
            database='practice',
            port='3306'
        )

        cur = c.cursor()

        cur.execute('CREATE TABLE `stats` (r VARCHAR(255), s VARCHAR(255), e VARCHAR(255), f INT)')

        c.commit()
        c.close()

        print('таблица stats создана')
        return
    except:
        print('не удалось создать таблицу stats')
        return


def 