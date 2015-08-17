from KV import KV
from flask import Flask
from flask import render_template, request, redirect, send_file
import io
import json

app = Flask(__name__)

app.secret_key = ''

@app.route("/")
def frontPage():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    return render_template('index.html', name=user_info['name'])

@app.route("/course")
def courseDefault():
    user_info = json.loads(request.headers.get('X-KVD-Payload'))
    lipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    courselist = [['Security', lipsum, 2, 5], 
	    ['All About Cats', lipsum, 1, 5],
	    ['How To Train Your Dragon', lipsum, 5, 5]]
    return render_template('course.html', courses = courselist, name=user_info['name'])

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
