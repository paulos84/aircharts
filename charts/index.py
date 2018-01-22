from flask import render_template, Blueprint


index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/chart/index')
def index():
    return render_template('index.html')

