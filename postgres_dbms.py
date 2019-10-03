import psycopg2
import sys
import datetime
import os

#Connection variables Declaration
conn = psycopg2.connect(database = 'postgres',user="postgres", password="postgre123",host="127.0.0.1", port="5432")
c = conn.cursor()

def verifyManager(username,password,c):
    cmd = '''  select * from manager'''
    c.execute(cmd)
    tab = c.fetchall()
    for row in tab:
        if row[0] == int(username) and row[1]==password:
            return True 
    return False  

def verifyEmployee(username,password,c):
    cmd = '''  select * from employee'''
    c.execute(cmd)
    tab = c.fetchall()
    for row in tab:
        if row[0] == int(username) and row[9]==password:
            return True 
    return False  

def viewLog(username,c):
    c.execute("select * from leave_log where leave_id in (select leave_id from emp_leave where emp_id = '{}')".format(username))
    tab = c.fetchall()
    print(tab)
    return tab
# def man_login():
# 	if not(man_id.isdigit()):
# 		print("\nWrong Employee ID")
# 		closedb()
	
# 	q = "select man_password from manager where man_id = "+man_id+";"
# 	cursor.execute(q)
# 	result = cursor.fetchone()

# 	if result is None:
# 		print("\nWrong Manager ID")
# 		closedb()
# 	if result[0] == pass_word:
# 		print("\nSuccessful Login\n")
# 	else:
# 		print("\nWrong password")
# 		closedb()
# 	X = PrettyTable()
# 	Y = PrettyTable()
# 	q="select * from leave_log where leave_id in(select leave_id from emp_leave where emp_id in (select emp_id from employee where dept_id=(select dept_id from department where man_id="+man_id+"))) and status='Pending';"
# 	cursor.execute(q)
# 	result = cursor.fetchall()
# 	q = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'leave_log' ORDER BY ORDINAL_POSITION"
# 	cursor.execute(q)
# 	col_names = cursor.fetchall()
# 	for i in range(len(col_names)):
# 		col_names[i] = ''.join(col_names[i])
# 	X.field_names = col_names
# 	for i in range(len(col_names)):
# 		col_names[i] = ''.join(col_names[i])
# 	X.field_names = col_names
# 	for i in result:
# 		X.add_row(i)

# 	print(X)
# 	if len(result)==0:
# 		print("No requests available")
# 	else:
# 		result1 = int(input("Choose the required leave id "))
# 		q = "select emp_id from emp_leave where leave_id = "+str(result1)+';'
# 		cursor.execute(q)
# 		a = cursor.fetchone()
# 		q = "select * from employee where emp_id = "+str(a[0])+';'
# 		cursor.execute(q)
# 		result = cursor.fetchall()
# 		# q = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'employee' ORDER BY ORDINAL_POSITION"
# 		# cursor.execute(q)
# 		# col_names = cursor.fetchall()
# 		# for i in range(len(col_names)):
# 		# 	col_names[i] = ''.join(col_names[i])
# 		# Y.field_names = col_names
# 		for i in result:
# 			Y.add_row(i)

# 		print(Y)

# 		b = input("\nDo you want to approve or disapprove (Yes/No)")
# 		if b=='Yes':
# 			q = "update leave_log set status='Approved' where leave_id = "+str(result1)+";"
# 			#print (q)
# 			cursor.execute(q)
# 			connection.commit()
# 			print("Successfully updated")
# 		else:
# 			q = "update leave_log set status='Not Approved' where leave_id = "+str(result1)+';'
# 			cursor.execute(q)
# 			#print("Successfully updated")
# 		closedb()

# def genlid():
# 	q = "select max(leave_id) from leave_log;"
# 	c.execute(q)
# 	return (c.fetchone()[0]+1)

# def applyleave():
# 	leave_id = genlid()
# 	print("Start Date (DD-MM-YYYY):",end = ' ')
# 	start_date = input()
# 	print("End Date (DD-MM-YYYY):",end = ' ')
# 	end_date = input()
# 	print("Type (PL/SL/CL):",end = ' ')
# 	l_type = input()
# 	print("Reason:",end = ' ')
# 	reason = input()
# 	today = datetime.date.today()
# 	d1 = today.strftime("%d/%m/%Y")
# 	apply_date = datetime.datetime.strptime(d1,"%d/%m/%Y").strftime("%Y-%m-%d")
# 	status  = "Pending"
# 	q = "insert into leave_log values("+str(leave_id)+",'"+start_date+"','"+end_date+"','"+reason+"','"+l_type+"','"+status+"','"+apply_date+"',NULL);"
# 	c.execute(q)
# 	q = "insert into emp_leave values("+str(emp_id)+","+str(leave_id)+");"
# 	c.execute(q)
# 	print("Successful Applied")

# #Closing database connection
# def closedb():
# 	if(connection):
# 	    c.close()
# 	    connection.close()
# 	print("\nPostgreSQL connection is closed")
# 	sys.exit()



