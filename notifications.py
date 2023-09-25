import utils
from email.message import EmailMessage
from datetime import datetime, timedelta
import sysdoc, setup, corrective, input


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


def formatOverdueASL(overdueASL):
    formattedOverdueASL = "<table><tr><th>Supplier ID</th><th>Name</th><th>City</th><th>Active</th><th>QMS</th><th>Certificate</th><th>Expiry</th><th>Scope</th><th>Comments</th></tr>"
    for row in overdueASL:
        formattedOverdueASL += "<tr>"
        for item in row:
            formattedOverdueASL += "<td>" + str(item) + "</td>" 
        formattedOverdueASL += "</tr>"
    formattedOverdueASL += "</table>"
    return formattedOverdueASL


def main():
    """Goes through tables and identifies overdue items. Sends email to appropriate people."""
    
    # ASL=======================================================
    sql1 = "select s.SUPPLIER_ID, s.NAME, s.CITY, s.STATUS, sq.QMS, sq.CERTIFICATE, sq.EXPIRY, ss.SCOPE, sc.COMMENTS from SUPPLIER s left join SUPPLIER_QMS sq on s.SUPPLIER_ID = sq.SUPPLIER_ID left join SUPPLIER_SCOPE ss on s.SUPPLIER_ID = ss.SUPPLIER_ID left join SUPPLIER_COMMENTS sc on s.SUPPLIER_ID = sc.SUPPLIER_ID where STATUS = 'A' and datediff(Now(),EXPIRY)>1;"
    overDueASL = utils.getDatabaseData(sql1)
    # formattedOverdueASL = formatOverdueASL(overDueASL)
    overDueASL = "Overdue ASL: \n" + str(overDueASL) + "\n"
    print(overDueASL)
    if overDueASL != "Overdue ASL: \n[]\n":
        utils.sendMail(to_email=["tim.kent@ci-aviation.com"], subject="Overdue ASL", message=overDueASL)
    else:
        print("No overdue ASL")


    # Training==================================================
    sql2 = "select * from CTA_ATTENDANCE where datediff(Now(),EXPIRATION_DATE)>1;"
    overDueTraining = utils.getDatabaseData(sql2)
    overDueTraining = "Overdue Training: \n" + str(overDueTraining) + "\n"
    print(overDueTraining)
    if overDueTraining != "Overdue Training: \n[]\n":
        utils.sendMail(to_email=["tim.kent@ci-aviation.com"], subject="Overdue Training", message=overDueTraining)
    else:
        print("No overdue training")


    # Annual Quality Policy Review==(QAM 5.3))=================================
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


if __name__ == "__main__":
    main()
    setup.main()
    setup.distro()
    sysdoc.main()
    corrective.main()
    input.main()
    print("Done.")