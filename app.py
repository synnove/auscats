from flask import Flask
from flask import render_template, request, redirect, send_file
import io

app = Flask(__name__)

app.secret_key = ''

@app.route("/")
def frontpage():
    return render_template('index.html')


# DO NOT TOUCH THIS SECTION DO NOT DO IT I WILL KNOW AND I WILL SMACK YOU
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
