from helper.excel_helper import ExcelHelper
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def service():
    return 'Service is running'

@app.route("/villaweber")
def main():
    return render_template("base.html")

@app.route("/test")
def test():
    helper = ExcelHelper()
    helper.read_excel('Komponenten')