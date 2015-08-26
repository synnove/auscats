from KV import KV
from flask import Flask
from flask import render_template, request, redirect, send_file, url_for
import io
import json
import queries as db

app = Flask(__name__)

app.secret_key = ''

# USER PAGES
@app.route("/")
def frontPage():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list()

    courses = db.get_course_info()
    if user_info['user'] in admin_list:
	return render_template('dashboard.html', name = user_info['name'], 
		is_admin = True)
    return render_template('course.html', name=user_info['name'],
	    courses = courses, is_admin = False)

# USER PAGES
@app.route("/courses")
def courseDefault():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list()

    courses = db.get_course_info()
    if user_info['user'] not in admin_list:
	return render_template('course.html', name=user_info['name'],
		courses = courses, is_admin = False)
    return redirect(url_for('dashboard'))

@app.route("/course/<courseid>", methods=['GET', 'POST'])
def coursePage(courseid):
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list()

    slides = [{'title' : 'Nova', 
	'contents' : ['Norwegian Forest Cat', '7 months old']}, 
	{'title' : 'Pretzel',
	    'contents' : ['Domestic Shorthair', '5 months old']},
	{'title' : 'Poppy',
	    'contents' : ['Ragdoll', '2 years old']},
	{'title' : 'Kitty',
	    'contents' : ['Turkish Van', '0 months old']} ]
    if user_info['user'] not in admin_list:
	return render_template('module.html', name = user_info['name'],
		coursetitle = courseid, slides = slides, is_admin = False)
    return redirect(url_for('dashboard'))

# ADMIN PAGES
@app.route("/dashboard")
def dashboard():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list();
    if user_info['user'] in admin_list:
	return render_template('dashboard.html', name = user_info['name'],
		is_admin = True)
    return render_template('unauthorized.html', name=user_info['name'], 
	    is_admin = False)

@app.route("/admin")
def admin():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list();
    if user_info['user'] in admin_list:
	return render_template('dashboard.html', name = user_info['name'],
		is_admin = True)
    return render_template('unauthorized.html', name=user_info['name'],
	    is_admin = False)

@app.route("/edit/<course_id>/<rev_id>/<slide_no>")
def modcourse():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list();
    if user_info['user'] in admin_list:
	return render_template('dashboard.html', name = user_info['name'],
		is_admin = True)
    return render_template('unauthorized.html', name=user_info['name'],
	    is_admin = False)

# DO NOT TOUCH THIS SECTION DO NOT DO IT I WILL KNOW AND I WILL SMACK YOU
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)
