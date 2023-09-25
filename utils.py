import os
from datetime import datetime


def ranToday(script):
    match script:
        case "sysdoc":
            print(f"{script} script")
            sysdocFile = "C:\\Users\\timk\\Documents\\Python\\sysdoc\\sysdoc.txt"
            if os.path.exists(sysdocFile):
                with open(sysdocFile, "r") as f:
                    lastRun = f.readline()
                if lastRun == str(datetime.now().date()):
                    return True
                else:
                    with open(sysdocFile, "w") as f:
                        f.write(str(datetime.now().date()))
                    return False
            else:
                with open(sysdocFile, "w") as f:
                    f.write(str(datetime.now().date()))
                return False
        case default:
            return True



def getDatabaseData(sql):
    import mysql.connector
    from mysql.connector import Error
    try:
        connection = mysql.connector.connect(host='ciqms.chgubqsqxrvz.us-east-2.rds.amazonaws.com',
                                             database='quality',
                                             user='admin',
                                             password='A1rplane$$$')
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            return records

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def sendMail(to_email, subject, message, from_email="quality@ci-aviation.com", cc_email=""):
    import smtplib, ssl
    from email.message import EmailMessage
    PORT = 465
    SERVER = "sh10.nethosting.com"
    CONTEXT = ssl.create_default_context()
    if from_email == "tim":
        USERNAME = "tim.kent@ci-aviation.com"
        PASSWORD = "#A1rplane23"

    else:
        USERNAME = "quality@ci-aviation.com"
        PASSWORD = "#A1rplane2023"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = USERNAME
    msg["To"] = to_email
    msg["Cc"] = cc_email
    msg.set_content(message)
    server = smtplib.SMTP_SSL(SERVER, PORT, context=CONTEXT)
    server.login(USERNAME, PASSWORD)
    server.send_message(msg)
    server.quit()


def updateDatabaseData(sql):
    # print(sql)
    table = sql.split()[2]
    import mysql.connector
    from mysql.connector import Error
    try:
        connection = mysql.connector.connect(host='ciqms.chgubqsqxrvz.us-east-2.rds.amazonaws.com',
                                              database='quality',
                                              user='admin',
                                              password='A1rplane$$$')
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            print(f"Inserted into {table}")
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            connection.close()


def emailAddress(name):
    import mysql.connector
    from mysql.connector import Error
    sql = f"select WORK_EMAIL_ADDRESS from PEOPLE where PEOPLE_ID = '{name}'"
    # print(sql)
    try:
        connection = mysql.connector.connect(host='ciqms.chgubqsqxrvz.us-east-2.rds.amazonaws.com',
                                              database='quality',
                                              user='admin',
                                              password='A1rplane$$$')
        if connection.is_connected():
            cursor = connection.cursor(buffered=True)
            cursor.execute(sql)
            # connection.commit()
            email = cursor.fetchone()
            # print(email)
            return email[0]
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            connection.close()