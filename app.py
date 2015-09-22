from flask import Flask
from flask import render_template, request, redirect, send_file, url_for, g
from flask import make_response, flash, jsonify
import csv
import io
import json
import queries as db

app = Flask(__name__)

app.secret_key = 'supersupersecret'

@app.before_request
def load_user():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    g.username = user_info['user']
    g.user = user_info['name'].split(" ")[0]
    g.admins = db.get_admin_user_list()

# USER PAGES
@app.route("/")
def frontPage():
    """ Main page (equivalent of index.html).
	Admin users redirect to administrator dashboard.
	Regular users redirect to list of modules."""

    if g.username in g.admins:
	return redirect(url_for('adminDashboard'))
    return redirect(url_for('courseDefault'))

@app.route("/modules")
def courseDefault():
    """ Default user page: displays list of modules either in progress or
	completed. """

    active_modules = db.get_module_info()
    modules_completed = db.modules_completed_by_user(g.username)
    num_active_modules = len(active_modules)
    num_incomplete = len(active_modules) - len(modules_completed)
    num_complete = len(modules_completed)
    
    if g.username not in g.admins:
	return render_template('user_module_list.html', name=g.user,
		subtitle="My Modules", user_id = g.username, 
		active_modules = active_modules, 
		modules_completed = modules_completed, 
		num_incomplete = num_incomplete,
		num_complete = num_complete, 
		num_active_modules = num_active_modules,  is_admin = False)
    return redirect(url_for('adminDashboard'))

@app.route("/module/<module_title>", methods=['GET', 'POST'])
def coursePage(module_title):
    """ Displays a module to the user. Currently content is stored in .txt
	files and parsed, will eventually shift to using database. """
    modules_list = db.get_module_names()

    # check url is valid
    if module_title.lower() not in modules_list:
	flash("Invalid module title.", "invalid")
	return redirect(url_for('courseDefault'))

    # get module content
    lecture_file = module_title.lower().replace(" ", "_") + ".txt"
    slides = parse_lecture_content(lecture_file)
    module_id = db.get_module_id_from_name(module_title)
    quizzes = db.get_quiz_questions_by_module(module_id)
    answers = db.get_quiz_answers()
    
    if g.username not in g.admins:
	return render_template('user_module.html', name = g.user, 
		subtitle = "Module: " + module_title, slides = slides, 
		module_title = module_title, quizzes = quizzes, 
		answers = answers, is_admin = False)
    return redirect(url_for('adminDashboard'))

@app.route("/review/<module_title>", methods=['GET', 'POST'])
def reviewModule(module_title):
    """ Displays a module to the user. Currently content is stored in .txt
	files and parsed, will eventually shift to using database. """
    modules_list = db.get_module_names()

    # check url is valid
    if module_title.lower() not in modules_list:
	flash("Invalid module title.", "invalid")
	return redirect(url_for('courseDefault'))

    # get module content
    lecture_file = module_title.lower().replace(" ", "_") + ".txt"
    slides = parse_lecture_content(lecture_file)
    
    if g.username not in g.admins:
	return render_template('user_module_review.html', name = g.user, 
		slides = slides, subtitle = "Review: " + module_title,
		is_admin = False)
    return redirect(url_for('adminDashboard'))

@app.route("/gradebook", methods=['GET', 'POST'])
def gradeList():
    """ displays grades to the user by the requested module. """

    modules = db.get_module_info()
    grades = completed_module_ids = db.modules_completed_by_user(g.username)
    completed_modules = []
    for module in modules:
	if module['MODULE_ID'] in completed_module_ids:
	    number_of_questions = db.get_total_number_of_questions(module['NAME'])
	    correct_answers = db.get_number_of_correct_answers(g.username, module['NAME'])
	    module['GRADE'] = int(correct_answers / float(number_of_questions) * 100)
	    completed_modules.append(module)
    if g.username not in g.admins:
        return render_template('user_gradebook.html', name = g.user, 
		subtitle = "My Grades", completed_modules = completed_modules,
		is_admin = False)
    return redirect(url_for('adminDashboard'))

