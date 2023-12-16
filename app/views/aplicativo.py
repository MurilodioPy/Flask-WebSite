from flask import Blueprint, render_template


aplicativo_bp = Blueprint('aplicativo', __name__, template_folder='templates')

@aplicativo_bp.route('/')
def index():
    return render_template('index.html')

@aplicativo_bp.route('/about')
def about():
    return render_template('aplicativo/sobre.html')