import psycopg2
import sys
import datetime
import os

# Connection variables Declaration
conn = psycopg2.connect(database='postgres', user="postgres",
                        password="postgre123", host="127.0.0.1", port="5432")
c = conn.cursor()


def verifyManager(username, password, c):
    cmd = '''  select * from manager'''
    c.execute(cmd)
    tab = c.fetchall()
    for row in tab:
        if row[0] == int(username) and row[1] == password:
            return True
    return False


def verifyEmployee(username, password, c):
    cmd = '''  select * from employee'''
    c.execute(cmd)
    tab = c.fetchall()
    for row in tab:
        if row[0] == int(username) and row[9] == password:
            return True
    return False


def viewLog(username, c):
    c.execute("select * from leave_log where leave_id in (select leave_id from emp_leave where emp_id = '{}');".format(username))
    tab = c.fetchall()
    log = []
    for e in tab:
        temp = list(e)
        log.append(temp)
    return log


def viewPending(username, c):
    c.execute("select * from leave_log where leave_id in(select leave_id from emp_leave where emp_id in (select emp_id from employee where dept_id=(select dept_id from department where man_id='{}'))) and status='Pending';".format(username))
    tab = c.fetchall()
    log = []
    for e in tab:
        temp = list(e)
        log.append(temp)
    return log


def manageLeave(leave_id, status, c):
    print(leave_id, status)
    today = datetime.date.today()
    d1 = today.strftime("%d/%m/%Y")
    approve_date = datetime.datetime.strptime(
        d1, "%d/%m/%Y").strftime("%Y-%m-%d")
    if status == 'approve':
        q = "update leave_log set status='Approved' where leave_id = {};".format(
            leave_id)
        print(q)
        c.execute(q)
    elif status == 'reject':
        q = "update leave_log set status='Not Approved' where leave_id = {};".format(
            leave_id)
        print(q)
        c.execute(q)
    q = "update leave_log set approved_date='{}' where leave_id = {};".format(
        approve_date, leave_id)
    print(q)
    c.execute(q)
    conn.commit()
    print("Successfully updated")


def genlid(c):
    q = "select max(leave_id) from leave_log;"
    c.execute(q)
    result = c.fetchone()
    if(len(result) == 0):
        return (70001)
    return (result[0]+1)


def applyleave(emp_id, start_date, end_date, l_type, reason, c):
    leave_id = genlid(c)
    today = datetime.date.today()
    d1 = today.strftime("%d/%m/%Y")
    apply_date = datetime.datetime.strptime(
        d1, "%d/%m/%Y").strftime("%Y-%m-%d")
    status = "Pending"
    q = "insert into leave_log values("+str(leave_id)+",'"+start_date+"','" + \
        end_date+"','"+reason+"','"+l_type+"','"+status+"','"+apply_date+"',NULL);"
    c.execute(q)
    print(q)
    q = "insert into emp_leave values("+str(emp_id)+","+str(leave_id)+");"
    c.execute(q)
    print(q)
    conn.commit()
    print("Successful Applied")

# Closing database connection


def closedb():
	if(conn):
	    c.close()
	    conn.close()
	print("\nPostgreSQL connection is closed")
	sys.exit()


def viewTable(c, table_name):
	cmd = '''  select * from {}  '''.format(table_name)
	c.execute(cmd)
	tab = c.fetchall()
	for row in tab: print(row)


def executeFile(fn, c, conn):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file = open(dir_path+'/SQLfiles/{}'.format(fn)).read()
    cmds = file.split(';')
    for cmd in cmds[:-1]:
        try:
            c.execute(cmd)
        except Exception as exc:
            c,conn = reconnectDB(c,conn)
            print(cmd)
            print(exc)
        print(cmd)
    return c,conn

def reconnectDB(c,conn):
	conn.commit()
	conn.close()
	conn = psycopg2.connect(database='postgres', user="postgres",
                        password="postgre123", host="127.0.0.1", port="5432")
	c = conn.cursor()
	return c,conn

def refreshDB(c,conn):
    c,conn  = executeFile('dropper_db.sql' , c, conn)
    c,conn = reconnectDB(c,conn)
    c,conn = executeFile('creater_db.sql' , c, conn)
    c,conn = reconnectDB(c,conn)
    c,conn = executeFile('inserter_db.sql', c, conn)
    c,conn = reconnectDB(c,conn)
    print("Database restarted")
    return c,conn
