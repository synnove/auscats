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
    g.appname = "AusCERT Security Training"

# USER PAGES
@app.route("/")
def default_page():
    """ Main page (equivalent of index.html).
	Admin users redirect to administrator dashboard.
	Regular users redirect to list of modules."""

    if g.username in g.admins:
	return redirect(url_for('admin_dashboard'))
    return redirect(url_for('user_module_list'))

@app.route("/modules")
def user_module_list():
    """ Default user page: displays list of modules in progress,
	completed, or scheduled. """

    active_modules = db.get_module_info()
    modules_completed = db.modules_completed_by_user(g.username)
    modules_started = db.get_modules_started_by_user(g.username)
    last_viewed_slide = db.get_last_viewed_slide_by_user(g.username)
    modules_in_progress = list(set(modules_started)-set(modules_completed))
    num_active_modules = len(active_modules)
    num_complete = len(modules_completed)
    num_started = len(modules_started)
    num_in_progress = len(modules_in_progress)
    num_scheduled = num_active_modules - num_complete - num_in_progress
        
    if g.username not in g.admins:
	return render_template('user_module_list.html', 
		pagetitle = g.appname + " - My Modules",
		subtitle = "My Modules", 
		user_id = g.username, name = g.user,
		active_modules = active_modules, 
		modules_completed = modules_completed,
		modules_started = modules_started,
		modules_in_progress = modules_in_progress,
		num_active_modules = num_active_modules,
                num_complete = num_complete,
		num_started = num_started,
		num_in_progress = num_in_progress,
		num_scheduled = num_scheduled,
		last_viewed_slide = last_viewed_slide, is_admin = False)
    return redirect(url_for('admin_dashboard'))

@app.route("/module/<module_title>", methods=['GET', 'POST'])
def user_module_slideshow(module_title):
    """ Displays a module to the user. Currently content is stored in .txt
	files and parsed, will eventually shift to using database. """
    modules_list = db.get_module_names()

    # check url is valid
    if module_title.lower() not in modules_list:
	flash("Invalid module title.", "invalid")
	return redirect(url_for('user_module_list'))

    # get module content
    lecture_file = module_title.lower().replace(" ", "_") + ".txt"
    slides = parse_lecture_content(lecture_file)
    module_id = db.get_module_id_from_name(module_title)
    quizzes = db.get_quiz_questions_by_module(module_id)
    answers = db.get_quiz_answers()
    
    if g.username not in g.admins:
	return render_template('user_module.html', 
		module_id = module_id,
		pagetitle = g.appname + " - " + module_title,
		subtitle = "Module: " + module_title, 
		name = g.user,
		module_title = module_title, slides = slides,
		quizzes = quizzes, answers = answers, 
		is_admin = False)
    return redirect(url_for('admin_dashboard'))

@app.route("/review/<module_title>", methods=['GET', 'POST'])
def user_module_review(module_title):
    """ Displays a module to the user. Currently content is stored in .txt
	files and parsed, will eventually shift to using database. """
    modules_list = db.get_module_names()

    # check url is valid
    if module_title.lower() not in modules_list:
	flash("Invalid module title.", "invalid")
	return redirect(url_for('user_module_list'))

    # get module content
    lecture_file = module_title.lower().replace(" ", "_") + ".txt"
    slides = parse_lecture_content(lecture_file)
    module_id = db.get_module_id_from_name(module_title)
    
    if g.username not in g.admins:
	return render_template('user_module_review.html', name = g.user, 
		slides = slides, subtitle = "Review: " + module_title,
		is_admin = False)
    return redirect(url_for('admin_dashboard'))

@app.route("/gradebook", methods=['GET', 'POST'])
def user_grade_list():
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
	return render_template('user_gradebook.html', 
		pagetitle = g.appname + " - My Grades",
		subtitle = "My Grades", 
		name = g.user,
		completed_modules = completed_modules,
		is_admin = False)
    return redirect(url_for('admin_dashboard'))

@app.route("/grades/<module_title>", methods=['GET', 'POST'])
def user_grade_details(module_title):
    """ displays grades to the user by the requested module. """
    modules_list = db.get_module_names()

    # check url is valid
    if module_title.lower() not in modules_list:
	flash("Invalid module title.", "invalid")
	return redirect(url_for('user_module_list'))

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
    return redirect(url_for('admin_dashboard'))

