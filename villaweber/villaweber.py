from villaweber import app
from flask import render_template
from helper.model import NavigationBar

@app.route("/")
def service():
    return 'Service is running'

@app.route("/villaweber/dashboard", methods=['GET'])
def main():
    nav_bar = NavigationBar()
    nav_bar.fetch_nav_items()
    
    return render_template("base.html", nav_bar=nav_bar)
