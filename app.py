from flask import Flask
from flask import render_template, request, redirect, send_file, url_for
from flask import make_response, flash
import csv
import io
import json
import queries as db

app = Flask(__name__)

app.secret_key = 'supersupersecret'

# UNAUTHORIZED PAGE
@app.errorhandler(401)
def custom_401(error):
        return Response('You are not authorized to view this page', 401,
		{'WWWAuthenticate':'Basic realm="You are not an administrator"'})

# USER PAGES
@app.route("/")
def frontPage():
    """ Main page (equivalent of index.html).
	Admin users redirect to administrator dashboard.
	Regular users redirect to list of modules."""
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list()

    if user_info['user'] in admin_list:
	return redirect(url_for('dashboard'))
    return redirect(url_for('courseDefault'))

@app.route("/modules")
def courseDefault():
    """ Default user page: displays list of modules either in progress or
	completed. """
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list()

    active_modules = db.get_module_info()
    modules_completed = db.modules_completed_by_user(user_info['user'])
    
    if user_info['user'] not in admin_list:
	return render_template('user_module_list.html', name=user_info['name'],
		user_id = user_info['user'], 
		active_modules = active_modules, modules_completed = modules_completed,
		is_admin = False)
    return redirect(url_for('dashboard'))

@app.route("/module/<module_title>", methods=['GET', 'POST'])
def coursePage(module_title):
    """ Displays a module to the user. Currently module content is hard-coded
	but will be eventually stored within the database as plain text and
	then parsed."""
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list()
    modules_list = db.get_module_names()
    if module_title.lower() not in modules_list:
	flash("Invalid module title.", "invalid")
	return redirect(url_for('courseDefault'))

    slides = parse_lecture_content("lecture.txt")
    modules = db.get_module_info()
    quizzes = db.get_quiz_questions_by_module(module_title)
    answers = db.get_quiz_answers()
    
    if user_info['user'] not in admin_list:
	return render_template('user_module.html', name = user_info['name'], slides = slides,
		module_title = module_title, modules = modules, quizzes = quizzes, 
		answers = answers, is_admin = False)
    return redirect(url_for('dashboard'))

@app.route("/check_answer/<info>", methods=['GET', 'POST'])
def check_answer(attrs):
    admin_perms = {}
    attrs = attrs.split("&")
    for item in attrs:
	info = item.split("=")
	admin_perms[info[0]] = info[1]
    parse_admin_mod_directive(admin_perms)
    return redirect(url_for('dashboard'))

# ADMIN PAGES
@app.route("/dashboard")
def dashboard():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list()

    modules = db.get_module_info()
    org_units = db.get_org_unit_info()

    if user_info['user'] in admin_list:
	return render_template('admin_dashboard.html', 
		name = user_info['name'], modules = modules,
		org_units = org_units, is_admin = True)
    return render_template('unauthorized.html', name=user_info['name'], 
	    is_admin = False)

@app.route("/download/<filters>", methods=['GET', 'POST'])
def download_csv(filters):
    if filters == "nofilter":
	data = db.get_data_for_csv(0, "")
    else:
	query_filters = {}
	filters = filters.split("&")
	num_filters = len(filters)
	for condition in filters:
	    query_filter = condition.split("=")
	    query_filters[query_filter[0]] = query_filter[1]
	data = db.get_data_for_csv(num_filters, query_filters)
    if data != None:
	csv = make_csv(data,["USER_ID","ORG_UNIT","MODULE_ID","QUESTION_ID","ANSWER_ID"])
	response = make_response(csv)
	response.headers["Content-Disposition"] = "attachment; filename=results.csv"
	return response
    flash("No results for requested filters.", "search")
    return redirect(url_for('dashboard'))

@app.route("/admin_mod/<attrs>", methods=['GET', 'POST'])
def admin_mod(attrs):
    admin_perms = {}
    attrs = attrs.split("&")
    for item in attrs:
	info = item.split("=")
	admin_perms[info[0]] = info[1]
    parse_admin_mod_directive(admin_perms)
    return redirect(url_for('dashboard'))
    
@app.route("/admin")
def admin():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list();

    if user_info['user'] in admin_list:
	return render_template('admin_dashboard.html', name = user_info['name'],
		is_admin = True)
    return render_template('unauthorized.html', name=user_info['name'],
	    is_admin = False)

@app.route("/drawingboard/<course_id>/<rev_id>/<slide_no>")
def modcourse():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list();

    if user_info['user'] in admin_list:
	return render_template('admin_dashboard.html', name = user_info['name'],
		is_admin = True)
    return render_template('unauthorized.html', name=user_info['name'],
	    is_admin = False)

@app.route("/edit")
def mod_course_list():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list();

    modules = db.get_module_info()

    if user_info['user'] in admin_list:
	return render_template('admin_edit.html', name = user_info['name'],
		modules = modules, is_admin = True)
    return render_template('unauthorized.html', name=user_info['name'],
	    is_admin = False)

# MISCELLANEOUS HELPER FUNCTIONS

def parse_lecture_content(filename):
    lecture_file = open(filename,"r")
    contents = []                                                                                                                                                                            
    slide = {}
    content_type = ""
    for line in lecture_file:
	if not line.strip():
	    contents.append(slide)
	    slide = {}
	elif line.strip()[0] == "[":
	    parts = line.strip().split("]")
	    content_type = parts[0][1:]
	    if content_type == "contents":
		slide[content_type] = []
		slide[content_type].append(parts[1].strip())
	    else:
		slide[content_type] = parts[1].strip()
	else:
	    slide[content_type].append(line.strip())
    return contents

def make_csv(data, headers):
    data_list = []
    csv = ""

    data_list.append(",".join(headers))
    for row in data:
	curr_row = []
	for item in headers:
	    curr_row.append(str(row[item]))
	data_list.append(",".join(curr_row))
    for row in data_list:
	csv += row
	csv += "\n"
    return csv


def parse_admin_mod_directive(admin_perms):
    action = admin_perms.pop("action", None)
    admin_id = admin_perms.pop("user", None)
    if action != None and admin_id != None:
	if action == "add":
	    status = add_administrator(admin_id, admin_perms)
	    if status == -1:
		flash("Administrator already exists.", "admin")
		return redirect(url_for('dashboard'))
	    elif status == 0:
		flash("Administrator successfully added.", "admin_ok")
		return redirect(url_for('dashboard'))
	elif action == "modify":
	    pass
	    # call other function
	elif action == "delete":
	    pass
	    # call delete function
    thing = str(action) + " " + str(admin_id)
    return redirect(url_for('dashboard'))

def add_administrator(admin_id, admin_perms):
    status = db.do_admin_add(admin_id)
    if status == -1:
	return -1
    for perm_type in admin_perms:
	if admin_perms[perm_type] == "true":
	    perm_err = db.do_admin_add_perms(admin_id, perm_type)
	    if perm_err == -1:
		flash("Permission " + perm_type + 
			" already exists for administrator " + 
			admin_id + ".", "admin")
		return redirect(url_for('dashboard'))
    return 0


# DO NOT TOUCH THIS SECTION DO NOT DO IT I WILL KNOW AND I WILL SMACK YOU
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)