@app.route("/grades/<module_title>", methods=['GET', 'POST'])
def gradePage(module_title):
    """ displays grades to the user by the requested module. """
    modules_list = db.get_module_names()

    # check url is valid
    if module_title.lower() not in modules_list:
	flash("Invalid module title.", "invalid")
	return redirect(url_for('courseDefault'))

    modules = db.get_module_info()
    num_correct_answers = db.get_number_of_correct_answers(g.username, module_title)
    number_of_questions = db.get_total_number_of_questions(module_title)
    module_id = db.get_module_id_from_name(module_title)    
    quizzes = db.get_quiz_questions_by_module(module_id)
    answers = db.get_quiz_answers()
    correct_answers = db.get_correct_answers()
    user_answers= db.get_answers_by_user(g.username)
    stats = db.get_question_statistics()
    for quiz in quizzes:
	for stat in stats:
	    if stat['QUESTION_ID'] == quiz['QUESTION_ID']:
		if ("SUCCESS" not in quiz or quiz['SUCCESS'] == 0):
		    quiz['SUCCESS'] = int(stat['PERCENT_SUCCESS'])
	    else:
		if ("SUCCESS" not in quiz):
		    quiz['SUCCESS'] = 0

    try:
	percentage_correct = int((num_correct_answers /float( number_of_questions)) * 100)
    except ZeroDivisionError:
	percentage_correct = 0

    if g.username not in g.admins:
        return render_template('user_grades.html', name = g.user, 
		subtitle = "My Grades: " + module_title,
		correct_answers = correct_answers, user_answers = user_answers,
		num_correct_answers = num_correct_answers,
                number_of_questions = number_of_questions, 
		percentage_correct = percentage_correct,
		quizzes = quizzes, answers = answers, 
		module_title = module_title, modules = modules, is_admin = False)
    return redirect(url_for('adminDashboard'))

@app.route("/check_answer", methods=['GET', 'POST'])
def check_answer():
    """ checks the user's answer """
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    qid = request.args.get('qid', -1, type=int)
    aid = request.args.get('aid', -1, type=int)
    result = db.log_user_answer(g.username, user_info['dn'], qid, aid)
    return jsonify(result=result)

# ADMIN PAGES
@app.route("/dashboard")
def adminDashboard():
    """ main admin user page """

    modules = db.get_module_info()
    org_units = db.get_org_unit_info()
    last_updated = db.get_last_updated_module()

    if g.username in g.admins:
	return render_template('admin_dashboard.html', subtitle="Administrator Dashboard",
		name = g.user, modules = modules,
		last_updated = last_updated, org_units = org_units, 
		is_admin = True)
    return render_template('unauthorized.html', name=g.user, 
	    subtitle = "Not Authorized", is_admin = False)

@app.route("/admin")
def manageAdmin():
    """ add, modify and remove admin users """

    if g.username in g.admins:
	return render_template('admin_dashboard.html', name = g.user,
		subtitle = "Manage Administrators",
		is_admin = True)
    return render_template('unauthorized.html', name=g.user, 
	    subtitle = "Not Authorized", is_admin = False)

@app.route("/drawingboard/<course_id>/<rev_id>/<slide_no>")
def editCourse():
    """ page for modifying module content """

    if g.username in g.admins:
	return render_template('admin_dashboard.html', name = g.user,
		subtitle = "Edit a Module",
		is_admin = True)
    return render_template('unauthorized.html', name=g.user, 
	    subtitle = "Not Authorized", is_admin = False)

@app.route("/edit")
def editCourseList():
    """ lists modules that administrators can edit """

    active_modules = db.get_admin_module_info("ACTIVE")
    inactive_modules = db.get_admin_module_info("INACTIVE")

    if g.username in g.admins:
	return render_template('admin_edit.html', name = g.user,
		active_modules = active_modules, subtitle = "Manage Courses",
		inactive_modules = inactive_modules, is_admin = True)
    return render_template('unauthorized.html', name=g.user, 
	    subtitle = "Not Authorized", is_admin = False)

@app.route("/download/<filters>", methods=['GET', 'POST'])
def download_csv(filters):
    """ retrieves a .csv file to download """
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
    return redirect(url_for('adminDashboard'))

@app.route("/admin_mod/<attrs>", methods=['GET', 'POST'])
def admin_mod(attrs):
    """ calls function that modifies admin permissions """
    admin_perms = {}
    attrs = attrs.split("&")
    for item in attrs:
	info = item.split("=")
	admin_perms[info[0]] = info[1]
    parse_admin_mod_directive(admin_perms)
    return redirect(url_for('adminDashboard'))

# MISCELLANEOUS HELPER FUNCTIONS

def parse_lecture_content(filename):
    """ reads a text file to get lecture content """
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
    """ creates a .csv file from data """
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
    """ determines action to take (add, modify or remove admin) """
    action = admin_perms.pop("action", None)
    admin_id = admin_perms.pop("user", None)
    if action != None and admin_id != None:
	if action == "add":
	    status = add_administrator(admin_id, admin_perms)
	    if status == -1:
		flash("Administrator already exists.", "admin")
		return redirect(url_for('adminDashboard'))
	    elif status == 0:
		flash("Administrator successfully added.", "admin_ok")
		return redirect(url_for('adminDashboard'))
	elif action == "modify":
	    pass
	    # call other function
	elif action == "delete":
	    pass
	    # call delete function
    thing = str(action) + " " + str(admin_id)
    return redirect(url_for('adminDashboard'))

def add_administrator(admin_id, admin_perms):
    """ adds an administrator with the specified permissions """
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
		return redirect(url_for('adminDashboard'))
    return 0

# DO NOT TOUCH THIS SECTION DO NOT DO IT I WILL KNOW AND I WILL SMACK YOU
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)
