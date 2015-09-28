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
    cur.execute("SELECT MODULE_ID, NAME, BLURB, NUM_QUESTIONS FROM MODULES WHERE status = 'ACTIVE'")
    rows = cur.fetchall()
    for row in rows:
	modules.append(row)
    conn.close()
    return modules

def get_module_id_from_name(module_name):
    """ get id from module name """
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT MODULE_ID FROM MODULES WHERE NAME = %s", [module_name])
    row = cur.fetchone()
    conn.close()
    return row['MODULE_ID']

def get_module_names():
    """ get list of module names to check against"""
    modules = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT NAME FROM MODULES WHERE status = 'ACTIVE'")
    rows = cur.fetchall()
    for row in rows:
	modules.append(row['NAME'].lower())
    conn.close()
    return modules

def get_admin_module_info(status):
    """ get module information for administrators """
    modules = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vw_ADMIN_MODULE_INFO WHERE STATUS = %s", [status])
    rows = cur.fetchall()
    for row in rows:
	modules.append(row)
    conn.close()
    return modules

def get_last_updated_module():
    """ get module information for administrators """
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vw_ADMIN_MODULE_INFO ORDER BY LAST_UPDATED DESC LIMIT 1")
    module = cur.fetchone()
    return module

def get_quiz_questions_by_module(module_id):
    """ get list of questions per module """
    questions = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUIZ_QUESTIONS WHERE MODULE_ID = %s", [module_id])
    rows = cur.fetchall()
    for row in rows:
	questions.append(row)
    conn.close()
    return questions

def get_question_statistics():
    """ get question statistics """
    stats = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT QUESTION_ID, PERCENT_SUCCESS FROM vw_QUESTION_STATISTICS")
    rows = cur.fetchall()
    for row in rows:
	stats.append(row)
    conn.close()
    return stats

def get_correct_answers():
    """ get list of correct answers """
    answers = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM CORRECT_ANSWERS")
    rows = cur.fetchall()
    for row in rows:
	answers.append(row['ANSWER_ID'])
    conn.close()
    return answers

def get_answers_by_user(uid):
    """ get list of correct answers """
    answers = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM GRADEBOOK WHERE USER_ID = %s", [uid])
    rows = cur.fetchall()
    for row in rows:
	answers.append(row['ANSWER_ID'])
    conn.close()
    return answers

def modules_completed_by_user(user_id):
    """ get list of modules that the user has already completed """
    modules_completed = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT A.MODULE_ID FROM MODULES M,(SELECT MODULE_ID,COUNT(MODULE_ID) AS COUNT FROM vw_USER_ANSWERS WHERE USER_ID = %s GROUP BY MODULE_ID) AS A WHERE COUNT = M.NUM_QUESTIONS", [user_id])
    rows = cur.fetchall()
    for row in rows:
	modules_completed.append(row['MODULE_ID'])
    conn.close()
    return modules_completed

def get_modules_started_by_user(user_id):
    """ get list of modules started by the user; module could be completed or not"""
    modules_started = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT MODULE_ID FROM USER_PROGRESS WHERE USER_ID=%s", [user_id])
    rows = cur.fetchall()
    for row in rows:
	modules_started.append(row['MODULE_ID'])
    conn.close()
    return modules_started

def get_last_viewed_slide_by_user(user_id):
    """ get list of last viewed slide for modules in progress by user """
    last_viewed_slides = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT MODULE_ID, LAST_VIEWED FROM USER_PROGRESS WHERE USER_ID=%s", [user_id])
    rows = cur.fetchall()
    for row in rows:
	last_viewed_slides.append(row)
    conn.close()
    return last_viewed_slides


def get_quiz_questions_by_module(module_id):
    """ get list of questions per module """
    quiz_questions_by_module = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUIZ_QUESTIONS WHERE MODULE_ID = %s", [module_id])
    rows = cur.fetchall()
    for row in rows:
	quiz_questions_by_module.append(row)
    conn.close()
    return quiz_questions_by_module
    
def get_quiz_answers():
    """ get list of all quiz answers to quiz questions"""
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

def get_number_of_correct_answers(user_id, module_title):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(QUESTION_ID) AS QUESTIONS_CORRECT FROM vw_USER_CORRECT_ANSWERS WHERE USER_ID = %s AND MODULE_ID IN (SELECT MODULE_ID FROM MODULES WHERE NAME = %s) GROUP BY USER_ID, MODULE_ID", [user_id, module_title])
    rows = cur.fetchall()
    
    if (rows):
	for row in rows:
	    correct_answers = row['QUESTIONS_CORRECT']
    else:
        correct_answers = 0
    
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

def check_answer_exists(uid, qid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("Select * FROM GRADEBOOK WHERE USER_ID = %s AND QUESTION_ID = %s",
	    [uid, qid])
    if cur.rowcount == 1:
	return True
    return False

def check_answer_valid(qid, aid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("Select * FROM QUIZ_ANSWERS WHERE QUESTION_ID = %s AND ANSWER_ID = %s",
	    [qid, aid])
    if cur.rowcount == 1:
	return True
    return False

def add_answer_to_gradebook(uid, orgunit, qid, aid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    try:
	cur.execute("INSERT INTO GRADEBOOK (USER_ID, ORG_UNIT, QUESTION_ID, ANSWER_ID) VALUES (%s, %s, %s, %s)", 
		[uid, orgunit, qid, aid])
	conn.commit()
	return 0
    except MySQLdb.Error as e:
	conn.rollback()
    conn.close()

def check_answer_correct(aid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("Select * FROM CORRECT_ANSWERS WHERE ANSWER_ID = %s", [aid])
    if cur.rowcount == 1:
	return True
    return False

def log_user_answer(uid, dn, qid, aid):
    if not check_answer_exists(uid, qid):
	if check_answer_valid(qid, aid):
	    orgunit = dn[0].split(",")[1][3:]
	    add_answer_to_gradebook(uid, orgunit, qid, aid)
	    if check_answer_correct(aid):
		return 0
	    return 1
    return -1

# QUERIES FOR GETTING INFORMATION ABOUT ADMIN-RELATED THINGS
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
    sql = "SELECT * FROM vw_USER_ANSWERS"
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
