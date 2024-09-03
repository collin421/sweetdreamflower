from flask import Blueprint, request, render_template, jsonify
from .func import get_db

branch_sales_blueprint = Blueprint('branch_sales', __name__, template_folder='templates')

@branch_sales_blueprint.route('/branch_sales', methods=['GET', 'POST'])
def branch_sales():
    db = get_db()
    branches = db.execute('SELECT id, name FROM branches').fetchall()
    branches_dict = {branch['id']: branch['name'] for branch in branches}  # 지점 ID와 이름 매핑

    selected_date = request.form.get('sale_date') if request.method == 'POST' else None
    selected_branch_id = request.form.get('branch_id')
    sales = []

    if selected_date:
        if selected_branch_id == 'all':
            sales = db.execute('''
                SELECT * FROM sales
                WHERE sale_date = ?
            ''', (selected_date,)).fetchall()
        elif selected_branch_id:
            sales = db.execute('''
                SELECT * FROM sales
                WHERE sale_date = ? AND branch_id = ?
            ''', (selected_date, int(selected_branch_id))).fetchall()

    return render_template('branch_sales.html', branches=branches, branches_dict=branches_dict, sales=sales, selected_date=selected_date, selected_branch_id=selected_branch_id)

@branch_sales_blueprint.route('/update_sale', methods=['POST'])
def update_sale():
    db = get_db()
    data = request.get_json()
    sale_id = data['sale_id']
    sales_card_sweetdream = float(data['sales_card_sweetdream'])
    sales_card_glory = float(data['sales_card_glory'])
    sales_cash = float(data['sales_cash'])
    sales_zeropay = float(data['sales_zeropay'])
    sales_transfer = float(data['sales_transfer'])
    total_sales = sales_card_sweetdream + sales_card_glory + sales_cash + sales_zeropay + sales_transfer

    db.execute('''
        UPDATE sales
        SET sales_card_sweetdream = ?, sales_card_glory = ?, sales_cash = ?, sales_zeropay = ?, sales_transfer = ?, total_sales = ?
        WHERE id = ?
    ''', (sales_card_sweetdream, sales_card_glory, sales_cash, sales_zeropay, sales_transfer, total_sales, sale_id))
    db.commit()

    return jsonify({'status': 'success'})

@branch_sales_blueprint.route('/delete_sale', methods=['POST'])
def delete_sale():
    db = get_db()
    sale_id = request.get_json()['sale_id']

    db.execute('DELETE FROM sales WHERE id = ?', (sale_id,))
    db.commit()

    return jsonify({'status': 'success'})
