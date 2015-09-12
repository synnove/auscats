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
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list()

    if user_info['user'] in admin_list:
	return redirect(url_for('dashboard'))
    return redirect(url_for('courseDefault'))

@app.route("/modules")
def courseDefault():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list()

    active_modules = db.get_active_modules()
    modules_completed = db.modules_completed_by_user(user_info['user'])
    
    if user_info['user'] not in admin_list:
	return render_template('user_module_list.html', name=user_info['name'],
		user_id = user_info['user'], 
		active_modules = active_modules, modules_completed = modules_completed,
		is_admin = False)
    return redirect(url_for('dashboard'))

@app.route("/module/<module_title>", methods=['GET', 'POST'])
def coursePage(module_title):
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list()

    slides = [
	    {"title": "Social Engineering",
		"quote": "Amateurs hack systems, professionals hack people",
		"cite": "someone"},
	    {"title": "Social engineering is..",
		"contents": ["The 'art' of utilizing human behaviour to breach security",
		"Without the participant (or victim) even realizing",
		"that they have been manipulated."]},
	    {"title": "Amateurs Hack Systems, Professionals Hack People",
		"contents": ["Social engineering is...", 
		"the 'art' of utilizing human behaviour to breach security",
		"without the participant (or victim) even realizing",
		"that they have been manipulated."]}
	    {"title":"A threat often overlooked..",
	     	"contents": ["but regularily exploited to take advantage",
		"of what is considered in the security chain of an organisation",
		"the 'human factor'"]}
	    {"title":"2 Main Types Social Engineering",
		"contents":["Technology-Based Approach: deceive the user",
		"into believing they are interacting with a 'real' computer system",
		"to extract personal information"]}
	    {"title": "Technology-Based Example",
		"contents":["The user gets a popup window, informing him that the",
		"computer application has had a problem and the user will need to",
		"reauthenticate in order to proceed. Once the user provides his",
		"id and password on that pop up window, the harm is done.",
		"The hacker now has the user id and password."]} 
	    {"title": "2 Main Types Of Social Engineering",
		"contents": ["Human Approach: takes advantage on the victims ignorance",
		"the natural human inclination to be helpful and liked"]}
	    {"title": "Human Based Example",
		"contents":["attacker impersonates a person with authority and  places",
		"a call to the help desk, and pretends to be a senior Manager",
		"they say that have forgotten their password and needs to get it reset",
		"The help desk person resets the password and gives the new password",
		"to the person waiting at the other end of the phone.",
		"the attacker now access the personnel systems as if they were the manager",]}
	    {"title":"The Cycle",
		"contents":["A common pattern associated with social engineering is known as",
		"'The Cycle'. The cycle has the following steps:",
		"Step 1) Information Gathering: aggressor gathers information about the target",
		"Step 2) Developing Relationship: aggressor develops trust with the victim",
		"Step 3) Exploitation: target is manipulated by trusted aggressor to revel",
		"information or perform an action",
		"Step 4) Execution: once the target has completed the task the cycle is complete",]}
	    {"title":"Types of Social Engineering Attacks",
		"contents":["The variation and extent of social engineering attacks are only",
		"limited by the creativity of the hacker.",
		"The more common methods are as follows.",]}
	    {"title":"Phishing",
		"contents":["The attempt to acquire sensitive information or to make",
		"somebody act in a desired way by acting as a trustworthy entity in an",
		"electronic communication medium. They are usually targeted at large groups of people",]}
	    {"title":"Dumpster Diving",
		"contents":["Sifting through the trash of private individuals",
		"or companies to find discarded items that include sensitive information that",
		"can be used to compromise a system or a specific user account",]}
	    {"title":"Shoulder Surfing",
		"contents":["Using direct observation techniques to get information, such as looking",
		"over someone shoulder at their screen or keyboard.",]}
	    {"title":"Reverse Social Engineering",
		"contents":["The attackers create a situation in which the victim requires help and",
		"then present themselves as someone the victim will consider someone who can both solve",
		"their problem and is allowed to receive privileged information.",]}
	    {"title":"Waterholing",
		"contents":["Describes a targeted attack where the attackers compromise a website that",
		"is likely to be of interest to the chosen victim. The attackers then wait at the",
		"waterhole for their victim.",]}
	    {"title":"Baiting",
		"contents":["An attack during which a malware-infected storage medium is left in a",
		"location where it is likely to be found by the targeted victims.",]}
	    {"title":"How to avoid social engineering schemes?",
		"contents":["1) Do not open any emails from untrusted sources. Be sure to contact",
		"a friend or family member in person or via phone if you ever receive an email",
		"message that seems unlike them in any way.",
		"2) Do not give offers from strangers the benefit of the doubt.",
		"If they seem too good to be true, they probably are.",
		"3) Lock your laptop whenever you are away from your workstation.",]}
	    {"title":"How to avoid social engineering schemes?"
		"contents":["4) Purchase anti-virus software. No solution can defend against every",
		"threat that seeks to jeopardize users information, but they can help protect against some.",
		"5) Read your company privacy policy to understand under what circumstances you can or",
		"should let a stranger into the building.",]}
]

    modules = db.get_module_info()
    quizzes = db.get_quiz_questions_by_module(module_title)
    answers = db.get_quiz_answers()
    
    if user_info['user'] not in admin_list:
	return render_template('user_module.html', name = user_info['name'], slides = slides,
		module_title = module_title, modules = modules, quizzes = quizzes, 
		answers = answers, is_admin = False)
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
