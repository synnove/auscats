import MySQLdb.cursors
import hashlib

db = None

def get_course_info():
    courses = list()
    db = do_mysql_connect()
    cur = db.cursor()
    cur.execute("SELECT * FROM COURSES")
    for row in cur.fetchall():
	courses.append(row)
    return courses

def read_mysql_password():
    f = open('mysql.passwd', 'r')
    passwd = f.read()
    f.close()
    return passwd.rstrip()

def do_mysql_connect():
    global db
    if db == None:
	db = MySQLdb.connect(db='auscats', host='localhost', port=3306, 
		user='root', passwd=read_mysql_password(), 
		cursorclass=MySQLdb.cursors.DictCursor)
    return db
