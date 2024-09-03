# from flask import Blueprint, request, render_template, redirect, url_for, jsonify
# from .func import get_db

# employee_blueprint = Blueprint('employee', __name__, template_folder='templates')

# @employee_blueprint.route('/employee', methods=['GET', 'POST'])
# def employee():
#    return render_template('employee.html')


from flask import Blueprint, render_template

employee_blueprint = Blueprint('employee', __name__, template_folder='templates')

@employee_blueprint.route('/employee')
def employee():
    return render_template('employee.html')