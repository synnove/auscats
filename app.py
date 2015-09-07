from flask import Flask
from flask import render_template, request, redirect, send_file, url_for, make_response
import csv
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

    active_modules = db.get_active_modules()
    gradebook = db.get_gradebook()
    
    if user_info['user'] in admin_list:
	return redirect(url_for('dashboard'))
    return render_template('user_module_list.html', name=user_info['name'],user_id = user_info['user'], 
	    active_modules = active_modules, gradebook = gradebook, is_admin = False)

@app.route("/modules")
def courseDefault():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list()

    modules = db.get_module_info()
    
    if user_info['user'] not in admin_list:
	return render_template('user_module_list.html', name=user_info['name'],
		modules = modules, is_admin = False)
    return redirect(url_for('dashboard'))

@app.route("/module/<module_title>", methods=['GET', 'POST'])
def coursePage(module_title):
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list()

    modules = db.get_module_info()
    quizes = db.get_quiz_questions()
    answers = db.get_quiz_answers()
    
    if user_info['user'] not in admin_list:
	return render_template('user_module.html', name = user_info['name'],
		module_title = module_title, modules = modules, quizes = quizes, answers = answers,  is_admin = False)
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
    # remember to parse filters and use them to modify query
    data = db.get_data_for_csv()
    csv = make_csv(data,["USER_ID","ORG_UNIT","MODULE_ID","QUESTION_ID","ANSWER_ID"])
    response = make_response(csv)
    response.headers["Content-Disposition"] = "attachment; filename=results.csv"
    return response
    
@app.route("/admin")
def admin():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list();

    if user_info['user'] in admin_list:
	return render_template('admin_dashboard.html', name = user_info['name'],
		is_admin = True)
    return render_template('unauthorized.html', name=user_info['name'],
	    is_admin = False)

@app.route("/edit/<course_id>/<rev_id>/<slide_no>")
def modcourse():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list();

    if user_info['user'] in admin_list:
	return render_template('admin_dashboard.html', name = user_info['name'],
		is_admin = True)
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


# DO NOT TOUCH THIS SECTION DO NOT DO IT I WILL KNOW AND I WILL SMACK YOU
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)
