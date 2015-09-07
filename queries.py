import MySQLdb.cursors
import hashlib

def get_module_info():
    modules = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM MODULES")
    rows = cur.fetchall()

    for row in rows:
	modules.append(row)
    conn.close()
    return modules

def get_active_modules():
    active_modules = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT module_id, name, blurb FROM MODULES WHERE status = 'ACTIVE'" )
    rows = cur.fetchall()
    
    for row in rows:
	active_modules.append(row)
    conn.close()
    return active_modules

def get_quiz_questions():
    quiz_questions = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUIZ_QUESTIONS")
    rows = cur.fetchall()
    
    for row in rows:
	quiz_questions.append(row)
    conn.close()
    return quiz_questions

def get_quiz_answers():
    quiz_answers = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUIZ_ANSWERS")
    rows = cur.fetchall()

    for row in rows:
	quiz_answers.append(row)
    conn.close()
    return quiz_answers

def get_gradebook():
    gradebook = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT user_id, question_id FROM GRADEBOOK")
    rows = cur.fetchall()

    for row in rows:
        gradebook.append(row)
    conn.close()
    return gradebook

def get_admin_user_list():
    admin = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM ADMIN")
    for row in cur.fetchall():
	admin.append(row['user_id'])
    conn.close()
    return admin

def get_org_unit_info():
    org_units = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT UNIT_ID, UNIT_NAME FROM ORG_UNITS")
    for row in cur.fetchall():
	org_units.append(row)
    conn.close()
    return org_units

def get_data_for_csv():
    data = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vw_USER_CORRECT_ANSWERS")
    for row in cur.fetchall():
	data.append(row)
    conn.close()
    return data

def read_mysql_password():
    f = open('mysql.passwd', 'r')
    passwd = f.read()
    f.close()
    return passwd.rstrip()

def do_mysql_connect():
    conn = MySQLdb.connect(db='auscats', host='localhost', port=3306, 
	    user='root', passwd=read_mysql_password(), 
	    cursorclass=MySQLdb.cursors.DictCursor)
    return conn
