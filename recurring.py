import utils
from datetime import datetime, timedelta

def getNotDones():
    """Goes through tables and identifies recurring items w/o open gt first of next month. Creates PPL_INPT record for those."""
    sql = """select USER_DEFINED_2 from quality.PPL_INPT_RCUR pir left join PEOPLE_INPUT pi on pir.RECUR_ID = pi.USER_DEFINED_2 
            where CLOSED = 'N' and pi.DUE_DATE > LAST_DAY(CURRENT_DATE())"""
    alreadyDone = utils.getDatabaseData(sql)
    done = []
    notDone = []
    for rid in alreadyDone:
        done.append(rid[0])
    recurrers = utils.getDatabaseData("select * from PPL_INPT_RCUR")
    for row in recurrers:
        if row[0] in done:
            print(f"Future action already exists: {row[0]}")
        else:
            notDone.append(row)
            print(f"Not done: {row[0]}")
    
    return notDone

def createInputRecords(notDones):
    """Creates PPL_INPT records for recurring items."""
    input_date = datetime.today()
    nextMonth = datetime.today() + timedelta(days=32)
    fdonm = nextMonth.replace(day=1)    

    for notDone in notDones:
        nid = utils.getNextSysid("INPUT_ID")
        rid = notDone[0]
        iid = notDone[1]
        assto = notDone[2]
        frequency = notDone[3]
        subject = notDone[4]
        projectid = utils.getProjectId(iid)

        #determine due date
        match frequency:
            case "W":
                due_date = datetime.today() + timedelta(days=7)
                # Wednesday
                if due_date.weekday() == 5:
                    replacement_date = due_date - timedelta(days=2)
                    due_date = replacement_date
                    break
                # Thursday
                if due_date.weekday() == 4:
                    replacement_date = due_date - timedelta(days=3)
                    due_date = replacement_date
                    break
                # Friday
                if due_date.weekday() == 5:
                    replacement_date = due_date - timedelta(days=4)
                    due_date = replacement_date
                    break
                # Saturday
                elif due_date.weekday() == 6:
                    replacement_date = due_date - timedelta(days=4)
                    due_date = replacement_date
                    break

                input_date = due_date - timedelta(days=10)


            case "M":
                # nextMonth = datetime.today() + timedelta(days=32)
                due_date = nextMonth.replace(day=1)
                input_date = due_date
            case "Q":
                due_date = datetime.today() + timedelta(weeks=12)
                due_date = due_date.replace(day=1)
                input_date = due_date
            case "A":
                due_date = datetime.today() + timedelta(days=365)
                due_date = due_date.replace(day=1)
                input_date = due_date - timedelta(days=10)

            case "BE":
                intwoyears = datetime.today() + timedelta(days=365*2)
                due_date = intwoyears
                input_date = due_date - timedelta(days=10)

        
        input_date = input_date.strftime('%Y-%m-%d')

        updateSql = (f"insert into PEOPLE_INPUT (INPUT_ID"
        ", INPUT_DATE"
        ", PEOPLE_ID"
        ", INPUT_TYPE"
        ", SUBJECT"
        ", ASSIGNED_TO"
        ", DUE_DATE"
        ", CLOSED"
        ", PROJECT_ID"
        ", USER_DEFINED_2"
        ", CREATE_BY"
        ", CREATE_DATE) values ("
        "'{nid}'"
        ", '{date}'"
        ", 'TKENT'"
        ", 'DATA'"
        ", '{subject}'"
        ", '{assto}'"
        ", '{due_date}'"
        ", 'N'"
        ", '{projectid}'"
        ", '{rid}'"
        ", 'RCUR'"
        ", NOW() )".format(nid=nid, date=fdonm, due_date=due_date, subject=subject, assto=assto, projectid=projectid, rid=rid))
        # print(updateSql)
        utils.updateDatabaseData(updateSql)
        # copy text from recurring item to new input record
        text = utils.getDatabaseData(f"select INPUT_TEXT from PPL_INPT_TEXT where INPUT_ID = '{iid}'")
        text = text[0][0]
        text = text.replace("'", "\\'")
        updateSql = f"insert into PPL_INPT_TEXT values ('{nid}', '{text}')"
        utils.updateDatabaseData(updateSql)

def main():
    # print(getNotDones())
    print("Starting recurring action items...")
    notdones = getNotDones()
    createInputRecords(notdones)
    print("Done.")


if __name__ == '__main__':
    main()
    print("Done.")