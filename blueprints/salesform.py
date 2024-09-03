from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from .func import get_db

sales_blueprint = Blueprint('sales', __name__, template_folder='templates')

@sales_blueprint.route('/sales', methods=['GET', 'POST'])
def sales_entry():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        sale_date = request.form.get('sale_date')
        branch_id = request.form.get('branch_id')
        sales_card_sweetdream = float(request.form.get('sales_card_sweetdream') or 0)
        sales_card_glory = float(request.form.get('sales_card_glory') or 0)
        sales_cash = float(request.form.get('sales_cash') or 0)
        sales_zeropay = float(request.form.get('sales_zeropay') or 0)
        sales_transfer = float(request.form.get('sales_transfer') or 0)

        # 기존 매출 데이터 조회
        cur.execute("""
            SELECT * FROM sales 
            WHERE sale_date = ? AND branch_id = ?
        """, (sale_date, branch_id))
        existing_data = cur.fetchone()

        if existing_data:
            # 기존 데이터 업데이트
            updated_sweetdream = existing_data['sales_card_sweetdream'] + sales_card_sweetdream
            updated_glory = existing_data['sales_card_glory'] + sales_card_glory
            updated_cash = existing_data['sales_cash'] + sales_cash
            updated_zeropay = existing_data['sales_zeropay'] + sales_zeropay
            updated_transfer = existing_data['sales_transfer'] + sales_transfer
            updated_total_sales = sum([
                updated_sweetdream, updated_glory, updated_cash, updated_zeropay, updated_transfer
            ])

            cur.execute("""
                UPDATE sales
                SET sales_card_sweetdream = ?, sales_card_glory = ?, sales_cash = ?, sales_zeropay = ?, sales_transfer = ?, total_sales = ?
                WHERE sale_date = ? AND branch_id = ?
            """, (updated_sweetdream, updated_glory, updated_cash, updated_zeropay, updated_transfer, updated_total_sales, sale_date, branch_id))
        else:
            # 새로운 매출 데이터 삽입
            cur.execute("""
                INSERT INTO sales (sale_date, branch_id, sales_card_sweetdream, sales_card_glory, sales_cash, sales_zeropay, sales_transfer, total_sales)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (sale_date, branch_id, sales_card_sweetdream, sales_card_glory, sales_cash, sales_zeropay, sales_transfer, sum([
                sales_card_sweetdream, sales_card_glory, sales_cash, sales_zeropay, sales_transfer
            ])))

        db.commit()
        return redirect(url_for('sales.sales_confirmation', sale_id=cur.lastrowid if not existing_data else existing_data['id']))

    else:
        return render_template('sales_entry.html')

@sales_blueprint.route('/sales/confirmation/<int:sale_id>')
def sales_confirmation(sale_id):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM sales WHERE id = ?', (sale_id,))
    sale_data = cur.fetchone()

    if sale_data:
        return render_template('sales_confirmation.html', sale=sale_data)
    return "매출 정보를 찾을 수 없습니다.", 404

@sales_blueprint.route('/api/branches')
def api_branches():
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT id, name FROM branches')
    branches = cur.fetchall()
    return jsonify([{'id': branch['id'], 'name': branch['name']} for branch in branches])
