from villaweber import app
from flask import render_template, Markup
from villaweber.model.navigation import NavigationBar

@app.route("/")
def service():
    return 'Service is running'

@app.route("/villaweber/dashboard", methods=['GET'])
def main():
    nav_bar = NavigationBar()
    nav_bar.fetch_nav_items()
    
    return render_template("base.html", nav_bar=nav_bar)

@app.route("/villaweber/content", methods=['GET'])
def main():
    cards = Markup() # TODO
    # get target html file from navigation bar table
    return render_template("content.html", card_markup=cards)
