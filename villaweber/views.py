from villaweber import app
from flask import render_template
from model.result import ErrorResult
from visualisation import Visualisation
from helper.log import Logger

@app.route("/")
def service():
    return 'Service is running'

@app.route("/villaweber/submit", methods=['PUT'])
def submit():
    # ToDo:
    pass

@app.route("/villaweber/<page_name>", methods=['GET'])
def page(page_name):
    error_message = None
    logger = Logger().get_logger(logger_name=__name__)
    visu = Visualisation(logger=logger)
    success = visu.build_navigation_bar()
    if success:
        success = visu.build_page(page_name)
        if success:
            bar = visu.get_navigation_bar()
            page = visu.get_page(page_name=page_name)
            template = render_template("villaweber.html", nav_bar=bar, page=page)
        else:
            error_message = 'Laden der Seite ' + page_name + ' fehlgeschlagen'
    else:
        error_message = 'Laden der Navigation Bar fehlgeschlagen'

    if error_message:
        result = ErrorResult(message=error_message)
        template = render_template("error.html", result=result)
    return template
