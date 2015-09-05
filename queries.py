import MySQLdb.cursors
import hashlib

def get_module_info():
    """ Returns a list of tuples containing the each row of data in the MODULES table 
	get_module_info() ---> List<Tuple> """
    modules = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM MODULES")
    rows = cur.fetchall()

    for row in rows:
	modules.append(row)
    conn.close()
    return modules

def get_quiz_question_info():
    """ Returns a list of tuples containing each row of data in the QUIZ_QUESTIONS table
	get_quiz_info() ---> List<Tuple> """
    quizes = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUIZ_QUESTIONS")
    rows = cur.fetchall()
    
    for row in rows:
	quizes.append(row)
    conn.close()
    return quizes


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
