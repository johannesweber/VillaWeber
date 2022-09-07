from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def service():
    return 'Service is running'

@app.route("/villaweber/dashboard", methods=['GET'])
def main():
    return render_template("base.html")
