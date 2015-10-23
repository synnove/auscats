import MySQLdb.cursors
import hashlib
from random import randrange
from datetime import datetime

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
    cur.execute("SELECT MODULE_ID, NAME, BLURB, NUM_QUIZ_QUESTIONS FROM MODULES WHERE status = 'ACTIVE'")
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

def get_all_module_names():
    """ get list of module names to check against"""
    modules = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT NAME FROM MODULES")
    rows = cur.fetchall()
    for row in rows:
	modules.append(row['NAME'].lower())
    conn.close()
    return modules

def get_admin_module_info():
    """ get module information for administrators """
    modules = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vw_ADMIN_MODULE_INFO ORDER BY STATUS ASC, MODULE_ID ASC")
    rows = cur.fetchall()
    for row in rows:
	row['LAST_UPDATED'] = row['LAST_UPDATED'].strftime('%d-%m-%Y')
	modules.append(row)
    conn.close()
    return modules

def get_module_edit_info(id):
    """ get module name and blurb to display in profile edit module """

    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT NAME, BLURB FROM vw_ADMIN_MODULE_INFO WHERE MODULE_ID = %s", [id]);
    info = cur.fetchone()
    return info

def add_new_module_profile(name, blurb, username):
    conn = do_mysql_connect()
    cur = conn.cursor()
    try:
	cur.execute("INSERT INTO MODULES (NAME, BLURB) VALUES (%s, %s)", 
		[name, blurb])
	conn.commit()
	mid = get_module_id_from_name(name)
	add_new_module_content(mid, username)
	return 0
    except MySQLdb.Error as e:
	conn.rollback()
    conn.close()

def add_new_module_content(mid, username):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO MODULE_CONTENT (MODULE_ID, REVISION, EDITOR) VALUES (%s, %s, %s)", 
	    [mid, 0, username])
    conn.commit()

def edit_module_profile(mid, name, blurb):
    conn = do_mysql_connect()
    cur = conn.cursor()
    try:
	cur.execute("UPDATE MODULES SET NAME = %s, BLURB = %s WHERE MODULE_ID = %s", 
		[name, blurb, mid])
	conn.commit()
	return 0
    except MySQLdb.Error as e:
	conn.rollback()
    return e
    conn.close()

