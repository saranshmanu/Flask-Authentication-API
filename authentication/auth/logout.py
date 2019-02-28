from flask import redirect, url_for, Blueprint

logout_blueprint = Blueprint("logout", __name__)
@logout_blueprint.route('/auth/logout', methods = ['POST'])
def logout():
    return redirect(url_for('hello_world'))