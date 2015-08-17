from KV import KV
from flask import Flask
from flask import render_template, request, redirect, send_file
import io
import json
import queries as db

app = Flask(__name__)

app.secret_key = ''

@app.route("/")
def frontPage():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    return render_template('index.html', name=user_info['name'])

@app.route("/courses")
def courseDefault():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    courses = db.get_course_info()
    return render_template('course.html', name=user_info['name'],
	    courses = courses)

@app.route("/course/<courseid>", methods=['GET', 'POST'])
def coursePage(courseid):
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    slides = [{'title' : 'Nova', 
	'contents' : ['Norwegian Forest Cat', '7 months old']}, 
	{'title' : 'Pretzel',
	    'contents' : ['Domestic Shorthair', '5 months old']} ]
    return render_template('module.html', name = user_info['name'],
	    coursetitle = courseid, slides = slides)

@app.route("/project")
def login():
    pass

# DO NOT TOUCH THIS SECTION DO NOT DO IT I WILL KNOW AND I WILL SMACK YOU
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)
