
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


def userExists(userid):
    try:
        c = sql.connect(
            host='sql',
            user='user',
            password='user1234',
            database='practice',
            port='3306'
        )

        cur = c.cursor()
        cur.execute("SELECT * FROM users WHERE user = %s", (userid,))
        result = cur.fetchall()

        c.close()

        return bool(len(result))
    except:
        return Exception

def addUser(userid):
    if not userExists(userid):
        try:
            c = sql.connect(
                host='sql',
                user='user',
                password='user1234',
                database='practice',
                port='3306'
            )

            cur = c.cursor()

            cur.execute('INSERT INTO users (user) VALUES (%s)', (userid,))

            c.commit()
            c.close()

            return True
        except:
            return False

    return False

def addStat(r, s, e, f):
    try:
        c = sql.connect(
            host='sql',
            user='user',
            password='user1234',
            database='practice',
            port='3306'
        )

        cur = c.cursor()

        cur.execute('INSERT INTO stats (r, s, e, f) VALUES (%s, %s, %s, %s)', (r, s, e, f,))

        c.commit()
        c.close()

        return True
    except:
        return False


def getUserCount():
    try:
        c = sql.connect(
            host='localhost',
            user='user',
            password='user1234',
            database='practice',
            port='3906'
        )

        cur = c.cursor()
        cur.execute("SELECT * FROM users")
        result = cur.fetchall()

        c.close()

        return len(result)
    except:
        return Exception

def getPopular():
    try:
        c = sql.connect(
            host='localhost',
            user='user',
            password='user1234',
            database='practice',
            port='3906'
        )

        cur = c.cursor()
        cur.execute("SELECT * FROM stats ORDER BY f DESC")

        data = cur.fetchall()[0]

        c.close()

        s = str(data[0])+ ", "

        match data[1]:
            case "None":
                sch = 'График: Не важно'
            case "fullDay":
                sch = 'График: Полный день'
            case "shift":
                sch = 'График: Сменный'
            case "flexible":
                sch = 'График: Гибкий'
            case "remote":
                sch = 'График: Удаленно'
            case "flyInFlyOut":
                sch = 'График: Вахта'

        s+=str(sch) + ', '

        match data[2]:
            case 'noExperience':
                exp = 'Без опыта'
            case 'between1And3':
                exp = 'От года до 3'
            case 'between3And6':
                exp = 'От 3 до 6'
            case 'moreThan6':
                exp = 'Более 6'

        s+=str(exp)

        return [s, data[3]]
    except Exception as e:
        return e


print(getPopular())