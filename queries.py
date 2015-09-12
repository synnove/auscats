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

# QUERIES FOR GETTING INFORMATION ABOUT MODULES
def get_module_info():
    """ get basic information about modules """
    modules = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT NAME, BLURB, NUM_QUESTIONS FROM MODULES WHERE status = 'ACTIVE'")
    rows = cur.fetchall()

    for row in rows:
	modules.append(row)
    conn.close()
    return modules

def get_admin_module_info():
    """ get module information for administrators """
    pass

def get_quiz_questions_by_module(module_title):
    """ get list of questions per module """
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
<<<<<<< HEAD
    """ get list of modules completed by a user """
=======
    """ get list of modules that the user has already completed """
>>>>>>> ca681758b0844ca81efa9e3f4030cb7da3e48fa0
    modules_completed = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT A.MODULE_ID FROM MODULES M,(SELECT MODULE_ID,COUNT(MODULE_ID) AS COUNT FROM vw_USER_ANSWERS WHERE USER_ID = %s GROUP BY MODULE_ID) AS A WHERE COUNT = M.NUM_QUESTIONS", [user_id])
    rows = cur.fetchall()
    for row in rows:
	modules_completed.append(row['MODULE_ID'])

    conn.close()
    return modules_completed

def get_quiz_questions_by_module(module_title):
    """ get list of questions per module """
    quiz_questions_by_module = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUIZ_QUESTIONS WHERE MODULE_ID = (SELECT MODULE_ID FROM MODULES WHERE  NAME = %s)", [module_title])
    rows = cur.fetchall()
    
    for row in rows:
	quiz_questions_by_module.append(row)
    conn.close()
    return quiz_questions_by_module
    
def get_quiz_answers():
<<<<<<< HEAD
    """ get list of all quiz answers to quiz questions"""
=======
    """ get list of answers """
>>>>>>> ca681758b0844ca81efa9e3f4030cb7da3e48fa0
    quiz_answers = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    # modify this to only get answers for one module's questions
    cur.execute("SELECT * FROM QUIZ_ANSWERS")
    rows = cur.fetchall()

    for row in rows:
	quiz_answers.append(row)
    conn.close()
    return quiz_answers

<<<<<<< HEAD
def get_number_of_correct_answers(user_id, module_title):
=======
def get_gradebook(user_id):
    """ get all of a user's entered answers """
    gradebook = list()
>>>>>>> ca681758b0844ca81efa9e3f4030cb7da3e48fa0
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(QUESTION_ID) AS QUESTIONS_CORRECT FROM vw_USER_CORRECT_ANSWERS WHERE USER_ID = %s AND MODULE_ID IN (SELECT MODULE_ID FROM MODULES WHERE NAME = %s) GROUP BY USER_ID, MODULE_ID", [user_id, module_title])
    rows = cur.fetchall()
   
    for row in rows:
	correct_answers = row['QUESTIONS_CORRECT']
    conn.close()
    return correct_answers

def get_total_number_of_questions(module_title):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("Select MODULE_ID, NUM_QUESTIONS FROM MODULES WHERE STATUS = 'ACTIVE' AND NAME = %s", [module_title])
    rows = cur.fetchall()

    for row in rows:
	number_of_questions = row['NUM_QUESTIONS']
    conn.close()
    return number_of_questions

def get_admin_user_list():
    """ get list of administrators """
    admin = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM ADMIN")
    for row in cur.fetchall():
	admin.append(row['user_id'])
    conn.close()
    return admin

def get_org_unit_info():
    """ get information about orgunits """
    org_units = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT UNIT_ID, UNIT_NAME FROM ORG_UNITS")
    for row in cur.fetchall():
	org_units.append(row)
    conn.close()
    return org_units

def get_data_for_csv(num, filters):
    """ generate data to be converted into csv as requested by user """
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
    """ check that an administrator exists """
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ADMIN WHERE USER_ID = %s", [admin_id])
    if cur.rowcount == 1:
	return True
    return False

def check_admin_perms(admin_id, permission_type):
    """ check that an administrator has the specified permission """
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ADMIN_PERM WHERE USER_ID = %s AND PERMISSION = %s",
	    [admin_id, permission_type])
    if cur.rowcount==1:
	return True
    return False

def check_orgunit_exists(orgunit):
    """ check that an orgunit exists in the database """
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ORG_UNITS WHERE UNIT_ID = %s", [orgunit])
    if cur.rowcount == 1:
	return True
    return False

def do_admin_add(admin_id):
    """ add a user to the administrator list """
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
    """ add a new orgunit """
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
    """ add permissions for a specified user """
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
    """ reads password from file """
    f = open('mysql.passwd', 'r')
    passwd = f.read()
    f.close()
    return passwd.rstrip()

def do_mysql_connect():
    """ connect to the database """
    conn = MySQLdb.connect(db='auscats', host='localhost', port=3306, 
	    user='root', passwd=read_mysql_password(), 
	    cursorclass=MySQLdb.cursors.DictCursor)
    return conn
