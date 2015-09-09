import MySQLdb.cursors
import hashlib
from random import randrange

unit_names = ["Cat Care Specialists", "IT Infrastructure Group",
	"Grouper Group", "Tuna Group", "Salmon Group", "Stray Pig News",
	"Some People", "Some Other People", "Pretty Okay People",
	"People Who Do Stuff", "Nothing To See Here"]

people_names = ["George", "Fred", "Harry", "Hermione", "Tammy", "Imogen",
	"William", "Alexander", "David", "David", "David", "David", "Marisa",
	"Marissa", "Alice", "Sarah", "Max", "Chloe", "Warren"]

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

def get_admin_module_info():
    modules = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM MODULES")
    for row in cur.fetchall():
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

def get_quiz_questions_by_module(module_title):
    quiz_questions_by_module = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUIZ_QUESTIONS WHERE MODULE_ID = (SELECT MODULE_ID FROM MODULES WHERE  NAME = %s)", [module_title])
    rows = cur.fetchall()
    
    for row in rows:
	quiz_questions_by_module.append(row)
    conn.close()
    return quiz_questions_by_module

def modules_completed_by_user(user_id):
    modules_completed = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT MODULE_ID FROM (SELECT MODULE_ID,COUNT(MODULE_ID) AS COUNT FROM vw_USER_ANSWERS WHERE USER_ID = %s GROUP BY MODULE_ID) AS A WHERE COUNT = 3", [user_id])
    rows = cur.fetchall()

    for row in rows:
	modules_completed.append(row['MODULE_ID'])

    conn.close()
    return modules_completed
    
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

def get_gradebook(user_id):
    gradebook = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT QUESTION_ID FROM GRADEBOOK WHERE USER_ID = %s", [user_id])
    rows = cur.fetchall()

    for row in rows:
        gradebook.append(row['QUESTION_ID'])
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

def get_data_for_csv(num, filters):
    data = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    sql = "SELECT * FROM vw_USER_CORRECT_ANSWERS"
    if num >= 1:
	attrs = list(filters.keys())
	for attr in attrs:
	    if attr == attrs[0]:
		sql += (" WHERE " + attr + " = " + filters[attr] + " ")
	    else:
		sql += ("AND " + attr + " = " + filters[attr] + " ")
    cur.execute(sql)
    for row in cur.fetchall():
	data.append(row)
    conn.close()
    if len(data) >= 1:
	return data
    return None

def check_admin_exists(admin_id):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ADMIN WHERE USER_ID = %s", [admin_id])
    if cur.rowcount == 1:
	return True
    return False

def check_admin_perms(admin_id, permission_type):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ADMIN_PERM WHERE USER_ID = %s AND PERMISSION = %s",
	    [admin_id, permission_type])
    if cur.rowcount==1:
	return True
    return False

def check_orgunit_exists(orgunit):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ORG_UNITS WHERE UNIT_ID = %s", [orgunit])
    if cur.rowcount == 1:
	return True
    return False

def do_admin_add(admin_id):
    conn = do_mysql_connect()
    cur = conn.cursor()
    orgunit = randrange(1,500) #artificially generating orgunit, get value from ldap
    do_add_orgunit(orgunit)
    if not check_admin_exists(admin_id):
        try:
            cur.execute("INSERT INTO ADMIN (USER_ID, NAME, UNIT_ID) VALUES (%s, %s, %s)", 
        	    [admin_id, people_names[randrange(0,len(people_names))], orgunit])
            conn.commit()
            return 0
        except MySQLdb.Error as e:
            conn.rollback()
	    return e
    conn.close()
    return -1

def do_add_orgunit(orgunit):
    conn = do_mysql_connect()
    cur = conn.cursor()
    if not check_orgunit_exists(orgunit):
        try:
            cur.execute("INSERT INTO ORG_UNITS (UNIT_ID, UNIT_NAME) VALUES (%s, %s)", 
        	    [orgunit, unit_names[randrange(0,len(unit_names))]])
            conn.commit()
            return 0
        except MySQLdb.Error as e:
            conn.rollback()
    conn.close()
    return -1

def do_admin_add_perms(admin_id, permission):
    conn = do_mysql_connect()
    cur = conn.cursor()
    if not check_admin_perms(admin_id, permission):
	try:
	    cur.execute("INSERT INTO ADMIN_PERM (USER_ID, PERMISSION) VALUES (%s, %s)", 
		    [admin_id, permission])
	    conn.commit()
	    return 0
	except MySQLdb.Error as e:
	    conn.rollback()
    conn.close()
    return -1

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