def get_module_status(mid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT STATUS FROM MODULES WHERE MODULE_ID = %s", [mid])
    row = cur.fetchone()
    conn.close()
    return row['STATUS']

def toggle_module_status(mid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    status = get_module_status(mid)
    try:
	if status == 'ACTIVE':
	    cur.execute("UPDATE MODULES SET STATUS = %s WHERE MODULE_ID = %s", ["INACTIVE", mid])
	else:
	    cur.execute("UPDATE MODULES SET STATUS = %s WHERE MODULE_ID = %s", ["ACTIVE", mid])
	conn.commit()
	return 0
    except MySQLdb.Error as e:
	conn.rollback()
    return e
    conn.close()

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

def get_questions_answered_by_user(uid):
    """ get number of questions answered by user """
    number_of_answers = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(QUESTION_ID) AS QUESTIONS_ANSWERED FROM GRADEBOOK WHERE USER_ID = %s AND QUESTION_TYPE = %s", [uid, "QUIZ"])
    rows = cur.fetchall()
    for row in rows:
        number_of_answers.append(row['QUESTIONS_ANSWERED'])
    conn.close()
    return number_of_answers

def get_correct_answers():
    """ get list of correct answers """
    answers = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUIZ_CORRECT")
    rows = cur.fetchall()
    for row in rows:
	answers.append(row['ANSWER_ID'])
    conn.close()
    return answers

def get_quiz_answers_by_user(uid):
    """ get list of correct answers """
    answers = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM GRADEBOOK WHERE USER_ID = %s AND QUESTION_TYPE = %s", [uid, "QUIZ"])
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
    cur.execute("SELECT DISTINCT A.MODULE_ID FROM MODULES M,(SELECT MODULE_ID,COUNT(MODULE_ID) AS COUNT FROM vw_USER_QUIZ_ANSWERS WHERE USER_ID = %s GROUP BY MODULE_ID) AS A WHERE COUNT = M.NUM_QUIZ_QUESTIONS", [user_id])
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

def get_int_questions_by_module(module_id):
    """ get list of interactive questions per module """
    int_questions_by_module = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM INTERACTIVE_QUESTIONS WHERE MODULE_ID = %s", [module_id])
    rows = cur.fetchall()
    for row in rows:
	int_questions_by_module.append(row)
    conn.close()
    return int_questions_by_module
    
def get_int_answers():
    """ get list of all answers to interactive questions"""
    int_answers = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    # modify this to only get answers for one module's questions
    cur.execute("SELECT * FROM INTERACTIVE_ANSWERS")
    rows = cur.fetchall()
    for row in rows:
	int_answers.append(row)
    conn.close()
    return int_answers

def get_int_correct_answers():
    """ get list of all correct answers to interactive questions"""
    correct_answers = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    # modify this to only get answers for one module's questions
    cur.execute("SELECT * FROM INTERACTIVE_CORRECT")
    rows = cur.fetchall()
    for row in rows:
	correct_answers.append(row)
    conn.close()
    return correct_answers

def get_number_of_correct_answers(user_id, module_title):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(QUESTION_ID) AS QUESTIONS_CORRECT FROM vw_USER_QUIZ_CORRECT WHERE USER_ID = %s AND MODULE_ID IN (SELECT MODULE_ID FROM MODULES WHERE NAME = %s) GROUP BY USER_ID, MODULE_ID", [user_id, module_title])
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
    cur.execute("Select MODULE_ID, NUM_QUIZ_QUESTIONS FROM MODULES WHERE STATUS = 'ACTIVE' AND NAME = %s", [module_title])
    rows = cur.fetchall()
    for row in rows:
	number_of_questions = row['NUM_QUIZ_QUESTIONS']
    conn.close()
    return number_of_questions

def check_quiz_answer_exists(uid, qid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("Select * FROM GRADEBOOK WHERE USER_ID = %s AND QUESTION_ID = %s AND QUESTION_TYPE = %s",
	    [uid, qid, "QUIZ"])
    if cur.rowcount == 1:
	return True
    return False

def check_quiz_answer_valid(qid, aid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("Select * FROM QUIZ_ANSWERS WHERE QUESTION_ID = %s AND ANSWER_ID = %s",
	    [qid, aid])
    if cur.rowcount == 1:
	return True
    return False

def add_answer_to_gradebook(uid, orgunit, qid, aid, question_type):
    conn = do_mysql_connect()
    cur = conn.cursor()
    try:
	cur.execute("INSERT INTO GRADEBOOK (USER_ID, ORG_UNIT, QUESTION_TYPE, QUESTION_ID, ANSWER_ID) VALUES (%s, %s, %s, %s, %s)", 
		[uid, orgunit, question_type, qid, aid])
	conn.commit()
	return 0
    except MySQLdb.Error as e:
	conn.rollback()
    conn.close()

def check_quiz_answer_correct(aid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("Select * FROM QUIZ_CORRECT WHERE ANSWER_ID = %s", [aid])
    if cur.rowcount == 1:
	return True
    return False

def log_user_quiz_answer(uid, dn, qid, aid, question_type):
    if not check_quiz_answer_exists(uid, qid):
	if check_quiz_answer_valid(qid, aid):
	    orgunit = dn[0].split(",")[1][3:]
	    add_answer_to_gradebook(uid, orgunit, qid, aid, question_type)
	    if check_quiz_answer_correct(aid):
		return 0
	    return 1
    return -1

def check_int_answer_exists(uid, qid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("Select * FROM GRADEBOOK WHERE USER_ID = %s AND QUESTION_ID = %s AND QUESTION_TYPE = %s",
	    [uid, qid, "INTERACTIVE"])
    if cur.rowcount == 1:
	return True
    return False

def check_int_answer_correct(aid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("Select * FROM INTERACTIVE_CORRECT WHERE INT_ANS_ID = %s", [aid])
    if cur.rowcount == 1:
	return True
    return False

def get_correct_msg(qid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM INTERACTIVE_QUESTIONS WHERE INT_Q_ID = %s", [qid])
    row = cur.fetchone()
    conn.close()
    return row['CORRECT_MESSAGE']

def get_incorrect_msg(qid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM INTERACTIVE_QUESTIONS WHERE INT_Q_ID = %s", [qid])
    row = cur.fetchone()
    conn.close()
    return row['INCORRECT_MESSAGE']

def delete_quiz_question(qid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM QUIZ_CORRECT WHERE QUESTION_ID = %s", [qid])
    cur.execute("DELETE FROM QUIZ_ANSWERS WHERE QUESTION_ID = %s", [qid])
    cur.execute("DELETE FROM QUIZ_QUESTIONS WHERE QUESTION_ID = %s", [qid])
    conn.close()
    return 0

def delete_int_question(qid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM INTERACTIVE_CORRECT WHERE INT_Q_ID = %s", [qid])
    cur.execute("DELETE FROM INTERACTIVE_ANSWERS WHERE INT_Q_ID = %s", [qid])
    cur.execute("DELETE FROM INTERACTIVE_QUESTIONS WHERE INT_Q_ID = %s", [qid])
    conn.close()
    return 0

def log_user_int_answer(uid, dn, qid, aid, question_type):
    if not check_int_answer_exists(uid, qid):
	orgunit = dn[0].split(",")[1][3:]
	add_answer_to_gradebook(uid, orgunit, qid, aid, question_type)
	correct = get_correct_msg(qid)
	incorrect = get_incorrect_msg(qid)
	if check_int_answer_correct(aid):
	    return [0, correct]
	return [1, incorrect]
    return [-1, "You have already answered this question."]

def check_module_started(username, mid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("Select * FROM USER_PROGRESS WHERE USER_ID = %s AND MODULE_ID = %s", [username, mid])
    if cur.rowcount == 1:
	return True
    return False

def get_last_viewed_slide(username, mid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT LAST_VIEWED FROM USER_PROGRESS WHERE USER_ID = %s AND MODULE_ID = %s", [username, mid])
    row = cur.fetchone()
    conn.close()
    return row['LAST_VIEWED']
    pass

def log_user_progress(username, mid, slide):
    conn = do_mysql_connect()
    cur = conn.cursor()
    if check_module_started(username, mid):
	last = get_last_viewed_slide(username, mid)
	if slide == (last + 1):
	    cur.execute("UPDATE USER_PROGRESS SET LAST_VIEWED = %s WHERE MODULE_ID = %s AND USER_ID = %s", [slide, mid, username])
    else:
	cur.execute("INSERT INTO USER_PROGRESS (LAST_VIEWED, MODULE_ID, USER_ID) VALUES (%s, %s, %s)", [slide, mid, username])
    conn.commit()
    conn.close()

# QUERIES FOR GETTING INFORMATION ABOUT ADMIN-RELATED THINGS
def get_admin_user_list():
    """ get list of administrators """
    admin = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT user_id,name,unit_ID FROM ADMIN")
    for row in cur.fetchall():
	admin.append(row)
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
    sql = "SELECT * FROM vw_USER_QUIZ_ANSWERS"
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

def get_all_read_perms():
    """ get all read admin permissions  """
    read_perms = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT User_ID FROM ADMIN_PERM WHERE PERMISSION='read'")

    for row in cur.fetchall():
	read_perms.append(row['User_ID'])

    conn.close()
    return read_perms

def get_all_write_perms():
    """ get all write admin permissions  """
    write_perms = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT User_ID FROM ADMIN_PERM WHERE PERMISSION = 'write'")

    for row in cur.fetchall():
        write_perms.append(row['User_ID'])

    conn.close()
    return write_perms



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

def update_quiz_answer_value(aid, new_value):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("UPDATE QUIZ_ANSWERS SET ANSWER = %s WHERE ANSWER_ID = %s", 
	    [new_value, aid])
    conn.commit()
    conn.close()
    return 0

def update_quiz_question_value(qid, new_value):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("UPDATE QUIZ_QUESTIONS SET QUESTION = %s WHERE QUESTION_ID = %s", 
	    [new_value, qid])
    conn.commit()
    conn.close()
    return 0

def update_int_question_value(qid, new_value):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("UPDATE INTERACTIVE_QUESTIONS SET QUESTION = %s WHERE INT_Q_ID = %s", 
	    [new_value, qid])
    conn.commit()
    conn.close()
    return 0

def update_int_answer_value(aid, new_value):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("UPDATE INTERACTIVE_ANSWERS SET ANSWER = %s WHERE INT_ANS_ID = %s", 
	    [new_value, aid])
    conn.commit()
    conn.close()
    return 0

def update_int_correct_value(qid, new_value):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("UPDATE INTERACTIVE_QUESTIONS SET CORRECT_MESSAGE = %s WHERE INT_Q_ID = %s", 
	    [new_value, qid])
    conn.commit()
    conn.close()
    return 0

def update_int_incorrect_value(qid, new_value):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("UPDATE INTERACTIVE_QUESTIONS SET INCORRECT_MESSAGE = %s WHERE INT_Q_ID = %s", 
	    [new_value, qid])
    conn.commit()
    conn.close()
    return 0

def update_max_q_num(mid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("UPDATE MODULES SET NUM_QUIZ_QUESTIONS = NUM_QUIZ_QUESTIONS + 1 WHERE MODULE_ID = %s", 
	    [mid])
    conn.commit()
    conn.close()
    return 0

def add_new_question(mid, new_question):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (%s, %s)", 
	    [mid, new_question])
    new_q_id = cur.lastrowid
    conn.commit()
    conn.close()
    update_max_q_num(mid)
    return new_q_id

def add_new_answer(qid, new_answer):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (%s, %s)", 
	    [qid, new_answer])
    new_ans_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_ans_id

def add_new_correct_answer(qid, aid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    # put some checks in m8
    cur.execute("INSERT INTO QUIZ_CORRECT (QUESTION_ID, ANSWER_ID) VALUES (%s, %s)", 
	    [qid, aid])
    new_ans_id = cur.lastrowid
    conn.commit()
    conn.close()
    return 0

def update_max_i_num(mid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("UPDATE MODULES SET NUM_INT_QUESTIONS = NUM_INT_QUESTIONS + 1 WHERE MODULE_ID = %s", 
	    [mid])
    conn.commit()
    conn.close()
    return 0

def add_new_int_question(mid, new_question, img_link, correct_msg, incorrect_msg):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO INTERACTIVE_QUESTIONS (MODULE_ID, QUESTION, MEDIA_LINK, MEDIA_TYPE, CORRECT_MESSAGE, INCORRECT_MESSAGE) VALUES (%s, %s, %s, %s, %s, %s)", 
	    [mid, new_question, img_link, "IMG", correct_msg, incorrect_msg])
    new_q_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_q_id

def add_new_int_answer(qid, new_answer):
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO INTERACTIVE_ANSWERS (INT_Q_ID, ANSWER) VALUES (%s, %s)", 
	    [qid, new_answer])
    new_ans_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_ans_id

def add_new_correct_int_answer(qid, aid):
    conn = do_mysql_connect()
    cur = conn.cursor()
    # put some checks in m8
    cur.execute("INSERT INTO INTERACTIVE_CORRECT (INT_Q_ID, INT_ANS_ID) VALUES (%s, %s)", 
	    [qid, aid])
    new_ans_id = cur.lastrowid
    conn.commit()
    conn.close()
    return 0

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

# DATABASE CONNECTION

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
