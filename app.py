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

    modules = db.get_module_info()
    if user_info['user'] in admin_list:
	return redirect(url_for('dashboard'))
    return render_template('user_module_list.html', name=user_info['name'],
	    modules = modules, is_admin = False)

@app.route("/modules")
def courseDefault():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    admin_list = db.get_admin_user_list()

    modules = db.get_module_info()
    if user_info['user'] not in admin_list:
	return render_template('user_module_list.html', name=user_info['name'],
		modules = modules, is_admin = False)
    return redirect(url_for('dashboard'))

@app.route("/module/<module_id>", methods=['GET', 'POST'])
def coursePage(module_id):
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
	return render_template('user_module.html', name = user_info['name'],
		module_title = module_id, slides = slides, is_admin = False)
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
