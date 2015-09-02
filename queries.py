import MySQLdb.cursors
import hashlib

def get_course_info():
    courses = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM MODULES")
    for row in cur.fetchall():
	courses.append(row)
    conn.close()
    return courses

def get_admin_user_list():
    admin = list()
    conn = do_mysql_connect()
    cur = conn.cursor()
    cur.execute("SELECT userid FROM ADMIN")
    for row in cur.fetchall():
	admin.append(row['userid'])
    conn.close()
    return admin

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
