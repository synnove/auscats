import MySQLdb.cursors
import hashlib

db = None

def read_mysql_password():
    f = open('mysql.passwd', 'r')
    passwd = f.read()
    f.close()
    return passwd.rstrip()

def do_mysql_connect():
    global db
    if db == None:
    db = MySQLdb.connect(db='dbname', host='localhost', port=3306, 
	    user='root', passwd=read_mysql_password(), 
	    cursorclass=MySQLdb.cursors.DictCursor)
    return db