@app.route("/check_answer", methods=['GET', 'POST'])
def check_answer():
    """ checks the user's answer """
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    qid = request.args.get('qid', -1, type=int)
    aid = request.args.get('aid', -1, type=int)
    result = db.log_user_answer(g.username, user_info['dn'], qid, aid)
    return jsonify(result=result)

@app.route("/update_user_progress", methods=['GET', 'POST'])
def update_progress():
    """ checks the user's answer """
    name = request.args.get('name', -1, type=unicode)
    slide = request.args.get('slide', -1, type=int)
    mid = db.get_module_id_from_name(name)    
    result = db.log_user_progress(g.username, mid, slide)
    return jsonify(result=result)

# ADMIN PAGES
@app.route("/dashboard")
def admin_dashboard():
    """ main admin user page """

    modules = db.get_module_info()
    org_units = db.get_org_unit_info()
    last_updated = db.get_last_updated_module()

    if g.username in g.admins:
	return render_template('admin_dashboard.html', 
		pagetitle = g.appname + " - My Dashboard",
		subtitle = "Administrator Dashboard", 
		name = g.user,
		modules = modules,
		last_updated = last_updated,
		org_units = org_units, 
		is_admin = True)
    return render_template('unauthorized.html', name=g.user, 
	    subtitle = "Not Authorized", is_admin = False)

@app.route("/admin")
def admin_manage_users():
    """ add, modify and remove admin users """

    if g.username in g.admins:
	return render_template('admin_manage.html', 
		pagetitle = g.appname + " - Manage Administrators",
		subtitle = "Manage Administrators", 
		name = g.user, 
		is_admin = True)
    return render_template('unauthorized.html', name=g.user,
	    subtitle = "Not Authorized", is_admin = False)

@app.route("/get_module_edit_info", methods=['GET', 'POST'])
def module_edit_info():
    """ returns module info to be edited """
    mid = request.args.get('mid', -1, type=int)
    results = db.get_module_edit_info(mid)
    return jsonify(blurb=results['BLURB'], name=results['NAME'])

@app.route("/edit_module_profile", methods=['GET', 'POST'])
def admin_edit_module_profile():
    """ returns module info to be edited """
    mid = request.args.get('mid', -1, type=int)
    name = request.args.get('name', -1, type=unicode)
    blurb = request.args.get('blurb', -1, type=unicode)
    result = db.edit_module_profile(mid, name, blurb)
    return jsonify(result=result)

@app.route("/add_module_profile", methods=['GET', 'POST'])
def admin_add_new_module():
    """ returns module info to be edited """
    name = request.args.get('name', -1, type=unicode)
    blurb = request.args.get('blurb', -1, type=unicode)
    result = db.add_new_module_profile(name, blurb, g.username)
    return jsonify(result=result)

@app.route("/change_module_status", methods=['GET', 'POST'])
def admin_change_module_status():
    """ returns module info to be edited """
    mid = request.args.get('mid', -1, type=int)
    result = db.toggle_module_status(mid)
    return jsonify(result=result)

@app.route('/module-manager')
def admin_list_courses(act=None, module_title=None):
    """ lists modules that administrators can edit """

    if g.username in g.admins:
	    modules = db.get_admin_module_info()
	    return render_template('admin_edit.html', 
		    pagetitle = g.appname + " - Manage Modules",
		    subtitle = "Manage Modules", 
		    name = g.user, 
		    modules = modules,
		    is_admin = True)
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
    return redirect(url_for('admin_dashboard'))

@app.route("/admin_mod/<attrs>", methods=['GET', 'POST'])
def admin_mod(attrs):
    """ calls function that modifies admin permissions """
    admin_perms = {}
    attrs = attrs.split("&")
    for item in attrs:
	info = item.split("=")
	admin_perms[info[0]] = info[1]
    parse_admin_mod_directive(admin_perms)
    return redirect(url_for('admin_dashboard'))

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
		return redirect(url_for('admin_dashboard'))
	    elif status == 0:
		flash("Administrator successfully added.", "admin_ok")
		return redirect(url_for('admin_dashboard'))
	elif action == "modify":
	    pass
	    # call other function
	elif action == "delete":
	    pass
	    # call delete function
    thing = str(action) + " " + str(admin_id)
    return redirect(url_for('admin_dashboard'))

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
		return redirect(url_for('admin_dashboard'))
    return 0

# DO NOT TOUCH THIS SECTION DO NOT DO IT I WILL KNOW AND I WILL SMACK YOU
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)
